import csv
import sys


def main(workload_type):
    throughputs = []
    with open('output/dbstate.csv') as f:
        f_csv = csv.reader(f)

        for row in f_csv:
            throughputs.append(float(row[3]))

    min_throughput = min(throughputs)
    max_throughput = max(throughputs)
    avg_throughput = sum(throughputs)/(len(throughputs))

    result = [min_throughput, max_throughput, avg_throughput]
    print(result)
    output_string = ",".join([str(x) for x in result])
    with open('output/throughputs_{}.csv'.format(workload_type), 'a') as f:
        print(output_string, file=f)


if __name__ == '__main__':
    workload_type = sys.argv[1]
    main(workload_type)
