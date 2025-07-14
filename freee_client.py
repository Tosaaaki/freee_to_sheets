import os
import json
import requests
from google.cloud import secretmanager

BASE = "https://api.freee.co.jp"
TOKEN_URL = "https://accounts.secure.freee.co.jp/public_api/token"


def _load_secret():
    client = secretmanager.SecretManagerServiceClient()
    name = os.environ["FREEE_SECRET_NAME"]  # projects/xxx/secrets/freee-oauth-cred/versions/latest
    payload = client.access_secret_version(request={"name": name}).payload.data.decode()
    return json.loads(payload)


def _save_secret(new_json: dict):
    client = secretmanager.SecretManagerServiceClient()
    parent = "/".join(os.environ["FREEE_SECRET_NAME"].split("/versions/")[0:1])
    client.add_secret_version(parent=parent, payload={"data": json.dumps(new_json).encode()})


def refresh_access_token() -> str:
    cred = _load_secret()
    data = {
        "grant_type": "refresh_token",
        "refresh_token": cred["refresh_token"],
        "client_id": cred["client_id"],
        "client_secret": cred["client_secret"],
    }
    resp = requests.post(TOKEN_URL, data=data, timeout=10)
    resp.raise_for_status()
    tok = resp.json()
    # freee は使い捨て refresh_token 仕様なので新 RT を保存
    cred["refresh_token"] = tok["refresh_token"]
    _save_secret(cred)
    return tok["access_token"]


def get_attendances(start_date: str, end_date: str) -> list[dict]:
    """指定期間の勤怠データを取得"""
    token = refresh_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "company_id": os.environ["FREEE_COMPANY_ID"],
        "start_date": start_date,
        "end_date": end_date,
    }
    emp_id = os.environ["FREEE_EMPLOYEE_ID"]
    url = f"{BASE}/api/v1/employees/{emp_id}/attendances"
    resp = requests.get(url, headers=headers, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json().get("attendances", [])

