from __future__ import annotations
from datetime import datetime, timedelta
from textwrap import dedent
from airflow import DAG
from Opinion.ptt import *
# from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.mongo.hooks.mongo import MongoHook



table_name="Stock"

def crawler(table_name): #主要程式
    end_page = new_page(table_name) #取得最新頁面
    
    DB=DataBase(table_name=table_name)

    start_page=DB.table_date_range()
    
    if start_page==[None, None]:
        start_page=round(end_page/1.5)
    
    for page in range(start_page, end_page, 1):
        print(page)
        url = f'https://www.ptt.cc/bbs/{table_name}/index{page}.html'
        links = links_list(url) #取得所有連結
        df = content_cralwer(links)
        df['date'] = page
        To_Mongo(table_name,df)

def To_Mongo(table_name,df):
    try:
        hook = MongoHook(conn_id='mongoid')

        hook.insert_many(mongo_collection=table_name, docs=df.to_dict('records'), mongo_db="Opinion")
      
    except Exception as e:
        print(f"Error connecting to MongoDB -- {e}")

crawler(table_name)

with DAG(
    dag_id="____",
    default_args={
        "owner": "Wang-jain-jhih",
        "depends_on_past": False,
        "email": ["airflow@example.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    description="A simple tutorial DAG",
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["example"],
) as dag:
   
    dag.doc_md = """
    This is a documentation placed anywhere
    """ 

    crawlPTT = PythonOperator(
        task_id="crawler",
        python_callable=crawler,
        provide=True
    )

    ToMongo = PythonOperator(
        task_id="To_Mongo",
        python_callable=To_Mongo,
        provide=True
    )
    
crawlPTT >> ToMongo