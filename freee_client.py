import requests, datetime, os, json
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

def refresh_access_token():
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
    # freee は 「使い捨て refresh_token」仕様 なので新 RT を保存
    cred["refresh_token"] = tok["refresh_token"]
    _save_secret(cred)
    return tok["access_token"]