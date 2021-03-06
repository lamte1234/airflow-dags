import airflow
from airflow import DAG

from datetime import datetime, timedelta

from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.bash_operator import BashOperator
from airflow.sensors.time_delta import TimeDeltaSensor

default_args = {
    "owner": "airflow",
    "start_date": datetime(2021, 11, 1),
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

with DAG("user_source_to_dl_to_db", schedule_interval="@daily", default_args=default_args, catchup=True) as dag:
	task_1 = SparkSubmitOperator(
		task_id = "task_1",
		application= "/mnt/c/airflow/jars/mockproject_2.12-0.1.jar",
		conn_id = "spark_conn_local",
		java_class="markettingtask.UsersSyncToDL",
		application_args = ["{{ macros.ds_add(ds, -1) }}"] ## or some random day watev
	)


	task_2 = SparkSubmitOperator(
		task_id = "task_2",
		application= "/mnt/c/airflow/jars/mockproject_2.12-0.1.jar",
		conn_id = "spark_conn_local",
		java_class="markettingtask.Demographic",
		application_args = ["{{ macros.ds_add(ds, -1) }}"] ## or some random day watev
	)

	# task_2 = BashOperator(
	# 	task_id = "task_2",
	# 	bash_command = 'echo "{{ macros.ds_add(ds, -1) }}"'
	# )

	# ## waiting for finishing spark job
	# sensor_1 = TimeDeltaSensor(
	# 	task_id = "sensor_1",
	# 	delta = timedelta(minutes=5)
	# )

	task_1 >> task_2

 	## More information:
 	## https://airflow.apache.org/docs/apache-airflow-providers-apache-spark/stable/_modules/airflow/providers/apache/spark/operators/spark_submit.html#SparkSubmitOperator.template_fields