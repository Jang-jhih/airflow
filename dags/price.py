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


default_args = {
    'owner': 'airflow',
    }

with DAG(
    "Price",
    default_args = default_args,
    description = "Stock price",
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["PTT_Opinion"],
) as dag:
    dag.doc_md = __doc__
    
    def Download_Data():
        tablename = 'price'
        datetime_object = datetime.strptime('20230202', '%Y%m%d')
        df = crawl_price(datetime_object)
        df.to_csv(f'/opt/airflow/tools/{tablename}_tmp.csv')


    def pass_to_psql():
        tablename = 'price'
        df = pd.read_csv(f'/opt/airflow/tools/{tablename}_tmp.csv')
        hook = PostgresHook(postgres_conn_id="_postgresql")
        engine = hook.get_sqlalchemy_engine()
        df.to_sql(tablename, engine, if_exists='append')



    Download_Data = PythonOperator(
        task_id = "Download_Data",
        python_callable = Download_Data
    )


    pass_to_psql = PythonOperator(
        task_id = "pass_to_psql",
        python_callable = pass_to_psql
    )

    Download_Data  >> pass_to_psql