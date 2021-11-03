import sys
import time
import csv
import numpy as np
from playhouse.cockroachdb import CockroachDatabase, DatabaseProxy
from decimal import Decimal
from datetime import datetime

from models import *
from transactions import *

import time
import threading


def main(client_number, workload_type):

    cockroach_db = CockroachDatabase(
        database='wholesale',
        user='root',
        sslmode='disable',
        # sslmode='require',
        # sslrootcert='..\..\..\Softwares\cockroach\certs\ca.crt',
        # sslkey='..\..\..\Softwares\cockroach\certs\client.root.key',
        # sslcert='..\..\..\Softwares\cockroach\certs\client.root.crt',
        port=26257,
        host='localhost'
    )

    database.initialize(cockroach_db)

    # input_data = sys.stdin.readlines()
    path = '/temp/cs5424_team_k/project_files_4/xact_files_' + \
        workload_type.upper() + '/' + client_number + '.txt'
    latency_list = []
    number_of_executed_trans = 0
    l = 0

    counter = 0

    def extract(one_string):
        st = one_string.strip().split(",")
        return [x.strip() for x in st]

    with open(path) as xact_file:
        while True:
            line = xact_file.readline()
            if not line:
                break
            line = extract(line)
            x_type = line[0]
            start_time = time.time()

            # different transaction
            if x_type == "N":
                c_id = int(line[1])
                w_id = int(line[2])
                d_id = int(line[3])
                num_items = int(line[4])
                item_number, supplier_warehouse, quantity = [], [], []
                for _ in range(num_items):
                    line = xact_file.readline()
                    item_info = extract(line)
                    item_number.append(int(item_info[0]))
                    supplier_warehouse.append(int(item_info[1]))
                    quantity.append(int(item_info[2]))
                # execute transaction:
                transaction = NewOrderTransaction(
                    (w_id, d_id, c_id), num_items, item_number, supplier_warehouse, quantity)
                transaction.execute()

            elif x_type == "P":
                c_w_id = int(line[1])
                c_d_id = int(line[2])
                c_id = int(line[3])
                payment_num = Decimal(line[4])
                transaction = PaymentTransaction(
                    (c_w_id, c_d_id, c_id), payment_num)
                transaction.execute()

            elif x_type == "D":
                w_id = int(line[1])
                carrier_id = int(line[2])
                transaction = DeliveryTransaction(w_id, carrier_id)
                transaction.execute()

            elif x_type == "O":
                c_w_id = int(line[1])
                c_d_id = int(line[2])
                c_id = int(line[3])
                transaction = OrderStatusTransaction((c_w_id, c_d_id, c_id))
                transaction.execute()

            elif x_type == "S":
                w_id = int(line[1])
                d_id = int(line[2])
                t = int(line[3])
                limit = int(line[4])
                transaction = StockLevelTransaction(w_id, d_id, t, limit)
                transaction.execute()

            elif x_type == "I":
                w_id = int(line[1])
                d_id = int(line[2])
                limit = int(line[3])
                transaction = PopularItemTransaction(w_id, d_id, limit)
                transaction.execute()

            elif x_type == "T":
                transaction = TopBanlanceTransaction()
                transaction.execute()

            elif x_type == "R":
                c_w_id = int(line[1])
                c_d_id = int(line[2])
                c_id = int(line[3])
                transaction = RelatedCustomerTransaction((c_w_id, c_d_id, c_id))
                transaction.execute()
            else:
                raise Exception(
                    "Invalid transaction type: %s [If you can't see invalid type letter, this means there is one or more empty line(s) in your input.]" % x_type)

            latency_list.append(time.time() - start_time)
            number_of_executed_trans += 1

    # 7 measurements
    latency_array = np.array(latency_list)
    total_latency = np.sum(latency_array)  # sec
    throughput = number_of_executed_trans / total_latency
    avr_latency = np.mean(latency_array) * 1000  # ms
    median_latency = np.median(latency_array) * 1000
    percentile_95 = np.percentile(latency_array, 95) * 1000
    percentile_99 = np.percentile(latency_array, 99) * 1000

    result = [sys.argv[1], number_of_executed_trans, total_latency,
              throughput, avr_latency, median_latency, percentile_95, percentile_99]

    with open('/temp/cs5424_team_k/cockroach/cockroach-v21.1.7.linux-amd64/task{}.csv'.format(sys.argv[2]), 'a+') as f:
        writer = csv.writer(f)
        writer.writerow(result)
    output_string = ",".join(result)
    print(output_string)
    return output_string


if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) < 3:
        sys.exit('Please type the correct args: client_number workload_type')
    client_number = sys.argv[1]
    workload_type = sys.argv[2]
    main(client_number, workload_type)
