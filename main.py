"""Cloud Function エントリーポイント"""
import os
import json
import base64
import logging
from typing import Any

from freee_client import get_attendances
from sheets_client import append_rows
from utils import jst_today


def _parse_event(event: dict) -> dict:
    if not event or "data" not in event:
        return {}
    return json.loads(base64.b64decode(event["data"]).decode())


def main(event: dict, context: Any) -> str:
    logging.basicConfig(level=logging.INFO)
    payload = _parse_event(event)
    mode = payload.get("mode", "daily")

    if mode == "daily":
        start = end = jst_today()
    else:
        start = payload.get("start_date", jst_today())
        end = payload.get("end_date", start)

    records = get_attendances(start, end)
    rows = []
    for r in records:
        rows.append([
            r.get("record_date"),
            r.get("clock_in_at"),
            r.get("clock_out_at"),
            r.get("break_duration"),
        ])

    if rows:
        append_rows(
            os.environ["TARGET_SHEET_ID"],
            rows,
            os.getenv("SHEET_RANGE", "Attendance!A1"),
        )
        logging.info("append %d rows", len(rows))
    else:
        logging.info("no records")
    return "ok"

