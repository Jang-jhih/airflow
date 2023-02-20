from textwrap import dedent
# from airflow import DAG
from openlineage.airflow import DAG
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
    'depends_on_past': False,
    'start_date': datetime(2023, 2, 18),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    "interest",
    default_args = default_args,
    description = "Stock interest",
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["amundsen_demo"],
) as dag:
    dag.doc_md = __doc__
    
    def Download_Data():
        tablename = 'interest'
        # datetime_object = datetime.strptime('20230202', '%Y%m%d')
        df = interest()


        hook = PostgresHook(postgres_conn_id="_postgresql")
        engine = hook.get_sqlalchemy_engine()

        df.to_sql(tablename, engine, if_exists='append', index=False)





    Download_Data = PythonOperator(
        task_id = "Download_Data",
        python_callable = Download_Data
    )


    Download_Data   