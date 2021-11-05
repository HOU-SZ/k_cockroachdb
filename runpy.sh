#!/bin/bash
server_num=$1
task_type=$2
hostname=${HOSTNAME}

for client in $(seq 0 39)
do
    if [ $(($client % 5)) -eq $server_num ];
    then
        python3 /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64/CS5424_Project_CockroachDB/main_driver.py $client $task_type $hostname >>log.txt &
    fi
done