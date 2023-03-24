from textwrap import dedent
from airflow import DAG 
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
# from datahub_provider.entities import Dataset, Urn
import csv
from finance.stock import *
import os


default_args = {
    'owner': 'Crawlar',
    }

with DAG(
    "bargin",
    default_args = default_args,
    description = "Stock bargin",
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["datahub_demo"],
) as dag:
    dag.doc_md = __doc__
    
    def Download_Data():
        tablename = 'bargin'
        hook = PostgresHook(postgres_conn_id="_postgresql")
        engine = hook.get_sqlalchemy_engine()


        datetime_object = datetime.strptime('20230202', '%Y%m%d')
        dates = date_range(datetime_object, datetime.now())
        for date in dates:
            df = crawl_bargin(date)
            print(f'Crawlar {date}')
            time.sleep(5)
            df.to_sql(tablename, engine, if_exists='append', index=False)


    create_temp_table = PostgresOperator(
        task_id='create_temp_table',
        postgres_conn_id='_postgresql',
        sql="""

        DROP TABLE IF EXISTS temp_bargin;

        CREATE TEMPORARY TABLE temp_bargin AS
        SELECT * FROM bargin
        WHERE date BETWEEN current_date - interval '3 days' AND current_date;

        """,
        dag=dag,
    )




    Download_Data = PythonOperator(
        task_id = "Download_Data",
        python_callable = Download_Data
    )


    # update_lineage = BashOperator(
    #         task_id="ETL",
    #         dag=dag,
    #         bash_command="echo 'This is where you might run your data tooling.'",
    #         inlets=[
    #             Urn("urn:li:dataset:(urn:li:dataPlatform:postgres,stock.public.bargin,PROD)"),
    #         ],
    #         outlets=[Dataset("postgres", "stock.public.temp_bargin")],
    #     )


    Download_Data  >> create_temp_table 