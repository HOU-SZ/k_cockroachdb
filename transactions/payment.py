from playhouse.cockroachdb import CockroachDatabase, DatabaseProxy
from decimal import Decimal
from datetime import datetime

from models import *
from transactions.base import BaseTransaction


class PaymentTransaction(BaseTransaction):
    def __init__(self, cus, payment):
        self.__w_id = cus[0]
        self.__d_id = cus[1]
        self.__id = cus[2]
        self.__payment = payment

    def _execute_transaction(self):

        Warehouse.update(ytd=Warehouse.ytd +
                         self.__payment).where(Warehouse.id == self.__w_id).execute()
        District.update(ytd=District.ytd + self.__payment).where((District.id ==
                                                                  self.__d_id) & (District.w_id == self.__w_id)).execute()
        Customer.update(
            balance=Customer.balance - self.__payment,
            ytd_payment=Customer.ytd_payment + self.__payment,
            payment_cnt=Customer.payment_cnt + 1
        ).where((Customer.w_id == self.__w_id) & (Customer.d_id == self.__d_id) & (Customer.id == self.__id)).execute()

        customer = Customer.get(Customer.w_id == self.__w_id,
                                Customer.d_id == self.__d_id, Customer.id == self.__id)
        warehouse = Warehouse.get(Warehouse.id == self.__w_id)
        district = District.get(
            District.id == self.__d_id, District.w_id == self.__w_id)

        print(f"Customer Info: ")
        print(f"    Identifier: ({self.__w_id}, {self.__d_id}, {self.__id})")
        print(f"    Name: {customer.first} {customer.middle} {customer.last}")
        print(
            f"    Adress: {customer.street_1}, {customer.street_2}, {customer.city}, {customer.state}, {customer.zip}\n")
        print(f"Warehouse's Address: ")
        print(
            f"    {warehouse.street_1}, {warehouse.street_2}, {warehouse.city}, {warehouse.state}, {warehouse.zip}\n")
        print(f"District's Address: ")
        print(
            f"    {district.street_1}, {district.street_2}, {district.city}, {district.state}, {district.zip}\n")
        print(f"Payment Amount: ")
        print(f"    {self.__payment}")
