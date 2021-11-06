#!/bin/bash
task_type=$1
username=$2
hostname_list=($3 $4 $5 $6 $7)
for n in $(seq 0 4)
do
{
    server_num=$n
    sshpass -p "123456" ssh $username@${hostname_list[$n]} "sh /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64/CS5424_Project_CockroachDB/runpy.sh $server_num $task_type"
    echo "Server $username@${hostname_list[$n]} starts..."
} &
done
