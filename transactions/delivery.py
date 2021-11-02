from decimal import Decimal
from datetime import datetime
from peewee import fn

from models import *
from transactions import BaseTransaction

class DeliveryTransaction(BaseTransaction):
    def __init__(self, w_id, carrier_id):
        self.__w_id = w_id
        self.__carrier_id = carrier_id
    
    def _execute_transaction(self):
        for i in range(1, 11):
            try:
                order = Order.select(Order.id).where(
                    Order.w_id == self.__w_id,
                    Order.d_id == i,
                    Order.carrier_id.is_null()
                ).order_by(Order.id).limit(1).get()
            except order.DoesNotExist:
                continue

            order_id = order.id
            
            order_line = Orderline.select(
                fn.SUM(Orderline.amount).alias("total_amount")
            ).where(
                Orderline.w_id == self.__w_id, 
                Orderline.d_id == i, 
                Orderline.o_id == order_id
            ).get()

            # update order
            Order.update(carrier_id = self.__carrier_id).where(
                Order.id == order.id,
                Order.w_id == order.w_id,
                Order.d_id == order_id
            ).execute()

            # update orderline
            Orderline.update(delivery_d = datetime.utcnow()).where(
                Orderline.w_id == self.__w_id,
                Orderline.d_id == i,
                Orderline.o_id == order_id
            ).execute()
            
            # update customer
            Customer.update(
                balance = Customer.balance + order_line.total_amount, 
                delivery_cnt = Customer.delivery_cnt + 1
            ).where(
                Customer.id == order.c_id,
                Customer.w_id == self.__w_id,
                Customer.d_id == i
            ).execute()

