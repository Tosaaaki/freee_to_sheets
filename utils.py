"""ユーティリティ関数群"""
import datetime

def jst_today():
    """JSTの日付を文字列で返す"""
    return (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).date().isoformat()
