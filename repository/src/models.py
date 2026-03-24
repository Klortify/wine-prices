from peewee import (
    Model,
    CharField,
    IntegerField,
    FloatField,
)
from db import db


class BaseModel(Model):
    class Meta:
        database = db


class WineMonthlyAveragePrice(BaseModel):
    member_state_code = CharField(index=True)
    member_state_name = CharField()
    description = CharField()
    year = IntegerField()
    month = IntegerField()
    avg_price_value = FloatField()

    class Meta:
        indexes = (
            (("member_state_code", "description", "year", "month"), True),
        )


class WinePrice(BaseModel):
    member_state_code = CharField()
    member_state_name = CharField()

    year = IntegerField()
    month = IntegerField()
    day = IntegerField()
    week_number = IntegerField()

    description = CharField()

    price_raw = CharField()
    price_value = FloatField(null=True)

    class Meta:
        indexes = (
            (
                (
                    "member_state_code",
                    "year",
                    "month",
                    "day",
                    "week_number",
                    "description",
                ),
                True,
            ),
        )
