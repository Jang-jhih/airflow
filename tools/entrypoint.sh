#!/bin/bash

# airflow connections add '_mongoid'  --conn-uri 'mongo://airflow:airflow@mongo:27017/'
# airflow connections add '_mysqlid'  --conn-uri 'mysql://root:airflow@mysql:3306/'
airflow connections add '_postgresql'  --conn-uri 'postgres://airflow:airflow@postgres:5432/stock'

# For REST-based:
# airflow connections add  --conn-type 'datahub_rest' 'datahub_rest_default' --conn-host 'http://datahub-gms:8080' --conn-password '<optional datahub auth token>'
# For Kafka-based (standard Kafka sink config can be passed via extras):
# airflow connections add  --conn-type 'datahub_kafka' 'datahub_kafka_default' --conn-host 'broker:9092' --conn-extra '{}'

airflow webserver
