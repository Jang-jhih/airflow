#!/bin/bash
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi $(docker images -q)

docker stop $(docker ps -aq) && docker rm $(docker ps -aq) && docker compose build && docker compose up


docker compose down 
docker compose build 
docker compose up -docker -d
sleep 10
docker compose cp webserver:/opt/airflow $PWD


#VirtualEnv
# source ./venv/bin/activate

# datahub docker quickstart --arch m1
# datahub docker quickstart --stop