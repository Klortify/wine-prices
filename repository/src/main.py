from contextlib import asynccontextmanager
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel as PydanticBaseModel
from models import WinePrice, WineMonthlyAveragePrice
from db import init_db, db

@asynccontextmanager
async def lifespan(app: FastAPI):
    import time
    import logging
    retries = 5
    while retries > 0:
        try:
            init_db([WinePrice, WineMonthlyAveragePrice])
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

class WineMonthlyAverage(PydanticBaseModel):
    member_state_code: str
    member_state_name: str
    description: str
    year: int
    month: int
    avg_price_value: float

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

@app.get("/prices")
def get_prices_for_processing():
    """Fetch raw price data for the processor service."""
    query = WinePrice.select(
        WinePrice.member_state_code,
        WinePrice.member_state_name,
        WinePrice.description,
        WinePrice.year,
        WinePrice.month,
        WinePrice.day,
        WinePrice.price_value
    )
    return list(query.dicts())

@app.get("/prices/averages", response_model=List[WineMonthlyAverage])
def get_monthly_averages():
    """Fetch all monthly averages."""
    query = WineMonthlyAveragePrice.select().order_by(
        WineMonthlyAveragePrice.year.desc(),
        WineMonthlyAveragePrice.month.desc(),
        WineMonthlyAveragePrice.member_state_code
    )
    return list(query.dicts())

@app.post("/prices/averages/batch")
def save_monthly_averages_batch(averages: List[WineMonthlyAverage]):
    count = 0
    with db.atomic():
        for avg in averages:
            obj, created = WineMonthlyAveragePrice.get_or_create(
                member_state_code=avg.member_state_code,
                description=avg.description,
                year=avg.year,
                month=avg.month,
                avg_price_value=avg.avg_price_value
            )
            if not created:
                obj.member_state_name = avg.member_state_name
                obj.avg_price_value = avg.avg_price_value
                obj.save()
            count += 1
    return {"inserted": count}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
