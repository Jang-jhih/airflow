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
    'owner': 'airflow',
    }

with DAG(
    "interest",
    default_args = default_args,
    description = "Stock interest",
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["Stock Crawler"],
) as dag:
    dag.doc_md = __doc__
    
    def Download_Data():
        tablename = 'interest'
        # datetime_object = datetime.strptime('20230202', '%Y%m%d')
        df = interest()
        df.reset_index(inplace = True)
        path = os.getcwd()
        df.to_csv(f'{path}/{tablename}_tmp.csv')


    def pass_to_psql():
        tablename = 'interest'
        path = os.getcwd()
        df = pd.read_csv(f'/{path}/{tablename}_tmp.csv')
        hook = PostgresHook(postgres_conn_id="_postgresql")
        engine = hook.get_sqlalchemy_engine()

        df.to_sql(tablename, engine, if_exists='append')



    # create_database = PostgresOperator(
    #         task_id="create_database",
    #         postgres_conn_id="_postgresql",
    #         sql="""
    #             CREATE DATABASE  stock;
    #           """
    # )


    Download_Data = PythonOperator(
        task_id = "Download_Data",
        python_callable = Download_Data
    )


    pass_to_psql = PythonOperator(
        task_id = "pass_to_psql",
        python_callable = pass_to_psql
    )

    # create_database >> 
    Download_Data  >> pass_to_psql