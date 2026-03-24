from contextlib import asynccontextmanager
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel as PydanticBaseModel
from models import WinePrice
from db import init_db, db

@asynccontextmanager
async def lifespan(app: FastAPI):
    import time
    import logging
    retries = 5
    while retries > 0:
        try:
            init_db([WinePrice])
            break
        except Exception as e:
            logging.error(f"DB connection failed: {e}. Retrying...")
            retries -= 1
            time.sleep(2)
    if retries == 0:
        raise RuntimeError("Could not connect to database")
    yield
    if not db.is_closed():
        db.close()

app = FastAPI(title="Wine Repository Service", lifespan=lifespan)

class WinePriceCreate(PydanticBaseModel):
    member_state_code: str
    member_state_name: str
    year: int
    month: int
    day: int
    week_number: int
    description: str
    price_raw: str
    price_value: Optional[float] = None

class WinePriceRead(WinePriceCreate):
    id: int

    class Config:
        from_attributes = True


@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/prices", response_model=WinePriceRead)
def create_price(price: WinePriceCreate):
    with db.atomic():
        obj, created = WinePrice.get_or_create(
            member_state_code=price.member_state_code,
            year=price.year,
            month=price.month,
            day=price.day,
            week_number=price.week_number,
            description=price.description,
            defaults={
                "member_state_name": price.member_state_name,
                "price_raw": price.price_raw,
                "price_value": price.price_value,
            }
        )
    return obj

@app.post("/prices/batch")
def create_prices_batch(prices: List[WinePriceCreate]):
    inserted_count = 0
    with db.atomic():
        for price in prices:
            _, created = WinePrice.get_or_create(
                member_state_code=price.member_state_code,
                year=price.year,
                month=price.month,
                day=price.day,
                week_number=price.week_number,
                description=price.description,
                defaults={
                    "member_state_name": price.member_state_name,
                    "price_raw": price.price_raw,
                    "price_value": price.price_value,
                }
            )
            if created:
                inserted_count += 1
    return {"inserted": inserted_count}

@app.get("/prices", response_model=List[WinePriceRead])
def list_prices(limit: int = 100, offset: int = 0):
    prices = WinePrice.select().offset(offset).limit(limit)
    return list(prices)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
