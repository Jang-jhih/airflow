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
    'owner': 'airflow',
    }

with DAG(
    "pe",
    default_args = default_args,
    description = "Stock pe",
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["Stock Crawler"],
) as dag:
    dag.doc_md = __doc__
    
    def Download_Data():
        tablename = 'pe'
        datetime_object = datetime.strptime('20230202', '%Y%m%d')
        df = crawl_pe(datetime_object)

        path = os.getcwd()
        df.to_pickle(f'{path}/{tablename}_tmp.pkl')


    def pass_to_psql():
        tablename = 'pe'
        path = os.getcwd()
        df = pd.read_pickle(f'/{path}/{tablename}_tmp.pkl')
        hook = PostgresHook(postgres_conn_id="_postgresql")
        engine = hook.get_sqlalchemy_engine()
        df.to_sql(tablename, engine, if_exists='append', index=False)






    Download_Data = PythonOperator(
        task_id = "Download_Data",
        python_callable = Download_Data
    )


    pass_to_psql = PythonOperator(
        task_id = "pass_to_psql",
        python_callable = pass_to_psql
    )


    Download_Data  >> pass_to_psql