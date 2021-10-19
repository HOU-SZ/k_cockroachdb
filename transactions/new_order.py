from playhouse.cockroachdb import CockroachDatabase, DatabaseProxy
from decimal import Decimal
from datetime import datetime

from models import *

cockroach_db = CockroachDatabase(
    database='wholesale',
    user='root',
    sslmode='require',
    sslrootcert='..\..\..\Softwares\cockroach\certs\ca.crt',
    sslkey='..\..\..\Softwares\cockroach\certs\client.root.key',
    sslcert='..\..\..\Softwares\cockroach\certs\client.root.crt',
    port=26257,
    host='localhost'
)

database.initialize(cockroach_db)

def draft():
    with database.atomic():
            print("Connection is successfully established")
            print("-------------------------------------")
            Item.delete().where(Item.id > 2).execute()
            query = Item.select()
            res = database.execute(query)
            print(res.fetchall())
            print("-------------------------------------")
            Item.create(id = 3, name = 'I3', price = Decimal(30))
            query = Item.select()
            res = database.execute(query)
            print(res.fetchall())
            print("-------------------------------------")
            query = Item.select().where(Item.price > 10).order_by(Item.id)
            res = database.execute(query)
            print(res.fetchall())


def create_order(cus, num_items, item_number, supplier_warehouse, quantity):
    
    # add order
    order_id = District.get(District.id == cus[1]).next_o_id
    is_local = list(map(lambda x: x == cus[0], supplier_warehouse))
    
    Order.create(
        id = order_id, 
        w_id = cus[0],
        d_id = cus[1],
        c_id = cus[2],
        carrier_id = None,
        ol_cnt = Decimal(num_items),
        all_local = Decimal(all(is_local)),
        entry_d = datetime.utcnow()
    )

    # update district
    District.update(next_o_id = District.next_o_id + 1).where(District.id == cus[1]).execute()

    for i in range(num_items):
        stock = Stock.get(
            Stock.w_id == supplier_warehouse[i], 
            Stock.i_id == item_number[i]
        )
        # update stock
        update_stock(i, stock, quantity[i], is_local[i])
        # create order_line
        create_order_line(i, order_id, stock, cus, item_number[i], supplier_warehouse[i], quantity[i])


def update_stock(i, stock, quantity_i, is_local_i):

    adjusted_qty = stock.quantity - quantity_i

    stock.update(
        quantity = adjusted_qty if adjusted_qty >= 10 else adjusted_qty + 100,
        ytd = stock.ytd + quantity_i,
        order_cnt = stock.order_cnt + 1,
        remote_cnt = stock.remote_cnt + is_local_i
    ).execute()


def create_order_line(i, order_id, stock, cus, item_number_i, supplier_warehouse_i, quantity_i):
    
    item = Item.get(Item.id == item_number_i)

    OrderLine.create(
        number = i + 1,
        o_id = order_id, 
        w_id = cus[0],
        d_id = cus[1],
        i_id = item_number_i,
        supply_w_id = supplier_warehouse_i,
        quantity = quantity_i,
        amount = quantity_i * item.price,
        delivery_d = None,
        dist_info = getattr(stock, f"dist_{cus[1]}")
    )



with database.atomic():
    create_order((1,1,1), 2, [1, 2], [1, 1], [5, 3])
