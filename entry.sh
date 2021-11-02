#!/bin/bash

task_type=$1

for n in $(seq 30 34)
do
    server_num=$(($n-30))
    echo "Server cs4224k@xcnc$n starts..."
    ssh cs4224k@xcnc$n.comp.nus.edu.sg "sh /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64/CS5424_Project_CockroachDB/runpy.sh $server_num $task_type"
    echo "Server cs4224k@xcnc$n started..." &
done
wait

for n in $(seq 30 34)
do
    ssh cs4224k@xcnc$n.comp.nus.edu.sg "cat /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64/output/task${task_type}.csv" >> result.csv
done

wait

echo "All workload $task_type tasks finish..."