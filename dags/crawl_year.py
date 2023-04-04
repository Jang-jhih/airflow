from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datahub_provider.entities import Dataset, Urn
from finance.stock import (download_finance_statement,
                            )
from finance.process import (season_range
                            )


default_args = {
    'owner': 'Crawlar',
    'depends_on_past': False,
    'start_date': datetime(2023, 2, 18),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

#create the dag, crawl year
with DAG(
    "crawl_year",
    default_args = default_args,
    description = "年執行",
    schedule=timedelta(days=1),
    start_date="15 19 * * *",
    catchup=False,
    tags=["datahub_demo"],
) as dag:

    def download_yearly_data():
        job = 'crawl_year'
        tablenames = "finance_statement"
        hook = PostgresHook(postgres_conn_id="_postgresql")
        engine = hook.get_sqlalchemy_engine()
        conn = engine.connect()
        start_date = datetime(2019, 1, 1)
        end_date = datetime.now()
        
        data_range = season_range(start_date, end_date)
        
        for date in data_range:
            
            

    download_yearly_data = PythonOperator(
        task_id = "download_yearly_data",
        python_callable = download_yearly_data,
    )

    download_yearly_data