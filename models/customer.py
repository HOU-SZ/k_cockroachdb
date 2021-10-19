from datetime import datetime

from peewee import (
    IntegerField,
    DecimalField,
    FloatField,
    CharField,
    FixedCharField,
    DateTimeField,
    CompositeKey,
    SQL,
)

from models.base import BaseModel


class Customer(BaseModel):
    id = IntegerField(column_name="c_id", null=False)
    w_id = IntegerField(column_name="c_w_id", null=False)
    d_id = IntegerField(column_name="c_d_id", null=False)
    first = CharField(column_name="c_first", max_length=16, null=False)
    middle = FixedCharField(column_name="c_middle", max_length=2)
    last = CharField(column_name="c_last", max_length=16, null=False)
    street_1 = CharField(column_name="c_street_1", max_length=20)
    street_2 = CharField(column_name="c_street_2", max_length=20)
    city = CharField(column_name="c_city", max_length=20)
    state = FixedCharField(column_name="c_state", max_length=2)
    zip = FixedCharField(column_name="c_zip", max_length=9, null=False)
    phone = FixedCharField(column_name="c_phone", max_length=16)
    since = DateTimeField(column_name="c_since", null=False, default=datetime.utcnow())
    credit = CharField(column_name="c_credit", max_length=2)
    credit_lim = DecimalField(column_name="c_credit_lim", max_digits=12, decimal_places=2)
    discount = DecimalField(column_name="c_discount", max_digits=4, decimal_places=4)
    balance = DecimalField(column_name="c_balance", max_digits=12, decimal_places=2, null=False, default=0.00)
    ytd_payment = FloatField(column_name="c_ytd_payment", null=False, default=0.00)
    payment_cnt = IntegerField(column_name="c_payment_cnt", null=False, default=0)
    delivery_cnt = IntegerField(column_name="c_delivery_cnt", null=False, default=0)
    data = CharField(column_name="c_data", max_length=500)

    class Meta:
        primary_key = CompositeKey("w_id", "d_id", "id")
        constraints = [
            SQL(
                "FOREIGN KEY (c_w_id, c_d_id) "
                "REFERENCES district (d_w_id, d_id)"
            )
        ]
