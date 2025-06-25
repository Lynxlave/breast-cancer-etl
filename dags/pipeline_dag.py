from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.trigger_rule import TriggerRule
from etl import evaluate, fetch_data, preprocess, train_model, upload_results

default_args = {
    "owner" : "'Истратова",
    "retries" : 3 ,
    "retry_delay" : timedelta(minutes=5),
    "execution_timeout" : timedelta(minutes=30),
}

with DAG(
    dag_id = "breast_cancer_etl_cloudru",
    description="ETL + ML pipeline + Cloud.ru S3",
    start_date=datetime(2025,6,25),
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    tags = ["Cloud.ru", "ml", "etl"]
) as dag:
    t_fetch = PythonOperator(task_id="fetch_data", python_callable=fetch_data.main, retries=5)
    t_preprocess = PythonOperator(task_id="preprocess", python_callable= preprocess.main)
    t_train_model = PythonOperator(task_id="train_model", python_callable=train_model.main)
    t_evaluate = PythonOperator(task_id="evaluate", python_callable=evaluate.main)
    t_upload_results = PythonOperator(task_id="upload_results", python_callable=upload_results.main, trigger_rule=TriggerRule.ALL_SUCCESS)

    t_fetch >> t_preprocess >> t_train_model >> t_evaluate >> t_upload_results
