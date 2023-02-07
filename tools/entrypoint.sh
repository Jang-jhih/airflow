#!/bin/bash

airflow connections add '_mongoid'  --conn-uri 'mongo://airflow:airflow@mongo:27017/'
airflow connections add '_mysqlid'  --conn-uri 'mysql://root:airflow@mysql:3306/'
airflow connections add '_postgresql'  --conn-uri 'postgres://airflow:airflow@postgres:5432/stock'



airflow webserver