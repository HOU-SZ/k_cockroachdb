from playhouse.cockroachdb import CockroachDatabase, DatabaseProxy
from decimal import Decimal
from datetime import datetime
from collections import Counter

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
        orders = Order.select().where(
            (Order.d_id == self.__district_number) & (Order.w_id == self.__warehouse_number) & (Order.id.between(n-1-self.__last_orders_number, n-1)))

        all_orders_items = []
        all_popular_items = []
        for order in orders:
            customer = Customer.get(Customer.id == order.c_id)
            print(f"Order Info: ")
            print(f"    Order Number: {order.id}")
            print(f"    Entry Dazte and Time: {order.entry_d}")
            print(
                f"    Customer Name: {customer.first}, {customer.middle}, {customer.last}\n")

            orderlines = Orderline.select(
                Orderline.i_id.alias("item_id"),
                Orderline.quantity.alias("item_quantity"),
                Item.name.alias("item_name")
            ).join(
                Item, on=(Item.id == Orderline.i_id)
            ).where(
                (Orderline.o_id == order.id) & (Orderline.d_id == self.__district_number) & (
                    Orderline.w_id == self.__warehouse_number)
            ).order_by(Orderline.quantity.desc()).dicts()

            orderlines_items = []
            popular_items = []
            max_quantity = orderlines[0]['item_quantity']

            for orderline in orderlines:
                if orderline["item_quantity"] == max_quantity:
                    popular_items.append(orderline)
                orderlines_items.append(orderline["item_name"])

            all_popular_items.append(popular_items)
            all_orders_items.append(orderlines_items)

            for item in popular_items:
                print(f"    Item Name: {item['item_name']}")
                print(f"    Item Quantity: {item['item_quantity']}\n")

        # print(all_orders_items)

        distinct_popular_items = []
        for popular_items in all_popular_items:
            item_names = [item["item_name"] for item in popular_items]
            distinct_popular_items.extend(item_names)
        distinct_popular_items = set(distinct_popular_items)

        for item in distinct_popular_items:
            print(f"    Distinct Popular Item Name: {item}")
            contain = list(map(lambda order: item in order, all_orders_items))
            percentage = round(
                Counter(contain)[1]/self.__last_orders_number, 4) * 100
            print(
                f"    The Percentage of Orders Contain This Item: {percentage}%\n")
