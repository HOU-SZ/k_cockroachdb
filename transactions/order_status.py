from models import *
from transactions import BaseTransaction

class OrderStatusTransaction(BaseTransaction):
    def __init__(self, cus):
        self.__w_id = cus[0]
        self.__d_id = cus[1]
        self.__c_id = cus[2]
    
    def _execute_transaction(self):
        customer = Customer.get_by_id((self.__w_id, self.__d_id, self.__c_id))
        
        order = Order.select().where(
            Order.w_id == self.__w_id, 
            Order.d_id == self.__d_id, 
            Order.c_id == self.__c_id
        ).order_by(
            Order.entry_d.desc()
        ).limit(1).get()

        print(f"Customer Info: ")
        print(f"    Name: {customer.name}")
        print(f"    Balance: {customer.balance}")
        print(f"Last Order Info: ")
        print(f"    Order ID: {order.id}")
        print(f"    Entry Date: {order.entry_d}")
        print(f"    Carrier ID: {order.carrier_id}")
        print(f"Item Info: ")

        orderlines = Orderline.select().where(
            Orderline.w_id == self.__w_id,
            Orderline.d_id == self.__d_id,
            Orderline.o_id == order.id
        )

        for orderline in orderlines:
            print(f"  --Item ID: {orderline.i_id}")
            print(f"    Supply Warehouse: {orderline.supply_w_id}")
            print(f"    Quantity: {orderline.quantity}")
            print(f"    Item Amount: {orderline.amount}")
            print(f"    Delivery Date: {orderline.delivery_d}")
