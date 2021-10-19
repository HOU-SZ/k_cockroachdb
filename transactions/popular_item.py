from playhouse.cockroachdb import CockroachDatabase, DatabaseProxy
from decimal import Decimal
from datetime import datetime

from models import *
from transactions.base import BaseTransaction


class PopularItemTransaction(BaseTransaction):
    def __init__(self, warehouse_number, district_number, last_orders_number):
        self.__warehouse_number = warehouse_number
        self.__district_number = district_number
        self.__last_orders_number = last_orders_number

    def _execute_transaction(self):

        print(
            f"District Identifier: ({self.__warehouse_number}, {self.__district_number})\n")
        print(f"Number of Last orders: {self.__last_orders_number}\n")

        n = District.get((District.w_id == self.__warehouse_number) &
                         (District.id == self.__district_number)).next_o_id
        s = Order.select().where(
            (Order.d_id == self.__district_number) & (Order.w_id == self.__warehouse_number) & (Order.id.between(n-1-self.__last_orders_number, n-1)))

        for x in s:
            customer = Customer.get(Customer.id == x.c_id)
            print(f"\nOrder Info: ")
            print(f"    Order Number: {x.id}")
            print(f"    Entry Dazte and Time: {x.entry_d}")
            print(
                f"    Customer Name: {customer.first}, {customer.middle}, {customer.last}")
            ix = Orderline.select().where(
                (Orderline.o_id == x.id) & (Orderline.d_id == self.__district_number) & (
                    Orderline.w_id == self.__warehouse_number)
            ).order_by(Orderline.quantity.desc())
            px = []
            max_quantity = ix[0].quantity
            for orderline in ix:
                if orderline.quantity == max_quantity:
                    px.append(orderline)
                else:
                    break
            for item in px:
                print(f"Item Name: {Item.get(Item.id == item.i_id).name}")
                print(f"Item Quantity: {item.quantity}")
