from peewee import *
from playhouse.cockroachdb import CockroachDatabase
import sys

from models import *
from transactions import *


def final_state(hostname):

    cockroach_db = CockroachDatabase(
        database='wholesale',
        user='root',
        sslmode='disable',
        port=26257,
        host=hostname,
        autoconnect=False
    )

    database.initialize(cockroach_db)
    database.connect()

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


    
    with open('/temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64/output/dbstate.csv', 'a+') as f:
        for metric in output:
            print(metric, file=f)


if __name__ == '__main__':
    hostname = sys.argv[1]
    final_state(hostname)