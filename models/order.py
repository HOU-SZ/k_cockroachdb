from datetime import datetime

from peewee import IntegerField, DecimalField, DateTimeField, CompositeKey, SQL

from models.base import BaseModel


class Order(BaseModel):
    id = IntegerField(column_name="o_id", null=False)
    w_id = IntegerField(column_name="o_w_id", null=False)
    d_id = IntegerField(column_name="o_d_id", null=False)
    c_id = IntegerField(column_name="o_c_id", null=False)
    carrier_id = IntegerField(column_name="o_carrier_id")
    ol_cnt = DecimalField(column_name="o_ol_cnt", max_digits=2, decimal_places=0, null=False)
    all_local = DecimalField(column_name="o_all_local", max_digits=1, decimal_places=0)
    entry_d = DateTimeField(column_name="o_entry_d", default=datetime.utcnow())

    class Meta:
        primary_key = CompositeKey("w_id", "d_id", "id")
        constraints = [
            SQL(
                "FOREIGN KEY (o_w_id, o_d_id, o_c_id) "
                "REFERENCES customer (c_w_id, c_d_id, c_id)"
            )
        ]
        indexes = (("w_id", "d_id", "c_id", "id"), True)
