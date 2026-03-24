from typing import List, Dict

from api_client import WineAPIClient
from models import WinePrice
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


def     upsert_prices(rows: List[Dict]) -> int:
    inserted = 0

    with WinePrice._meta.database.atomic():
        for row in rows:
            begin_date = parse_date(row.get("beginDate"))
            _, created = WinePrice.get_or_create(
                member_state_code=row.get("memberStateCode"),
                year=begin_date.year,
                month=begin_date.month,
                day=begin_date.day,
                week_number=row.get("weekNumber"),
                description=row.get("description"),
                defaults={
                    "member_state_name": row.get("memberStateName"),
                    "price_raw": row.get("price"),
                    "price_value": parse_price(row.get("price")),
                },
            )
            if created:
                inserted += 1

    return inserted


def run_etl()->int:
    with WineAPIClient() as client:
        rows = client.get_prices()
        print(f"Fetched rows: {len(rows)}")

        inserted = upsert_prices(rows)
        print(f"Inserted rows: {inserted}")

        return inserted