from finance.finance_statemnt import get_finance_season
from finance.process import season_range,test_database
from datetime import datetime, timedelta
# from finance.stock import date_range
from airflow.models import Variable
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import pandas as pd
import os

test = os.getenv('test')
"""
    This DAG will crawl the data from the season.
    The code is in the following files:
    1. crawl_season.py
    2. crawl_year.py
    3. crawl_week.py
    4. crawl_day.py
"""

default_args = {
    'owner': 'Crawlar',
    'depends_on_past': False,
    'start_date': datetime(2023, 2, 18),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id="crawl_season",
    default_args=default_args,
    description="季執行",
    schedule_interval=None,
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["datahub_demo"],
) as dag:
    dag.doc_md = __doc__
    
    def crawl_season():
        
        var = 'crawl_season'
        try:
            datetime_object = Variable.get(var)
        except:
            datetime_object = datetime.strptime('20190501', '%Y%m%d')

        dates = season_range(datetime_object, datetime.now())
        for date in dates:
            get_finance_season(date)
            Variable.set(var, date)
            
    #Put the data from history directory into the database.
    def put_data_into_db():
        
        hook = PostgresHook(postgres_conn_id="_postgresql")
        engine = hook.get_sqlalchemy_engine()
        path = os.path.join('history','financial_statement')
        
        #get all the pickle files.
        pickle_files = [f for f in os.listdir(path) if f.endswith('.pickle')]

        for file in pickle_files:
            dfs = pd.read_pickle(f'{path}/{file}')

            #get the data from the dataframe.
            for key in dfs.items():
                df = dfs[key]

                #test database
                if test:
                    test_database(df,key)
                else:
                    
                    df.to_sql(file.split('.')[0], engine, if_exists='append', index=False)

    #remove the history directory.
    def remove_history():
        os.rmdir('history')
        print('!!!!Remove history directory!!!!')
        


    Download_Season_Data = PythonOperator(
        task_id = "download_season_data",
        python_callable = crawl_season,
    )


    Put_Data_Into_DB = PythonOperator(
        task_id = "put_data_into_db",
        python_callable = put_data_into_db,
    )

    Remove_History = PythonOperator(
        task_id = "remove_history",
        python_callable = remove_history,
    )

    Download_Season_Data >> Put_Data_Into_DB >> Remove_History


    
        
        