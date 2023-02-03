#!/usr/bin/env bash

webserver () {
    echo "Removing older pid files..."
    rm ${AIRFLOW_HOME}/airflow-webserver.pid



    echo "Starting Airflow Webserver..."
    airflow webserver \
        --port 8080
}


