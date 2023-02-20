from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.bash import BashOperator
from datahub_provider.entities import Dataset, Urn

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 2, 18),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}



with DAG(
    "chatGPT_test1.",
    default_args = default_args,
    description = "Stock price",
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["Stock Crawler"],
) as dag:
    dag.doc_md = __doc__

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


    task1 = BashOperator(
            task_id="run_data_task",
            dag=dag,
            bash_command="echo 'This is where you might run your data tooling.'",
            inlets=[
                Dataset("postgres", "stock.public.price"),
                Urn(
                    "urn:li:dataset:(urn:li:dataPlatform:snowflake,mydb.schema.tableC,PROD)"
                ),
            ],
            outlets=[Dataset("postgres", "stock.public.temp_price")],
        )



    create_temp_table >> task1
