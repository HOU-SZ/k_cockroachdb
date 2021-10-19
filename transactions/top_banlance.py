from playhouse.cockroachdb import CockroachDatabase, DatabaseProxy
from decimal import Decimal
from datetime import datetime

from models import *
from transactions.base import BaseTransaction


class TopBanlanceTransaction(BaseTransaction):
    def _execute_transaction(self):
        top_customers = (Customer.select(
            Customer.first.alias("first_name"),
            Customer.middle.alias("middle_name"),
            Customer.last.alias("last_name"),
            Customer.balance.alias("balance"),
            Customer.w_id,
            Customer.d_id,
            Warehouse.name.alias("warehouse_name"),
            District.name.alias("district_name")).join(
                Warehouse, on=(Warehouse.id == Customer.w_id)).join(
                    District, on=((District.w_id == Customer.w_id) & (District.id == Customer.d_id))).order_by(Customer.balance.desc()).limit(10).dicts())

        # print(top_customers)
        for customer in top_customers:
            print(f"Customer Info: ")
            print(
                f"    Name: {customer['first_name']} {customer['middle_name']} {customer['last_name']}")
            print(f"    Balance: {customer['balance']}")
            print(f"    Warehouse Name: {customer['warehouse_name']}")
            print(f"    District Name: {customer['district_name']}\n")
