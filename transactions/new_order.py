from decimal import Decimal
from datetime import datetime

from models import *
from transactions.base import BaseTransaction


class NewOrderTransaction(BaseTransaction):
    def __init__(self, cus, num_items, item_number, supplier_warehouse, quantity):
        self.__w_id = cus[0]
        self.__d_id = cus[1]
        self.__c_id = cus[2]
        self.__num_items = num_items
        self.__item_number = item_number
        self.__supplier_warehouse = supplier_warehouse
        self.__quantity = quantity


    def _execute_transaction(self):
        warehouse = Warehouse.get_by_id(self.__w_id)
        district = District.get_by_id((self.__w_id, self.__d_id))
        customer = Customer.get_by_id((self.__w_id, self.__d_id, self.__c_id))

        order_id = district.next_o_id
        is_local = list(map(lambda x: x == self.__w_id, self.__supplier_warehouse))
        all_is_local = all(is_local)
        total_amount = 0
        
        order = self.__create_order(order_id, all_is_local)
        self.__update_district(district)

        print(f"Customer Info: ")
        print(f"    Identifier: ({self.__w_id}, {self.__d_id}, {self.__c_id})")
        print(f"    Lastname: {customer.last}")
        print(f"    Credit: {customer.credit}")
        print(f"    Discount: {customer.discount}")
        print(f"Tax Rate: ")
        print(f"    Warehouse: {warehouse.tax}")
        print(f"    District: {district.tax}")
        print(f"Order Info: ")
        print(f"    Order ID: {order.id}")
        print(f"    Entry Data: {order.entry_d}")
        print(f"    Number of Items: {self.__num_items}")
        print(f"Item Info: ")
        
        for i in range(self.__num_items):
            
            stock = Stock.get_by_id((self.__supplier_warehouse[i], self.__item_number[i]))
            item = Item.get_by_id(self.__item_number[i])
            
            adjusted_qty = stock.quantity - self.__quantity[i]

            self.__update_stock(i, stock, adjusted_qty, is_local[i])
            orderline = self.__create_orderline(i, order_id, stock, item)

            total_amount += orderline.amount

            print(f"  --Item ID: {item.id}")
            print(f"    Order ID: {item.name}")
            print(f"    Supply Warehouse: {self.__supplier_warehouse[i]}")
            print(f"    Quantity: {self.__quantity[i]}")
            print(f"    Item Amount: {orderline.amount}")
            print(f"    Stock: {stock.quantity}")

        total_amount = total_amount * (1 + warehouse.tax + district.tax) * (1 - customer.discount)
        print(f"Total Amount: {total_amount}")


    def __create_order(self, order_id, all_is_local):
        order = Order.create(
            id = order_id, 
            w_id = self.__w_id,
            d_id = self.__d_id,
            c_id = self.__c_id,
            carrier_id = None,
            ol_cnt = Decimal(self.__num_items),
            all_local = Decimal(all_is_local),
            entry_d = datetime.utcnow()
        )
        return  order
    

    def __update_district(self, district):
        district.update(
            next_o_id = district.next_o_id + 1
        ).execute()


    def __update_stock(self, i, stock, adjusted_qty, is_local_i):
        stock.update(
            quantity = adjusted_qty if adjusted_qty >= 10 else adjusted_qty + 100,
            ytd = stock.ytd + self.__quantity[i],
            order_cnt = stock.order_cnt + 1,
            remote_cnt = stock.remote_cnt + is_local_i
        ).execute()
    

    def __create_orderline(self, i, order_id, stock, item):
        orderline = Orderline.create(
            number = i + 1,
            w_id = self.__w_id,
            d_id = self.__d_id,
            o_id = order_id, 
            i_id = self.__item_number[i],
            supply_w_id = self.__supplier_warehouse[i],
            quantity = self.__quantity[i],
            amount = self.__quantity[i] * item.price,
            delivery_d = None,
            dist_info = getattr(stock, f"dist_{self.__d_id}")
        )
        return orderline



# ### test
# new_order = NewOrderTransaction((1,1,1), 2, [1, 2], [1, 1], [5, 3])
# new_order.execute()
