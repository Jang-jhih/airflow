from __future__ import annotations
from datetime import datetime, timedelta
from textwrap import dedent
from airflow import DAG
from Opinion.ToDatabas import *
from Opinion.ptt import *
# from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.models import Variable



def crawler(**context): #主要程式
    # print(os.getcwd())
    table_name = Variable.get("table_name")
    end_page = new_page(table_name) #取得最新頁面
    
    for page in range(start_page, end_page, 1):
        print(page)
        url = f'https://www.ptt.cc/bbs/{table_name}/index{page}.html'
        links = links_list(url) #取得所有連結
        df = content_cralwer(links)
        df['date'] = page



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
        provide_context=True
    )

    # ToMongo = PythonOperator(
    #     task_id="To_Mongo",
    #     python_callable=To_Mongo,
    #     # provide=True
    # )
    
crawlPTT 
# >> ToMongo