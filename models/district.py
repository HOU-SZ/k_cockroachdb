from peewee import (
    IntegerField,
    DecimalField,
    CharField,
    FixedCharField,
    ForeignKeyField,
    CompositeKey,
)

from models.base import BaseModel
from models.warehouse import Warehouse


class District(BaseModel):
    id = IntegerField(column_name="d_id", null=False)
    w_id = ForeignKeyField(Warehouse, backref="w_id", column_name="d_w_id", null=False)
    name = CharField(column_name="d_name", max_length=10, null=False)
    street_1 = CharField(column_name="d_street_1", max_length=20)
    street_2 = CharField(column_name="d_street_2", max_length=20)
    city = CharField(column_name="d_city", max_length=20)
    state = FixedCharField(column_name="d_state", max_length=2)
    zip = FixedCharField(column_name="d_zip", max_length=9, null=False)
    tax = DecimalField(column_name="d_tax", max_digits=4, decimal_places=4, null=False)
    ytd = DecimalField(column_name="d_ytd", max_digits=12, decimal_places=2, null=False, default=0.00)
    next_o_id = IntegerField(column_name="d_next_o_id", null=False, default=2)

    class Meta:
        primary_key = CompositeKey("w_id", "id")
