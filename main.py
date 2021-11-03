from playhouse.cockroachdb import CockroachDatabase, DatabaseProxy
from decimal import Decimal
from datetime import datetime
import time

from models import *
from transactions import *

cockroach_db = CockroachDatabase(
    database='supplier',
    user='root',
    sslmode='require',
    sslrootcert='..\..\..\Softwares\cockroach\certs\ca.crt',
    sslkey='..\..\..\Softwares\cockroach\certs\client.root.key',
    sslcert='..\..\..\Softwares\cockroach\certs\client.root.crt',
    port=26257,
    host='localhost',
    autoconnect=False
)

database.initialize(cockroach_db)

database.connect()


start_time = time.time()
# test NewOrderTransaction
# new_order = NewOrderTransaction((1, 1, 1), 2, [3, 1], [1, 2], [3, 6])
# new_order.execute()

# test PaymentTransaction
# payment = PaymentTransaction((1, 1, 1), 6)
# payment.execute()

# test DeliveryTransaction
# delivery = DeliveryTransaction(1, 5)
# delivery.execute()

# test OrderStatusTransaction
order_status = OrderStatusTransaction((1,1,1))
order_status.execute()

# test StockLevelTransaction
# stock_level = StockLevelTransaction(1, 1, 50, 5)
# stock_level.execute()

# test PopularItemTransaction
# popular_item = PopularItemTransaction(1, 1, 20)
# popular_item.execute()

# test TopBanlanceTransaction
# top_customers = TopBanlanceTransaction()
# top_customers.execute()

# test RelatedCustomerTransaction
# related_customer = RelatedCustomerTransaction((1, 1, 1))
# related_customer.execute()

end_time = time.time()
print(f"Run time: {end_time - start_time}\n")


