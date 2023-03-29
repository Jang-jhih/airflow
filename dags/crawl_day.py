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
from finance.stock import *
import os


default_args = {
    'owner': 'Crawlar',
    'depends_on_past': False,
    'start_date': datetime(2023, 2, 18),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}
# This DAG is used to crawl the date every day.

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
    
    def download_daily_data():
        job = 'crawl_date'
        tablenames = ['price','bargin','benchmark','pe']
        crawl_funcs = [crawl_price,crawl_bargin,crawl_benchmark,crawl_pe]
        hook = PostgresHook(postgres_conn_id="_postgresql")
        engine = hook.get_sqlalchemy_engine()

        try:
            datetime_object = Variable.get(var)
        except:
            datetime_object = datetime.strptime('20000107', '%Y%m%d')

        dates = date_range(datetime_object, datetime.now())

        for crawl_func,tablename in zip(crawl_funcs,tablenames):
            # print(crawl_func,tablename)
            for date in dates:
                week = get_weekday(date)
                print(f'Crawlar {tablename} {date}')
                var = f'{job}_{tablename}'
                df = crawl_func(date)

                time.sleep(5)

                df.to_sql(tablename, engine, if_exists='append', index=False)
                Variable.set(var,date + timedelta(days=1))





    Download_Daily_Data = PythonOperator(
        task_id = "download_daily_data",
        python_callable = download_daily_data
    )


  

    Download_Daily_Data 