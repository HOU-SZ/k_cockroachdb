# k_cockroachdb

## 1. Prerequisites

* Using SSH to connect to the servers

  ```sh
  ### for each server
  ssh <user_name>@<hostname>

  ### for example
  ### access server "xcnc30"
  ssh cs4224k@xcnc30.comp.nus.edu.sg
  
  ### access server "xcnc31"
  ssh cs4224k@xcnc31.comp.nus.edu.sg
  
  ### ...
  ```

* Install CockroachDB binary on 5 server

  ```sh
  ### for each server
  mkdir /temp/cs5424_team_k
  cd /temp/cs5424_team_k
  curl https://binaries.cockroachdb.com/cockroach-v21.1.7.linux-amd64.tgz | tar -xz
  ```

* Install Python package on 5 server

  ```sh
  ### for each server
  pip3 install --user --upgrade pip
  pip3 install --user psycopg2-binary
  pip3 install --user peewee
  ```

* Copy project code to 5 servers

  ```sh
  ### copy code to 5 servers (k_cockroachdb.zip is the source code zip, if the name of the source zip is different, please change accordingly. And also please change <user_name> and <hostname_1> accordingly)
  scp k_cockroachdb.zip <user_name>@<hostname_1>:/temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64
  scp k_cockroachdb.zip <user_name>@<hostname_2>:/temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64
  scp k_cockroachdb.zip <user_name>@<hostname_3>:/temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64
  scp k_cockroachdb.zip <user_name>@<hostname_4>:/temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64
  scp k_cockroachdb.zip <user_name>@<hostname_5>:/temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64
  
  ### run following command on each of the 5 server nodes
  cd /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64
  unzip -o -d . k_cockroachdb.zip
  ```

* Download data

  ```sh
  ### for each server
  cd /temp/cs5424_team_k
  wget http://www.comp.nus.edu.sg/~<user_name>/project_files_4.zip
  unzip -o -d . project_files_4.zip
  ```





## 2. Get Started

### ① Start Cluster

> If you want to kill all the cockroach process, run `pkill cockroach` 
>
> If you want to kill the certain process, run `kill -9 <PID>` 

* Node 1

  ```sh
  cd /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64
  ./cockroach start --insecure --listen-addr=<hostname_1>:26257 --http-addr=<hostname_1>:3000 --join=<hostname_2>:26257,<hostname_3>:26257,<hostname_4>:26257,<hostname_5> --cache=.35 --max-sql-memory=.35 --background
  ```

* Node2

  ```sh
  cd /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64
  ./cockroach start --insecure --listen-addr=<hostname_2>:26257 --http-addr=<hostname_2>:3000 --join=<hostname_1>:26257,<hostname_3>:26257,<hostname_4>:26257,<hostname_5> --cache=.35 --max-sql-memory=.35 --background
  ```

* Node3

  ```sh
  cd /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64
  ./cockroach start --insecure --listen-addr=<hostname_3>:26257 --http-addr=<hostname_3>:3000 --join=<hostname_1>:26257,<hostname_2>:26257,<hostname_4>:26257,<hostname_5> --cache=.35 --max-sql-memory=.35 --background
  ```

* Node4

  ```sh
  cd /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64
  ./cockroach start --insecure --listen-addr=<hostname_4>:26257 --http-addr=<hostname_4>:3000 --join=<hostname_1>:26257,<hostname_2>:26257,<hostname_3>:26257,<hostname_5> --cache=.35 --max-sql-memory=.35 --background
  ```

* Node5

  ```sh
  cd /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64
  ./cockroach start --insecure --listen-addr=<hostname_5> --http-addr=<hostname_5>:3000 --join=<hostname_1>:26257,<hostname_2>:26257,<hostname_3>:26257,<hostname_4>:26257 --cache=.35 --max-sql-memory=.35 --background
  ```



### ② Init Cluster

> You can init cluster on any node among 1 to 5, the following example is on node1
>
> If the cluster has already been initialized, you can skip this step. The above `cockroach start` command can help you restart the cluster.

* Node 1

  ```sh
  cd /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64
  ./cockroach init --insecure --host=<hostname_1>:26257
  ```



### ③ Test Cluster 

* Check cluster info

  ```sh
  grep 'cluster' cockroach-data/logs/cockroach.log -A 11
  ```

* Check cluster status

  ```sh
  cd /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64
  ./cockroach node status --insecure --host=<hostname_1>:26257
  ```

* Check Cockroach database

  ```sh
  cd /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64
  ./cockroach sql --insecure --host=<hostname_1>:26257
  ```





## 3. Load data into Database

* Preparation

  ```sh
  ### for any one server
  ### ssh <user_name>@<hostname>
  cd /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64
  mkdir cockroach-data/extern
  cp ../project_files_4/data_files/* ./cockroach-data/extern/
  ```

* Init Database & Load data

  ```sh
  ### on the server used in the previous command
  cd /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64
  ./cockroach sql --insecure --host=<hostname_1>:26257 --file ./k_cockroachdb/db_init.sql
  ```





## 4. Run Transaction files

* Prepare

  ```sh
  ssh <user_name>@<hostname_1> "mkdir /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64/output"
  ssh <user_name>@<hostname_2> "mkdir /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64/output"
  ssh <user_name>@<hostname_3> "mkdir /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64/output"
  ssh <user_name>@<hostname_4> "mkdir /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64/output"
  ssh <user_name>@<hostname_5> "mkdir /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64/output"
  ```

* Run

  * Run script on local machine

  ```sh
  cd k_cockroachdb
  ./entry.sh <task_type> <user_name> <hostname_1> <hostname_2> <hostname_3> <hostname_4> <hostname_5>
  ### for example
  ### run workload A
  ./entry.sh A cs4224k xcnc30.comp.nus.edu.sg xcnc31.comp.nus.edu.sg xcnc32.comp.nus.edu.sg xcnc33.comp.nus.edu.sg xcnc34.comp.nus.edu.sg
  ### run workload B
  ./entry.sh B cs4224k xcnc30.comp.nus.edu.sg xcnc31.comp.nus.edu.sg xcnc32.comp.nus.edu.sg xcnc33.comp.nus.edu.sg xcnc34.comp.nus.edu.sg
  ```

  *  Or run manual (run the following commands on 5 servers)

  ```sh
  ### for each server
  cd /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64/k_cockroachdb
  sh runpy.sh <server_num> <task_type>
  ### for example
  ### on server node 1
  sh runpy.sh 0 A
  sh runpy.sh 0 B
  ### on server node 2
  sh runpy.sh 1 A
  sh runpy.sh 1 B
  ### on server node 3
  sh runpy.sh 2 A
  sh runpy.sh 2 B
  ### on server node 4
  sh runpy.sh 3 A
  sh runpy.sh 3 B
  ### on server node 5
  sh runpy.sh 4 A
  sh runpy.sh 4 B
  ```

* Get statistics csv file

  ```sh
  cd /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64/k_cockroachdb
  ### get client.csv
  ./report_client.sh A <user_name> <hostname_1> <hostname_2> <hostname_3> <hostname_4> <hostname_5>
  ./report_client.sh B <user_name> <hostname_1> <hostname_2> <hostname_3> <hostname_4> <hostname_5>
  ### get dbstate.csv
  python3 report_dbstate.py
  ### get throughput.csv
  python3 report_throughput.py <task_type>
  ```

  

