#!/bin/bash



docker stop $(docker ps -aq)
docker rm $(docker ps -aq)




# docker compose -f ./docker-amundsen.yml  up -d

docker compose -f ./test.yml  up -d
docker compose -f ./docker-airflow.yml up -d

# docker compose -f ./docker-airflow.yml exec -it airflow-webserver bash
# docker compose -f ./docker-airflow.yml exec -it postgres bash
# psql -d airflow -U airflow

# docker compose -f ./airflow/docker-airflow.yml run -it --rm  postgres  bash
docker compose  -f ./airflow/docker-airflow.yml up  postgres  -d
