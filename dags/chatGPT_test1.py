from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 2, 18),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'example_postgres_operator',
    default_args=default_args,
    schedule_interval=timedelta(weeks=1),
)

create_temp_table = PostgresOperator(
    task_id='create_temp_table',
    postgres_conn_id='_postgresql',
    sql="""CREATE TEMP TABLE my_temp_table AS
           SELECT * FROM price
           WHERE date >= '{{ ds }}' AND date < '{{ next_ds }}';
        """,
    dag=dag,
)

create_temp_table
