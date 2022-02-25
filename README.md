# airflow-dags
Airflow repository for storing dag files to deploy mock project

### 1. Install WSL on Windows
Airflow is not supported for Windows OS so we must use WSL to locally install. </br>
Find <strong>Turn Windows features on or off</strong> and enable <strong>Window Subsystem for Linux</strong> </br>
Install <strong>Ubuntu</strong> from Windows Store (or any kernel you want) </br>
### 2. Install Aiflow
Access super user mode: `sudo su` and provide the password for super user </br>
Run following commands:

    
    apt-get update
    apt-get upgrade
    apt-get install python-pip
    
    
Then install Airflow using pip:


    pip install apache-airflow
    
    
To make sure Airflow was installed, run this command: `pip list` and find the package.
Start Airflow:


    airflow db init
    airflow webserver
    airflow scheduler
    
    
The Web UI will run default on [localhost:8080](localhost:8080)
### 3. Install Apache Spark Providers package
In order to use `SparkSubmitOperator` and create connection to Spark we have to install Apache Spark Providers package </br>
Run this command: `pip install apache-airflow-providers-apache-spark`
### 4. Install Java
`SparkSubmitOperator` triggers Spark Jobs by using `spark-submit` command on Spark, so that we need to install JVM for Spark to run. </br>
Run following commands:


    apt install openjdk-8-jdk -y
    echo 'JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64"' | sudo tee -a /etc/environment
    source /etc/environment
    
    
To make sure Airflow was installed, run this command: `cat /etc/environment | grep JAVA` it should return `JAVA_HOME` value.
### 5. Create spark connection on Airflow
In Airflow Web UI: </br>
<strong>Admin >> Connections >> +</strong> </br>
Select <strong>Connection type</strong> is <strong>Spark</strong> </br>
Fill <strong>Host</strong> field: `local[*]` if you want to run Spark locally, otherwise fill in the IP of the Spark Master (e.g. `spark://172.21.168.1:7077`)
### 6. Write DAGs
Write the DAGs and put them in Airflow dags folder. This folder's path can be modify in `airflow.cfg` through `dags_folder` 
### 7. Testing and deployment
To connect to MySQL you will need `mysql-connector-java.jar` file, make sure you have the compatible version. </br>
The dags ending with `source_to_dl` and `dl_to_db` is for unit testing
The 3 dags ending with `source_to_dl_to_db` is for integration test and deployment.
