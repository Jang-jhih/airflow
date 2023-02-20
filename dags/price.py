from textwrap import dedent
from openlineage.airflow import DAG
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

with DAG(
    "Price",
    default_args = default_args,
    description = "Stock price",
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["datahub_demo"],
) as dag:
    dag.doc_md = __doc__
    
    def Download_Data():
        tablename = 'price'
        hook = PostgresHook(postgres_conn_id="_postgresql")
        engine = hook.get_sqlalchemy_engine()
        
        datetime_object = datetime.strptime('20230202', '%Y%m%d')
        dates = date_range(datetime_object, datetime.now())

        for date in dates:
            print(f'Crawlar {date}')
            df = crawl_price(date)

            time.sleep(5)

            df.to_sql(tablename, engine, if_exists='append', index=False)





    Download_Data = PythonOperator(
        task_id = "Download_Data",
        python_callable = Download_Data
    )

    create_temp_table = PostgresOperator(
        task_id='create_temp_table',
        postgres_conn_id='_postgresql',
        sql="""

        DROP TABLE IF EXISTS temp_price;

        CREATE TEMPORARY TABLE temp_price AS
        SELECT * FROM price
        WHERE date BETWEEN current_date - interval '3 days' AND current_date;

        """,
        dag=dag,
    )

    update_lineage = BashOperator(
            task_id="ETL",
            dag=dag,
            bash_command="echo 'This is where you might run your data tooling.'",
            inlets=[
                Urn("urn:li:dataset:(urn:li:dataPlatform:postgres,stock.public.price,PROD)"),
            ],
            outlets=[Dataset("postgres", "stock.public.temp_price")],
        )

    Download_Data >> create_temp_table >> update_lineage