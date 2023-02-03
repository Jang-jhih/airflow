from textwrap import dedent
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from datetime import datetime, timedelta
from airflow.providers.mysql.hooks.mysql import MySqlHook

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


    def pass_to_Neo4j():
        tablename = 'price'
        df = pd.read_csv(f'/opt/airflow/tools/{tablename}_tmp.csv')
        mysql = MySqlHook(mysql_conn_id="mysqlid")
        conn = mysql.get_conn()
        cursor = conn.cursor()


        cursor = db.cursor()

    Download_Data = PythonOperator(
        task_id = "Download_Data",
        python_callable = Download_Data
    )


    pass_to_Neo4j = PythonOperator(
        task_id = "pass_to_Neo4j",
        python_callable = pass_to_Neo4j
    )

    Download_Data  >> pass_to_Neo4j