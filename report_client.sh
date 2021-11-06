#!/bin/bash
task_type=$1
username=$2
hostname_list=($3 $4 $5 $6 $7)

for n in $(seq 0 4)
do
    ssh $username@${hostname_list[$n]} "cat /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64/task${task_type}.csv" >> result.csv
done

wait

echo "All workload $task_type tasks finish..."