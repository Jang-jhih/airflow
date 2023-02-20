import random

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta


default_args = {
    'owner': 'marquez',
    'depends_on_past': False,
    'start_date':datetime(2021, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'email': ['datascience@example.com']
}

dag = DAG(
    'counter',
    default_args = default_args,
    schedule=timedelta(days=1),
    catchup=False,
    description='DAG that generates a new count value between 1-10.'
)

t1 = PostgresOperator(
    task_id='if_not_exists',
    postgres_conn_id='_postgresql',
    sql='''
        DROP TABLE IF EXISTS temp_benchmark_1;
        CREATE TABLE temp_benchmark AS
        SELECT * FROM benchmark
        WHERE date BETWEEN current_date - interval '1 days' AND current_date;

        ''',
    dag=dag
)

t2 = PostgresOperator(
    task_id='inc',
    postgres_conn_id='_postgresql',
    sql='''
        DROP TABLE IF EXISTS temp_benchmark_2;
        CREATE TABLE temp_benchmark AS
        SELECT * FROM benchmark
        WHERE date BETWEEN current_date - interval '1 days' AND current_date;

        ''',
    parameters={
      'value': random.randint(1, 10)
    },
    dag=dag
)

t1 >> t2