from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.bash import BashOperator
from datahub_provider.entities import Dataset, Urn

default_args = {
    'owner': 'datahub',
    'depends_on_past': False,
    'start_date': datetime(2023, 2, 18),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}



with DAG(
    "Push_datahub_lineage",
    default_args = default_args,
    description = "Stock price",
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["datahub_demo"],
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
            task_id="DataWarehouse",
            dag=dag,
            bash_command="echo 'This is where you might run your data tooling.'",
            inlets=[
                # Dataset("postgres", "stock.public.price"),
                Urn("urn:li:dataset:(urn:li:dataPlatform:postgres,stock.public.temp_bargin,PROD)"),
                Urn("urn:li:dataset:(urn:li:dataPlatform:postgres,stock.public.temp_price,PROD)"),


            ],
            outlets=[Dataset("postgres", "stock.public")],
        )



    create_temp_table >> task1
