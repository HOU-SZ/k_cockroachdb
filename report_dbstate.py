from peewee import *
from playhouse.cockroachdb import CockroachDatabase, DatabaseProxy
from decimal import Decimal
from datetime import datetime
import time

from models import *
from transactions import *


def final_state():

    cockroach_db = CockroachDatabase(
        database='wholesale',
        user='root',
        # sslmode='disable',
        sslmode='require',
        sslrootcert='..\..\..\Softwares\cockroach\certs\ca.crt',
        sslkey='..\..\..\Softwares\cockroach\certs\client.root.key',
        sslcert='..\..\..\Softwares\cockroach\certs\client.root.crt',
        port=26257,
        # host='xcnc30.comp.nus.edu.sg',
        host = 'localhost',
        autoconnect=False
    )

    database.initialize(cockroach_db)
    database.connect()

    # w_ytd = Warehouse.select(fn.SUM(Warehouse.ytd))
    # d_ytd = District.select(fn.SUM(District.ytd))
    # d_next_o_id = District.select(fn.SUM(District.next_o_id))
    # c_balance = Customer.select(fn.SUM(Customer.balance))
    # c_ytd_payment = Customer.select(fn.SUM(Customer.ytd_payment))
    # c_payment_cnt = Customer.select(fn.SUM(Customer.payment_cnt))
    # c_delivery_cnt = Customer.select(fn.SUM(Customer.delivery_cnt))
    # o_id = Order.select(fn.MAX(Order.id))
    # o_ol_cnt = Order.select(fn.SUM(Order.ol_cnt))
    # ol_amount = Orderline.select(fn.SUM(Orderline.amount))
    # ol_quantity = Orderline.select(fn.SUM(Orderline.quantity))
    # s_quantity = Stock.select(fn.SUM(Stock.quantity))
    # s_ytd = Stock.select(fn.SUM(Stock.ytd))
    # s_order_cnt = Stock.select(fn.SUM(Stock.order_cnt))
    # s_remote_cnt = Stock.select(fn.SUM(Stock.remote_cnt))

    warehouse = Warehouse.select(fn.SUM(Warehouse.ytd))
    
    district = District.select(
        fn.SUM(District.ytd), 
        fn.SUM(District.next_o_id)
    )
    
    customer = Customer.select(
        fn.SUM(Customer.balance),
        fn.SUM(Customer.ytd_payment),
        fn.SUM(Customer.payment_cnt),
        fn.SUM(Customer.delivery_cnt)
    )
    
    order = Order.select(
        fn.MAX(Order.id),
        fn.SUM(Order.ol_cnt)
    )

    orderline = Orderline.select(
        fn.SUM(Orderline.amount),
        fn.SUM(Orderline.quantity)
    )

    stock = Stock.select(
        fn.SUM(Stock.quantity),
        fn.SUM(Stock.ytd),
        fn.SUM(Stock.order_cnt),
        fn.SUM(Stock.remote_cnt)
    )
    
    output = []
    output.extend([str(i) for i in database.execute(warehouse).fetchall()[0]])
    output.extend([str(i) for i in database.execute(district).fetchall()[0]])
    output.extend([str(i) for i in database.execute(customer).fetchall()[0]])
    output.extend([str(i) for i in database.execute(order).fetchall()[0]])
    output.extend([str(i) for i in database.execute(orderline).fetchall()[0]])
    output.extend([str(i) for i in database.execute(stock).fetchall()[0]])


    
    with open('output/dbstate.csv', 'a+') as f:
        for metric in output:
            print(metric, file=f)


if __name__ == '__main__':
    final_state()