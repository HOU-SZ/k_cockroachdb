from peewee import (
    IntegerField,
    DecimalField,
    CharField,
    DateTimeField,
    ForeignKeyField,
    CompositeKey,
    SQL,
)

from models.base import BaseModel
from models.item import Item


class Orderline(BaseModel):
    number = IntegerField(column_name="ol_number", null=False)
    w_id = IntegerField(column_name="ol_w_id", null=False)
    d_id = IntegerField(column_name="ol_d_id", null=False)
    o_id = IntegerField(column_name="ol_o_id", null=False)
    i_id = ForeignKeyField(Item, backref="i_id", column_name="ol_i_id", null=False)
    delivery_d = DateTimeField(column_name="ol_delivery_d")
    amount = DecimalField(column_name="ol_amount", max_digits=7, decimal_places=2, null=False)
    supply_w_id = IntegerField(column_name="ol_supply_w_id", null=False)
    quantity = DecimalField(column_name="ol_quantity", max_digits=2, decimal_places=0, null=False)
    dist_info = CharField(column_name="ol_dist_info", max_length=24)

    class Meta:
        primary_key = CompositeKey(
            "number", "w_id", "d_id", "o_id"
        )
        constraints = [
            SQL(
                "FOREIGN KEY (ol_w_id, ol_d_id, ol_o_id) "
                "REFERENCES order (o_w_id, o_d_id, o_id)"
            )
        ]
        indexes = (("w_id", "d_id", "o_id"), False)
