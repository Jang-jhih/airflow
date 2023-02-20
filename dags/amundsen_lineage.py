



from pyhocon import ConfigFactory
from datetime import datetime, timedelta
from openlineage.airflow import DAG
from databuilder.extractor.csv_extractor import (
    CsvColumnLineageExtractor, CsvTableLineageExtractor,
)
from databuilder.job.job import DefaultJob
from databuilder.loader.file_system_neo4j_csv_loader import FsNeo4jCSVLoader
from databuilder.publisher.neo4j_csv_publisher import Neo4jCsvPublisher
from databuilder.task.task import DefaultTask
from databuilder.transformer.base_transformer import  NoopTransformer
from airflow.operators.python import PythonOperator  # noqa

neo4j_user = 'neo4j'
neo4j_password = 'test'

NEO4J_ENDPOINT = 'bolt://neo4j:7687'

neo4j_endpoint = NEO4J_ENDPOINT

dag_args = {
    'max_active_tasks': 10,
    # One dagrun at a time
    'max_active_runs': 1,
    # 4AM, 4PM PST
    'schedule': '0 11 * * *',
    'catchup': False
}

default_args = {
    'owner': 'amundsen',
    'start_date': datetime(2018, 6, 18),
    'depends_on_past': False,
    'email': [''],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'priority_weight': 10,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(minutes=120)
}

def run_table_lineage_job():
    table_lineage_path = '/tmp/lineage/sample_table_lineage.csv'
    tmp_folder = '/var/tmp/amundsen/table_column'
    node_files_folder = f'{tmp_folder}/nodes'
    relationship_files_folder = f'{tmp_folder}/relationships'
    extractor = CsvTableLineageExtractor()
    csv_loader = FsNeo4jCSVLoader()
    task = DefaultTask(extractor,
                       loader=csv_loader,
                       transformer=NoopTransformer())

                       
    job_config = ConfigFactory.from_dict({
        'extractor.csvtablelineage.table_lineage_file_location': table_lineage_path,
        'loader.filesystem_csv_neo4j.node_dir_path': node_files_folder,
        'loader.filesystem_csv_neo4j.relationship_dir_path': relationship_files_folder,
        'loader.filesystem_csv_neo4j.delete_created_directories': True,
        'publisher.neo4j.node_files_directory': node_files_folder,
        'publisher.neo4j.relation_files_directory': relationship_files_folder,
        'publisher.neo4j.neo4j_endpoint': neo4j_endpoint,
        'publisher.neo4j.neo4j_user': neo4j_user,
        'publisher.neo4j.neo4j_password': neo4j_password,
        'publisher.neo4j.neo4j_encrypted': False,
        'publisher.neo4j.job_publish_tag': 'lineage_unique_tag',  # should use unique tag here like {ds}
    })
    job = DefaultJob(conf=job_config,
                     task=task,
                     publisher=Neo4jCsvPublisher())
    job.launch()


def run_column_lineage_job():
    column_lineage_path = '/tmp/lineage/sample_column_lineage.csv'
    tmp_folder = '/var/tmp/amundsen/table_column'
    node_files_folder = f'{tmp_folder}/nodes'
    relationship_files_folder = f'{tmp_folder}/relationships'
    extractor = CsvColumnLineageExtractor()
    csv_loader = FsNeo4jCSVLoader()
    task = DefaultTask(extractor,
                       loader=csv_loader,
                       transformer=NoopTransformer())
    job_config = ConfigFactory.from_dict({
        'extractor.csvcolumnlineage.column_lineage_file_location': column_lineage_path,
        'loader.filesystem_csv_neo4j.node_dir_path': node_files_folder,
        'loader.filesystem_csv_neo4j.relationship_dir_path': relationship_files_folder,
        'loader.filesystem_csv_neo4j.delete_created_directories': True,
        'publisher.neo4j.node_files_directory': node_files_folder,
        'publisher.neo4j.relation_files_directory': relationship_files_folder,
        'publisher.neo4j.neo4j_endpoint': neo4j_endpoint,
        'publisher.neo4j.neo4j_user': neo4j_user,
        'publisher.neo4j.neo4j_password': neo4j_password,
        'publisher.neo4j.neo4j_encrypted': False,
        'publisher.neo4j.job_publish_tag': 'lineage_unique_tag',  
    })
    job = DefaultJob(conf=job_config,
                     task=task,
                     publisher=Neo4jCsvPublisher())
    job.launch()



with DAG('amundsen_lineage', 
        default_args=default_args,
        tags=["amundsen_demo"],
         **dag_args
     ) as dag:

    run_table_lineage_job = PythonOperator(
        task_id='postgres_table_extract_job',
        python_callable=run_table_lineage_job
    )

    run_column_lineage_job = PythonOperator(
        task_id='postgres_es_index_job',
        python_callable=run_column_lineage_job
    )
    
    run_table_lineage_job >> run_column_lineage_job

