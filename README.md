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

* Node 1(xcnc30)

  > Any node among 1 to 5 is ok

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

### ① Preparation

```sh
### ssh cs4224k@xcnc.comp.nus.edu.sg
cd /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64
mkdir cockroach-data/extern
cp ../project_files_4/data_files/* ./cockroach-data/extern/
```



### ② Init Database & Load data

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

  ```sh
  cd /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64/CS5424_Project_CockroachDB
  ### run workload A
  sh entry.sh A
  ### run workload B
  sh entry.sh A
  ```

* Get statistics csv file

  ```sh
  cd /temp/cs5424_team_k/cockroach-v21.1.7.linux-amd64/CS5424_Project_CockroachDB
  ### get dbstate.csv
  python3 report_dbstate.py
  ### get throughput.csv
  python3 report_throughput.py
  ```

  

