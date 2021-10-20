from models import *
from transactions import BaseTransaction

class RelatedCustomerTransaction(BaseTransaction):
    def __init__(self, cus):
        self.__w_id = cus[0]
        self.__d_id = cus[1]
        self.__c_id = cus[2]
    
    def _execute_transaction(self):
        customer = Customer.get_by_id((self.__w_id, self.__d_id, self.__c_id))

        query = Order.select(Order.id).where(
            Order.w_id == self.__w_id,
            Order.d_id == self.__d_id,
            Order.c_id == self.__c_id
        )

        order_list = database.execute(query).fetchall()
        item_list_all = []

        for i in order_list:
            order_item_list = []
            order_id = i[0]
            order = Order.get_by_id((self.__w_id, self.__d_id, order_id))
            for j in range(int(order.ol_cnt)):
                orderline = Orderline.get_by_id((j+1, self.__w_id, self.__d_id, order_id))
                item = Item.get_by_id(orderline.i_id)
                order_item_list.append(item.id)
            item_list_all.append(order_item_list)

        query = Customer.select(
            Customer.w_id, 
            Customer.d_id, 
            Customer.id, 
            Order.id, 
            Order.ol_cnt
        ).join(
            Order, on = (
                (Order.c_id == Customer.id) &
                (Order.w_id == Customer.w_id) &
                (Order.d_id == Customer.d_id)
            )
        ).where(
            Customer.w_id != customer.w_id,
            Order.ol_cnt > 1
        )

        customer_list = database.execute(query).fetchall()
        related_customer_list = []

        for customer_order in customer_list:
            if (customer_order[0], customer_order[1], customer_order[2]) in related_customer_list:
                continue
            order_item_list = []
            for j in range(int(customer_order[4])):
                orderline = Orderline.get_by_id((j+1, customer_order[0], customer_order[1], customer_order[3]))
                item = Item.get_by_id(orderline.i_id)
                order_item_list.append(item.id)
            
            related_flag = 0

            for item_list in item_list_all:
                num_related_item = 0
                for order_item_id in order_item_list:
                    num_related_item += 1 if order_item_id in item_list else 0
                    if num_related_item >= 2:
                        related_flag = 1
                        break
                if related_flag:
                    break
            
            if related_flag:
                related_customer_list.append((customer_order[0], customer_order[1], customer_order[2]))
        
        print(f"Related Customers: ")
        for i in related_customer_list:
            print(f"    {i}") 

