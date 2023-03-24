# from textwrap import dedent
from airflow import DAG 
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datahub_provider.entities import Dataset, Urn
import csv
from finance.stock import (crawl_bargin,
                           crawl_pe,
                           crawl_price,
                           crawl_benchmark
                           )
import os


default_args = {
    'owner': 'Crawlar',
    'depends_on_past': False,
    'start_date': datetime(2023, 2, 18),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    "crawl_date",
    default_args = default_args,
    description = "日執行",
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["datahub_demo"],
) as dag:
    dag.doc_md = __doc__
    
    def Download_Data():
        job = 'crawl_date'
        tablenames = ['price','bargin','benchmark','pe']
        hook = PostgresHook(postgres_conn_id="_postgresql")
        engine = hook.get_sqlalchemy_engine()

        dates = date_range(datetime_object, datetime.now())

        for date in dates:
            print(f'Crawlar {date}')
            for tablename in tablenames:
                var = f'{job}_{tablename}'
                try:
                    datetime_object = Variable.get(var)
                except:
                    datetime_object = datetime.strptime('20000107', '%Y%m%d')
                
                
                print(f'Crawlar {tablename}')
                df = crawl_price(date)

                time.sleep(5)

                df.to_sql(tablename, engine, if_exists='append', index=False)
            Variable.set(var,date + timedelta(days=1))





    Download_Data = PythonOperator(
        task_id = "Download_Data",
        python_callable = Download_Data
    )


  

    Download_Data 