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
import logging


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
    logger = logging.getLogger("airflow.task")

    def crawl_season():
        date_format = '%Y-%m-%d'
        var = 'crawl_season'

        try:
            datetime_str = Variable.get(var)
            datetime_object = datetime.strptime(datetime_str, date_format)
            logger.info("datetime_object is %s" % datetime_object)
        except:
            datetime_object = datetime.strptime('20190501', '%Y%m%d')
            logger.info("date time is %s" % datetime_object)

        dates = season_range(datetime_object, datetime.now())
        logger.info("dates is %s" % dates)
        for date in dates:
            logger.info("date is %s" % date)
            get_finance_season(date)
            Variable.set(var, date)
            
    #Put the data from history directory into the database.
    def concat_all_data():

        tmp_path = os.getenv('tmp_dir')
        path = os.path.join(tmp_path,'financial_statement')
        pickle_files = [f for f in os.listdir(path) if f.endswith('.pickle')]
        
        i = 0
        for file in pickle_files:
            dfs = pd.read_pickle(f'{path}/{file}')
            for key in dfs.keys():
                df = dfs[key]
                if i == 0:
                    old_df = pd.concat([df,pd.DataFrame()])
                else:
                    old_df = pd.read_csv(os.path.join(tmp_path,f'{key}.csv'))
                    old_df = pd.concat([old_df,df])
                old_df.to_csv(os.path.join(tmp_path,f'{key}.csv'),index=False)
            i += 1

                    
    def put_data_into_db():
        hook = PostgresHook(postgres_conn_id="_postgresql")
        engine = hook.get_sqlalchemy_engine()
        tmp_path = os.getenv('tmp_dir')
        for file in os.listdir(tmp_path):
            if file.endswith('.csv'):
                df = pd.read_csv(os.path.join(tmp_path,file))
                file_name = file.split('.')[0]
                df.to_sql(file_name, engine, if_exists='replace', index=False)


    #remove the history directory.
    def remove_history():
        tmp_path = os.getenv('tmp_dir')
        path = os.path.join(tmp_path,'financial_statement')
        os.rmdir(path)
        print('!!!!Remove history directory!!!!')
        


    Download_Season_Data = PythonOperator(
        task_id = "download_season_data",
        python_callable = crawl_season,
    )

    Concat_All_Data = PythonOperator(
        task_id = "concat_all_data",
        python_callable = concat_all_data,
    )

    Put_Data_Into_DB = PythonOperator(
        task_id = "put_data_into_db",
        python_callable = put_data_into_db,
    )



    Remove_History = PythonOperator(
        task_id = "remove_history",
        python_callable = remove_history,
    )


    Download_Season_Data >> Concat_All_Data >> Put_Data_Into_DB >> Remove_History


    
        
        