# CS5424_Project_CockroachDB

## 1. Prerequisites

* Using SSH to connect to the server

  ```sh
  ### access server "xcnc30"
  ssh cs4224k@xcnc30.comp.nus.edu.sg
  
  ### access server "xcnc31"
  ssh cs4224k@xcnc31.comp.nus.edu.sg
  
  ### ...
  ```

* Install CockroachDB binary on 5 server

  ```sh
  mkdir /temp/cs5424_team_k
  cd /temp/cs5424_team_k
  curl https://binaries.cockroachdb.com/cockroach-v21.1.7.linux-amd64.tgz | tar -xz
  ```

* Install Python package on 5 server

  ```sh
  pip3 install --user --upgrade pip
  pip3 install --user psycopg2-binary
  pip3 install --user peewee
  ```

* Copy project code to 5 servers

  ```sh
  ### copy code to 5 servers
  scp CS5424_Project_CockroachDB.zip cs4224k@xcnc30.comp.nus.edu.sg:/temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64
  scp CS5424_Project_CockroachDB.zip cs4224k@xcnc31.comp.nus.edu.sg:/temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64
  scp CS5424_Project_CockroachDB.zip cs4224k@xcnc32.comp.nus.edu.sg:/temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64
  scp CS5424_Project_CockroachDB.zip cs4224k@xcnc33.comp.nus.edu.sg:/temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64
  scp CS5424_Project_CockroachDB.zip cs4224k@xcnc34.comp.nus.edu.sg:/temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64
  
  ### run following command on each of the 5 server nodes
  cd /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64
  unzip -o -d . CS5424_Project_CockroachDB.zip
  ```

* Download data

  ```sh
  cd /temp/cs5424_team_k
  wget http://www.comp.nus.edu.sg/~cs4224/project_files_4.zip
  unzip -o -d . project_files_4.zip
  ```





## 2. Get Started

### ① Start Cluster

> If you want to kill all the cockroach process, run `pkill cockroach` 
>
> If you want to kill the certain process, run `kill -9 <PID>` 

* Node 1(xcnc30)

  ```sh
  cd /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64
  ./cockroach start --insecure --listen-addr=xcnc30.comp.nus.edu.sg:26257 --http-addr=xcnc30.comp.nus.edu.sg:3000 --join=xcnc31.comp.nus.edu.sg:26257,xcnc32.comp.nus.edu.sg:26257,xcnc33.comp.nus.edu.sg:26257,xcnc34.comp.nus.edu.sg:26257 --cache=.25 --max-sql-memory=.25 --background
  ```

* Node2 (xcnc31)

  ```sh
  cd /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64
  ./cockroach start --insecure --listen-addr=xcnc31.comp.nus.edu.sg:26257 --http-addr=xcnc31.comp.nus.edu.sg:3000 --join=xcnc30.comp.nus.edu.sg:26257,xcnc32.comp.nus.edu.sg:26257,xcnc33.comp.nus.edu.sg:26257,xcnc34.comp.nus.edu.sg:26257 --cache=.25 --max-sql-memory=.25 --background
  ```

* Node3 (xcnc32)

  ```sh
  cd /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64
  ./cockroach start --insecure --listen-addr=xcnc32.comp.nus.edu.sg:26257 --http-addr=xcnc32.comp.nus.edu.sg:3000 --join=xcnc30.comp.nus.edu.sg:26257,xcnc31.comp.nus.edu.sg:26257,xcnc33.comp.nus.edu.sg:26257,xcnc34.comp.nus.edu.sg:26257 --cache=.25 --max-sql-memory=.25 --background
  ```

* Node4 (xcnc33)

  ```sh
  cd /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64
  ./cockroach start --insecure --listen-addr=xcnc33.comp.nus.edu.sg:26257 --http-addr=xcnc33.comp.nus.edu.sg:3000 --join=xcnc30.comp.nus.edu.sg:26257,xcnc31.comp.nus.edu.sg:26257,xcnc32.comp.nus.edu.sg:26257,xcnc34.comp.nus.edu.sg:26257 --cache=.25 --max-sql-memory=.25 --background
  ```

* Node5 (xcnc34)

  ```sh
  cd /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64
  ./cockroach start --insecure --listen-addr=xcnc34.comp.nus.edu.sg:26257 --http-addr=xcnc34.comp.nus.edu.sg:3000 --join=xcnc30.comp.nus.edu.sg:26257,xcnc31.comp.nus.edu.sg:26257,xcnc32.comp.nus.edu.sg:26257,xcnc33.comp.nus.edu.sg:26257 --cache=.25 --max-sql-memory=.25 --background
  ```



### ② Init Cluster

> You can init cluster on any node among 1 to 5, the following example is on node1 (xcnc30)
>
> If the cluster has already been initialized, you can skip this step. The above `cockroach start` command can help you restart the cluster.

* Node 1(xcnc30)

  ```sh
  cd /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64
  ./cockroach init --insecure --host=xcnc30.comp.nus.edu.sg:26257
  ```



### ③ Test Cluster 

* Check cluster info

  ```sh
  grep 'cluster' cockroach-data/logs/cockroach.log -A 11
  ```

* Check cluster status

  ```sh
  cd /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64
  ./cockroach node status --insecure --host=xcnc30.comp.nus.edu.sg:26257
  ```

* Check Cockroach database

  ```sh
  cd /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64
  ./cockroach sql --insecure --host=xcnc30.comp.nus.edu.sg:26257
  ```





## 3. Load data into Database

* Preparation

  ```sh
  ### ssh cs4224k@xcnc.comp.nus.edu.sg
  cd /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64
  mkdir cockroach-data/extern
  cp ../project_files_4/data_files/* ./cockroach-data/extern/
  ```

* Init Database & Load data

  ```sh
  cd /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64
  ./cockroach sql --insecure --host=xcnc30.comp.nus.edu.sg:26257 --file ./CS5424_Project_CockroachDB/db_init.sql
  ```





## 4. Run Transaction files

* Prepare

  ```sh
  ssh cs4224@xcnc30.comp.nus.edu.sg "mkdir /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64/output"
  ssh cs4224@xcnc31.comp.nus.edu.sg "mkdir /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64/output"
  ssh cs4224@xcnc32.comp.nus.edu.sg "mkdir /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64/output"
  ssh cs4224@xcnc33.comp.nus.edu.sg "mkdir /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64/output"
  ssh cs4224@xcnc34.comp.nus.edu.sg "mkdir /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64/output"
  ```

* Run

  * Run script on local machine

  ```sh
  cd CS5424_Project_CockroachDB
  ./entry.sh <task_type> <user_name> <hostname_1> <hostname_2> <hostname_3> <hostname_4> <hostname_5>
  ### run workload A
  ./entry.sh A cs4224k xcnc30.comp.nus.edu.sg xcnc31.comp.nus.edu.sg xcnc32.comp.nus.edu.sg xcnc33.comp.nus.edu.sg xcnc34.comp.nus.edu.sg
  ### run workload B
  ./entry.sh B cs4224k xcnc30.comp.nus.edu.sg xcnc31.comp.nus.edu.sg xcnc32.comp.nus.edu.sg xcnc33.comp.nus.edu.sg xcnc34.comp.nus.edu.sg
  ```

  *  Or run manual (run the following commands on 5 servers)

  ```sh
  cd /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64/CS5424_Project_CockroachDB
  sh runpy.sh <task_type> <hostname>
  ### on server node 1
  sh runpy.sh 0 A xcnc30.comp.nus.edu.sg
  sh runpy.sh 0 B xcnc30.comp.nus.edu.sg
  ### on server node 2
  sh runpy.sh 1 A xcnc31.comp.nus.edu.sg
  sh runpy.sh 1 B xcnc31.comp.nus.edu.sg
  ### on server node 3
  sh runpy.sh 2 A xcnc32.comp.nus.edu.sg
  sh runpy.sh 2 B xcnc32.comp.nus.edu.sg
  ### on server node 4
  sh runpy.sh 3 A xcnc33.comp.nus.edu.sg
  sh runpy.sh 3 B xcnc33.comp.nus.edu.sg
  ### on server node 5
  sh runpy.sh 4 A xcnc34.comp.nus.edu.sg
  sh runpy.sh 4 B xcnc34.comp.nus.edu.sg
  ```

* Get statistics csv file

  ```sh
  cd /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64/CS5424_Project_CockroachDB
  ### get client.csv
  sh report_client.sh A
  sh report_client.sh B
  ### get dbstate.csv
  python3 report_dbstate.py
  ### get throughput.csv
  python3 report_throughput.py
  ```

  

