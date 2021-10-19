from peewee import (
    IntegerField,
    DecimalField,
    CharField,
    ForeignKeyField,
    CompositeKey,
)

from models.base import BaseModel
from models.warehouse import Warehouse
from models.item import Item


class Stock(BaseModel):
    w_id = ForeignKeyField(Warehouse, backref="w_id", column_name="s_w_id", null=False)
    i_id = ForeignKeyField(Item, backref="i_id", column_name="s_i_id", null=False)
    quantity = DecimalField(column_name="s_quantity", max_digits=4, decimal_places=0, null=False, default=0)
    ytd = DecimalField(column_name="s_ytd", max_digits=8, decimal_places=2, null=False, default=0.00)
    order_cnt = IntegerField(column_name="s_order_cnt", null=False, default=0)
    remote_cnt = IntegerField(column_name="s_remote_cnt", null=False, default=0)
    dist_1 = CharField(column_name="s_dist_01", max_length=24)
    dist_2 = CharField(column_name="s_dist_02", max_length=24)
    dist_3 = CharField(column_name="s_dist_03", max_length=24)
    dist_4 = CharField(column_name="s_dist_04", max_length=24)
    dist_5 = CharField(column_name="s_dist_05", max_length=24)
    dist_6 = CharField(column_name="s_dist_06", max_length=24)
    dist_7 = CharField(column_name="s_dist_07", max_length=24)
    dist_8 = CharField(column_name="s_dist_08", max_length=24)
    dist_9 = CharField(column_name="s_dist_09", max_length=24)
    dist_10 = CharField(column_name="s_dist_10", max_length=24)
    data = CharField(column_name="s_data", max_length=50)

    class Meta:
        primary_key = CompositeKey("w_id", "i_id")
