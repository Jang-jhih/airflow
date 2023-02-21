from textwrap import dedent
from airflow import DAG 
from Opinion.ptt import *
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from airflow.providers.mongo.hooks.mongo import MongoHook
from datetime import datetime, timedelta

default_args = {
    'owner': 'Opinion',
    # "depends_on_past": False,
    # "email": ["airflow@example.com"],
    # "email_on_failure": False,
    # "email_on_retry": False,
    # "retries": 1,
    # "retry_delay": timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
    }

with DAG(
    "PTT_Stock",
    default_args=default_args,
    description="Cralwer",
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["PTT_Opinion"],
) as dag:


    dag.doc_md = __doc__

    def extract(**kwargs):
        ti = kwargs['ti']
        table_name = Variable.get("table_name")
        end_page = new_page(table_name)
        Variable.set(f'{table_name}_new_page',end_page)

        try:
            page = Variable.get(f"{table_name}_page")
        except:
            Variable.set(f"{table_name}_page",1000)
            page = Variable.get(f"{table_name}_page")

        ti.xcom_push('order_data', page)

    def transform(**kwargs):

        ti = kwargs['ti']
        page = ti.xcom_pull(task_ids='extract', key='order_data')


        table_name = Variable.get("table_name")
        url = f'https://www.ptt.cc/bbs/{table_name}/index{page}.html'
        links = links_list(url) #取得所有連結
        df = content_cralwer(links)
        df['date'] = page
        df.to_csv(f'/opt/airflow/tools/{table_name}_tmp.csv')
        


        # total_value = {"total_order_value": total_order_value}
        # total_value_json_string = json.dumps(total_value)
        ti.xcom_push("table_name", table_name)

    def load(**kwargs):
        
        ti = kwargs['ti']
        table_name = ti.xcom_pull(task_ids='transform',key='table_name')


        df = pd.read_csv(f'/opt/airflow/tools/{table_name}_tmp.csv')

        dict = df.to_dict('records')

        hook = MongoHook(conn_id="mongoid")
        hook.insert_many(docs=dict,mongo_db="Opinion",mongo_collection=table_name )

        page = ti.xcom_pull(task_ids='extract', key='order_data')

        Variable.set(f"{table_name}_page",int(page) + 1)


    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract,
    )
    extract_task.doc_md = dedent(
        """\
    #### Extract task
    A simple Extract task to get data ready for the rest of the data pipeline.
    In this case, getting data is simulated by reading from a hardcoded JSON string.
    This data is then put into xcom, so that it can be processed by the next task.
    """
    )

    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform,
    )
    transform_task.doc_md = dedent(
        """\
    #### Transform task
    A simple Transform task which takes in the collection of order data from xcom
    and computes the total order value.
    This computed value is then put into xcom, so that it can be processed by the next task.
    """
    )

    load_task = PythonOperator(
        task_id='load',
        python_callable=load,
    )
    load_task.doc_md = dedent(
        """\
    #### Load task
    A simple Load task which takes in the result of the Transform task, by reading it
    from xcom and instead of saving it to end user review, just prints it out.
    """
    )

    extract_task >> transform_task  >> load_task