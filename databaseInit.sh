#!/bin/bash

for n in $(seq 30 34)
do
    ssh cs4224k@xcnc$n.comp.nus.edu.sg "sh /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64/test.sh"
done


ssh cs4224k@xcnc30.comp.nus.edu.sg "cd /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64 ; ./cockroach init --insecure --host=xcnc30.comp.nus.edu.sg:26257"


# for n in $(seq 30 34)
# do
#     server_num=(30 31 32 33 34)
#     cur_num=`expr $n-30`
#     unset server_num[$cur_num]
#     ssh cs4224k@xcnc$n.comp.nus.edu.sg "cd /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64 ; \
#     pkill cockroach ; \
#     rm -rf cockroach-data ; \
#     ./cockroach start --insecure --listen-addr=xcnc$n.comp.nus.edu.sg:26257 --http-addr=xcnc$n.comp.nus.edu.sg:3000 --join=xcnc${server_num[0]}.comp.nus.edu.sg:26257,xcnc${server_num[1]}.comp.nus.edu.sg:26257,xcnc${server_num[2]}.comp.nus.edu.sg:26257,xcnc${server_num[3]}.comp.nus.edu.sg:26257 --cache=.25 --max-sql-memory=.25 --background"
#     echo "Database at cs4224k@xcnc$n.comp.nus.edu.sg has started"
# done

# sshpass -p "123456" ssh cs4224k@xcnc$n.comp.nus.edu.sg "cd /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64 ; ./cockroach sql --insecure --host=localhost:26257 --file /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64/db_init.sql"