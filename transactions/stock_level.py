from models import *
from transactions import BaseTransaction

class StockLevelTransaction(BaseTransaction):
    def __init__(self, w_id, d_id, threshold, num_order):
        self.__w_id = w_id
        self.__d_id = d_id
        self.__th = threshold
        self.__num_order = num_order
    
    def _execute_transaction(self):
        n = District.get_by_id((self.__w_id, self.__d_id)).next_o_id
        item_list = set()
        
        for i in range(n - self.__num_order, n):
            order = Order.get_by_id((self.__w_id, self.__d_id, i))
            for j in range(int(order.ol_cnt)):
                orderline = Orderline.get_by_id((j+1, self.__w_id, self.__d_id, i))
                item = Item.get_by_id(orderline.i_id)
                item_list.add(item.id)

        res = len(list(filter(
            lambda x: int(Stock.get_by_id((self.__w_id, x)).quantity) < self.__th, 
            item_list
        )))
        
        print(f"Stock Level: ")
        print(f"    Warehouse: {self.__w_id}")
        print(f"    Order Info: last {self.__num_order} orders in District {self.__d_id}")
        print(f"    Level: {res}")
