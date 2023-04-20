# from textwrap import dedent
from airflow import DAG 
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datahub_provider.entities import Dataset, Urn
from finance.stock import crawl_monthly_report

import time
from finance.process import month_range, test_database
import os


test = os.getenv('test')
"""
    This DAG will crawl the data from the month.
    The code is in the following files:
    1. crawl_month.py
    2. crawl_year.py
    3. crawl_week.py
    4. crawl_day.py
"""



default_args = {
    'owner': 'Crawlar',
    'depends_on_past': False,
    'start_date': datetime(2023, 2, 18),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    "crawl_month",
    default_args=default_args,
    description="月執行",
    schedule_interval="15 19 1-10 * *",
    catchup=False,
    tags=["datahub_demo"],
) as dag:
    dag.doc_md = __doc__
    
    
    def download_monthly_data():
        job = 'crawl_month'
        tablename = "month_revenue"
        hook = PostgresHook(postgres_conn_id="_postgresql")
        engine = hook.get_sqlalchemy_engine()

        var = f'{job}'
        try:
            datetime_object = Variable.get(var)
        except:
            datetime_object = datetime.strptime('20190110', '%Y%m%d')
        dates = month_range(datetime_object, datetime.now())

        for date in dates:
            time.sleep(5)
            print(f'Crawlar {date} {tablename}')


            df = crawl_monthly_report(date)
            
            if test:
                df = test_database(df,key=tablename)
            else:
                df.to_sql(tablename, engine, if_exists='append', index=False)





    Download_Monthly_Data = PythonOperator(
        task_id = "download_monthly_data",
        python_callable = download_monthly_data
    )


  

    Download_Monthly_Data 