#!/bin/bash
task_type=$1

for n in 30 31 32 34
do
    ssh cs4224k@xcnc$n.comp.nus.edu.sg "cat /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64/task${task_type}.csv" >> result.csv
done

wait

echo "All workload $task_type tasks finish..."