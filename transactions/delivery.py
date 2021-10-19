from decimal import Decimal
from datetime import datetime

from models import *
from transactions import BaseTransaction

class DeliveryTransaction(BaseTransaction):
    def __init__(self, w_id, carrier_id):
        self.__w_id = w_id
        self.__carrier_id = carrier_id
    
    def _execute_transaction(self):
        for i in range(1, 11):
            query = Order.select(Order.id).where(
                Order.w_id == self.__w_id,
                Order.d_id == i,
                Order.carrier_id.is_null()
            )
            order_list = database.execute(query).fetchall()
            if not order_list:
                return
            n = min(list(map(lambda x: x[0], order_list)))
            total_amount = 0

            order = Order.get_by_id((self.__w_id, i, n))
            customer = Customer.get_by_id((self.__w_id, i, order.c_id))

            # update order
            order.update(carrier_id = self.__carrier_id).execute()

            # update orderline
            for j in range(int(order.ol_cnt)):
                orderline = Orderline.get_by_id((j+1, self.__w_id, i, order.id))
                orderline.update(delivery_d = datetime.utcnow()).execute()
                total_amount += orderline.amount
            
            # update customer
            customer.update(
                balance = customer.balance + total_amount, 
                delivery_cnt = customer.delivery_cnt + 1
            ).execute()


