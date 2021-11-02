from peewee import Tuple

from models import *
from transactions import BaseTransaction

class RelatedCustomerTransaction(BaseTransaction):
    def __init__(self, cus):
        self.__w_id = cus[0]
        self.__d_id = cus[1]
        self.__c_id = cus[2]
    
    def _execute_transaction(self):
        # customer = Customer.get_by_id((self.__w_id, self.__d_id, self.__c_id))

        orders = (
            Order.select(Order.id.alias("id")).where(
                Order.w_id == self.__w_id,
                Order.d_id == self.__d_id,
                Order.c_id == self.__c_id
            )
        ).cte("orders")

        orderlines = (
            Orderline.select(
                Orderline.o_id.alias("o_id"),
                Orderline.i_id.alias("i_id")
            ).distinct().join(
                orders,
                on = (
                    (Orderline.w_id == self.__w_id) &
                    (Orderline.d_id == self.__d_id) &
                    (Orderline.o_id == orders.c.id)
                )
            )
        ).cte("orderlines")

        orderlines_2 = orderlines.alias("orderlines_2")

        item_pairs = (
            orderlines.select(
                orderlines.c.i_id.alias("i_id_1"),  
                orderlines_2.c.i_id.alias("i_id_2")
            ).join(
                orderlines_2,
                on = (
                    orderlines_2.c.o_id == orderlines.c.o_id
                )
            ).where(
                orderlines.c.i_id < orderlines_2.c.i_id
            )
        ).cte("item_pairs")


        related_orderlines = (
            Orderline.select(
                Orderline.w_id.alias("w_id"),
                Orderline.d_id.alias("d_id"),
                Orderline.o_id.alias("o_id"),
                Orderline.i_id.alias("i_id")
            ).distinct().where(
                (Orderline.w_id != self.__w_id) &
                Orderline.i_id.in_(
                    orderlines.select(
                        orderlines.c.i_id
                    ).distinct()
                )
            )
        ).cte("related_orderlines")

        related_orderlines_2 = related_orderlines.alias("related_orderlines_2")

        related_customers = related_orderlines.select(
            related_orderlines.c.w_id.alias("w_id"),
            related_orderlines.c.d_id.alias("d_id"),
            Order.c_id.alias("c_id")
        ).distinct().join(
            related_orderlines_2,
            on = (
                (related_orderlines_2.c.w_id == related_orderlines.c.w_id) &
                (related_orderlines_2.c.d_id == related_orderlines.c.d_id) &
                (related_orderlines_2.c.o_id == related_orderlines.c.o_id) &
                (related_orderlines.c.i_id < related_orderlines_2.c.i_id)
            )
        ).join(
            Order,
            on = (
                (Order.w_id == related_orderlines.c.w_id) &
                (Order.d_id == related_orderlines.c.d_id) &
                (Order.id == related_orderlines.c.o_id)
            )
        ).where(
            Tuple(
                related_orderlines.c.i_id,
                related_orderlines_2.c.i_id
            ).in_(
                item_pairs.select(
                    item_pairs.c.i_id_1,
                    item_pairs.c.i_id_2,
                )
            )
        ).order_by(
            related_orderlines.c.w_id,
            related_orderlines.c.d_id,
            Order.c_id
        ).with_cte(
            orders,
            orderlines,
            orderlines_2,
            item_pairs,
            related_orderlines,
            related_orderlines_2
        )

        related_customer_list = database.execute(related_customers).fetchall()
        
        print(f"Related Customers: ")
        for i in related_customer_list:
            print(f"    {i}") 
