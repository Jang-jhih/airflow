# from textwrap import dedent
from airflow import DAG 
from airflow.operators.python import PythonOperator

from datetime import datetime, timedelta
from finance.stock import (crawl_price,crawl_bargin,crawl_benchmark,crawl_pe)
import time
from finance.process import test_database, date_range, save_to_parquet
import os
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models import Variable
import pandas as pd


test = os.getenv('test')
default_args = {
    'owner': 'Crawlar',
    'depends_on_past': False,
    'start_date': datetime(2023, 2, 18),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# This DAG is used to crawl the date every day.
with DAG(
    "crawl_date",
    default_args=default_args,
    description="日執行",
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=["datahub_demo"],
) as dag:
    dag.doc_md = __doc__

    
    def download_daily_data():
        # os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64"
        job = 'crawl_date'
        tablenames = ['price','bargin','benchmark','pe']
        crawl_funcs = [crawl_price,crawl_bargin,crawl_benchmark,crawl_pe]
        hook = PostgresHook(postgres_conn_id="_postgresql")
        engine = hook.get_sqlalchemy_engine()
        date_format = '%Y-%m-%d'

        for crawl_func,tablename in zip(crawl_funcs,tablenames):
            # print(crawl_func,tablename)
            var = f'{job}_{tablename}'
            try:
                datetime_str = Variable.get(var)
                datetime_object = datetime.strptime(datetime_str, date_format)
            except:
                datetime_object = datetime.strptime('20190107', '%Y%m%d')


            dates = date_range(datetime_object, datetime.now())
            for date in dates:
 
                print(f'Crawlar {tablename} {date}')
                var = f'{job}_{tablename}'
                df = crawl_func(date)

                time.sleep(5)
                # if test:
                #     df = test_database(df,key=tablename)
                # else:
                # df.to_sql(tablename, engine, if_exists='append', index=False)
                save_to_parquet(df,tablename)
                Variable.set(var,date + timedelta(days=1))



    Download_Daily_Data = PythonOperator(
        task_id = "download_daily_data",
        python_callable = download_daily_data
    )



    Download_Daily_Data 