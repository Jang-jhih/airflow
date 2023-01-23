#!/bin/bash
docker compose down 
docker compose build 
docker compose up -docker -d
sleep 10
docker compose cp webserver:/opt/airflow $PWD