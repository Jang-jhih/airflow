from textwrap import dedent
from airflow import DAG
# from Opinion.ToDatabas import *
from Opinion.ptt import *
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
from airflow.providers.mongo.hooks.mongo import MongoHook

default_args = {
    'owner': 'airflow',
}

with DAG(
    '____',
    default_args=default_args,
    description='PTT Opinion',
    schedule_interval=None,
    start_date=days_ago(2),
    tags=['PTT_Crawler'],
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
        df.to_csv(f'/opt/airflow/data/{table_name}_tmp.csv')
        


        # total_value = {"total_order_value": total_order_value}
        # total_value_json_string = json.dumps(total_value)
        ti.xcom_push("table_name", table_name)

    def load(**kwargs):
        
        ti = kwargs['ti']
        table_name = ti.xcom_pull(task_ids='transform',key='table_name')


        df = pd.read_csv(f'/opt/airflow/data/{table_name}_tmp.csv')

        dict = df.to_dict('records')

        hook = MongoHook(conn_id="mongo")
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