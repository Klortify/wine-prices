from typing import List, Dict
import requests
from api_client import WineAPIClient
from config import settings
from datetime import datetime

def parse_date(value):
    if not value:
        return None
    return datetime.strptime(value, "%d/%m/%Y").date()

def parse_price(value: str | None) -> float | None:
    if not value:
        return None
    try:
        return float(value[1:])
    except Exception:
        return None


def upsert_prices(rows: List[Dict]) -> int:
    payload = []
    for row in rows:
        begin_date = parse_date(row.get("beginDate"))
        payload.append({
            "member_state_code": row.get("memberStateCode"),
            "member_state_name": row.get("memberStateName"),
            "year": begin_date.year,
            "month": begin_date.month,
            "day": begin_date.day,
            "week_number": row.get("weekNumber"),
            "description": row.get("description"),
            "price_raw": row.get("price"),
            "price_value": parse_price(row.get("price")),
        })

    resp = requests.post(
        f"{settings.repository_url}/prices/batch",
        json=payload,
        timeout=settings.request_timeout
    )
    resp.raise_for_status()
    return resp.json().get("inserted", 0)


def run_etl()->int:
    with WineAPIClient() as client:
        rows = client.get_prices()
        print(f"Fetched rows: {len(rows)}")

        inserted = upsert_prices(rows)
        print(f"Inserted rows: {inserted}")

        return inserted