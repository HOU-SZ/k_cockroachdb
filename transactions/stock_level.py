from models import *
from transactions import BaseTransaction

class StockLevelTransaction(BaseTransaction):
    def __init__(self, w_id, d_id, threshold, num_order):
        self.__w_id = w_id
        self.__d_id = d_id
        self.__th = threshold
        self.__num_order = num_order
    
    def _execute_transaction(self):

        orderlines = Orderline.select(
            Orderline.i_id.alias("i_id")
        ).join(
            District,
            on = (
                (Orderline.w_id == District.w_id) & 
                (Orderline.d_id == District.id)
            )
        ).distinct().where(
            (Orderline.w_id == self.__w_id) & 
            (Orderline.d_id == self.__d_id) & 
            (Orderline.o_id >= District.next_o_id - self.__num_order)
        )

        item_num = Stock.select().join(
            orderlines,
            on=(
                (Stock.w_id == self.__w_id) & 
                (Stock.i_id == orderlines.c.i_id)
            ),
        ).where(
            Stock.quantity < self.__th
        ).count()


        print(f"Stock Level: ")
        print(f"    Warehouse: {self.__w_id}")
        print(f"    Order Info: last {self.__num_order} orders in District {self.__d_id}")
        print(f"    Level: {item_num}")
