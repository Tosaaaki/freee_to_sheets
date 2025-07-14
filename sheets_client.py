"""Google Sheets 操作用クライアント"""
from googleapiclient.discovery import build
from google.auth import default


def append_rows(sheet_id: str, rows: list[list], rng: str = "Attendance!A1"):
    """指定シートに行を追記する"""
    creds, _ = default(scopes=["https://www.googleapis.com/auth/spreadsheets"])
    service = build("sheets", "v4", credentials=creds)
    body = {"values": rows}
    service.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range=rng,
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",
        body=body,
    ).execute()

