from textwrap import dedent
from airflow import DAG 
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from datetime import datetime, timedelta
# from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
import csv
from finance.stock import *
import os


default_args = {
    'owner': 'Crawlar',
    }

with DAG(
    "benchmark",
    default_args = default_args,
    description = "",
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["datahub_demo"],
) as dag:
    dag.doc_md = __doc__
    
    def Download_Data():
        tablename = 'benchmark'
        hook = PostgresHook(postgres_conn_id="_postgresql")
        engine = hook.get_sqlalchemy_engine()
        datetime_object = datetime.strptime('20230202', '%Y%m%d')
        dates = date_range(datetime_object, datetime.now())


        for date in dates:
            print(f'Crawlar {date}')
            time.sleep(5)
            df = crawl_benchmark(datetime_object)
            df.to_sql(tablename, engine, if_exists='append', index=False)






    Download_Data = PythonOperator(
        task_id = "Download_Data",
        python_callable = Download_Data
    )


    create_temp_table = PostgresOperator(
        task_id='create_temp_table',
        postgres_conn_id='_postgresql',
        sql="""

        DROP TABLE IF EXISTS temp_benchmark;

        CREATE TABLE temp_benchmark AS
        SELECT * FROM benchmark
        WHERE date BETWEEN current_date - interval '3 days' AND current_date;

        """,
        dag=dag,
    )


    Download_Data  >> create_temp_table



