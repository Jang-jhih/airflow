#!/usr/bin/env bash

scheduler () {
    airflow db init
    echo "Migrating Apache Airflow metadata..."
    airflow db upgrade

    echo "Starting Airflow Scheduler..."
    airflow scheduler
}
