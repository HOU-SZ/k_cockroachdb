from playhouse.cockroachdb import CockroachDatabase, DatabaseProxy
from decimal import Decimal
from datetime import datetime

from models import *
from transactions import *

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


### test NewOrderTransaction
new_order = NewOrderTransaction((1,1,1), 2, [1, 2], [1, 1], [5, 3])
new_order.execute()

### test DeliveryTransaction
# delivery = DeliveryTransaction(1, 2)
# delivery.execute()

### test OrderStatusTransaction
# order_status = OrderStatusTransaction((1,1,1))
# order.execute()