import sys
import time
import csv
import numpy as np
from playhouse.cockroachdb import CockroachDatabase
from decimal import Decimal
from datetime import datetime
import logging
import traceback

from models import *
from transactions import *

import time

logging.basicConfig(filename='/temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64/task.log',
                    level=logging.INFO, filemode='a')


def execute_client(client_number, workload_type, hostname):
    try:
        cockroach_db = CockroachDatabase(
            database='wholesale',
            user='root',
            sslmode='disable',
            port=26257,
            host=str(hostname),
            autoconnect=False
        )

        database.initialize(cockroach_db)
        database.connect()
    except:
        print('Error database connect')
        logging.error('Database connection: ' + traceback.format_exc())

    # input_data = sys.stdin.readlines()
    path = '/temp/cs5424_team_k/project_files_4/xact_files_' + \
        workload_type.upper() + '/' + client_number + '.txt'
    latency_list = []
    number_of_executed_trans = 0

    # record fail transactions
    counter = 0

    def extract(one_string):
        st = one_string.strip().split(",")
        return [x.strip() for x in st]

    try:
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
                    try:
                        transaction = NewOrderTransaction(
                            (w_id, d_id, c_id), num_items, item_number, supplier_warehouse, quantity)
                        transaction.execute()
                        logging.info(str(line))
                    except:
                        counter += 1
                        print("Error transaction: " + str(line))
                        logging.error(
                            "Transaction execute: " + str(line) + " [DETAILS] " + traceback.format_exc())
                    finally:
                        latency_list.append(time.time() - start_time)

                elif x_type == "P":
                    c_w_id = int(line[1])
                    c_d_id = int(line[2])
                    c_id = int(line[3])
                    payment_num = Decimal(line[4])
                    try:
                        transaction = PaymentTransaction(
                            (c_w_id, c_d_id, c_id), payment_num)
                        transaction.execute()
                        logging.info(str(line))
                    except:
                        counter += 1
                        print("Error transaction: " + str(line))
                        logging.error(
                            "Transaction execute: " + str(line) + " [DETAILS] " + traceback.format_exc())
                    finally:
                        latency_list.append(time.time() - start_time)

                elif x_type == "D":
                    w_id = int(line[1])
                    carrier_id = int(line[2])
                    try:
                        transaction = DeliveryTransaction(w_id, carrier_id)
                        transaction.execute()
                        logging.info(str(line))
                    except:
                        counter += 1
                        print("Error transaction: " + str(line))
                        logging.error(
                            "Transaction execute: " + str(line) + " [DETAILS] " + traceback.format_exc())
                    finally:
                        latency_list.append(time.time() - start_time)

                elif x_type == "O":
                    c_w_id = int(line[1])
                    c_d_id = int(line[2])
                    c_id = int(line[3])
                    try:
                        transaction = OrderStatusTransaction(
                            (c_w_id, c_d_id, c_id))
                        transaction.execute()
                        logging.info(str(line))
                    except:
                        counter += 1
                        print("Error transaction: " + str(line))
                        logging.error(
                            "Transaction execute: " + str(line) + " [DETAILS] " + traceback.format_exc())
                    finally:
                        latency_list.append(time.time() - start_time)

                elif x_type == "S":
                    w_id = int(line[1])
                    d_id = int(line[2])
                    t = int(line[3])
                    limit = int(line[4])
                    try:
                        transaction = StockLevelTransaction(
                            w_id, d_id, t, limit)
                        transaction.execute()
                        logging.info(str(line))
                    except:
                        counter += 1
                        print("Error transaction: " + str(line))
                        logging.error(
                            "Transaction execute: " + str(line) + " [DETAILS] " + traceback.format_exc())
                    finally:
                        latency_list.append(time.time() - start_time)

                elif x_type == "I":
                    w_id = int(line[1])
                    d_id = int(line[2])
                    limit = int(line[3])
                    try:
                        transaction = PopularItemTransaction(w_id, d_id, limit)
                        transaction.execute()
                        logging.info(str(line))
                    except:
                        counter += 1
                        print("Error transaction: " + str(line))
                        logging.error(
                            "Transaction execute: " + str(line) + " [DETAILS] " + traceback.format_exc())
                    finally:
                        latency_list.append(time.time() - start_time)

                elif x_type == "T":
                    try:
                        transaction = TopBanlanceTransaction()
                        transaction.execute()
                        logging.info(str(line))
                    except:
                        counter += 1
                        print("Error transaction: " + str(line))
                        logging.error(
                            "Transaction execute: " + str(line) + " [DETAILS] " + traceback.format_exc())
                    finally:
                        latency_list.append(time.time() - start_time)

                elif x_type == "R":
                    c_w_id = int(line[1])
                    c_d_id = int(line[2])
                    c_id = int(line[3])
                    try:
                        transaction = RelatedCustomerTransaction(
                            (c_w_id, c_d_id, c_id))
                        transaction.execute()
                        logging.info(str(line))
                    except:
                        counter += 1
                        print("Error transaction: " + str(line))
                        logging.error(
                            "Transaction execute: " + str(line) + " [DETAILS] " + traceback.format_exc())
                    finally:
                        latency_list.append(time.time() - start_time)
                else:
                    print(
                        "Invalid transaction type: %s "
                        "[If you can't see invalid type letter, "
                        "this means there is one or more empty line(s) in your input.]" % x_type
                    )
                    logging.error(
                        "Invalid transaction type: %s "
                        "[If you can't see invalid type letter, "
                        "this means there is one or more empty line(s) in your input.]" % x_type
                    )

                    continue
    except:
        print('Error xact_file')
        logging.error('Error xact_file: ' + traceback.format_exc())

    # 7 measurements
    try:
        number_of_executed_trans = len(latency_list) - counter
        latency_array = np.array(latency_list)
        total_latency = np.sum(latency_array)  # sec
        throughput = number_of_executed_trans / total_latency
        avr_latency = np.mean(latency_array) * 1000  # ms
        median_latency = np.median(latency_array) * 1000
        percentile_95 = np.percentile(latency_array, 95) * 1000
        percentile_99 = np.percentile(latency_array, 99) * 1000

        result = [client_number, number_of_executed_trans, total_latency,
                  throughput, avr_latency, median_latency, percentile_95, percentile_99]
        print(result)
        output_string = ",".join([str(x) for x in result])
        logging.info("Final result: " + output_string)
    except:
        print('Error measurement')
        logging.error('Measurement: ' + traceback.format_exc())

    try:
        with open('/temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64/task{}.csv'.format(workload_type), 'a+') as f:
            print(output_string, file=f)
        print(output_string)
        # return output_string
        logging.info('success:' + output_string)
    except:
        print('Error write csv')
        logging.error('Write csv: ' + traceback.format_exc())


if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) < 3:
        sys.exit('Please type the correct args: client_number workload_type')
    client_number = sys.argv[1]
    workload_type = sys.argv[2]
    host_name = sys.argv[3]
    try:
        execute_client(client_number, workload_type, host_name)
    except:
        logging.error('Execute_client: ' + client_number +
                      workload_type + '[DETAILS]' + traceback.format_exc())
