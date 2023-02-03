#!/usr/bin/env bash

scheduler () {
    airflow db init
    echo "Migrating Apache Airflow metadata..."
    airflow db upgrade



    echo "Creating default user in UI..."
    airflow users create \
        --role ${ROLE} \
        --username ${USERNAME} \
        --password ${PASSWORD} \
        --firstname ${FIRSTNAME} \
        --lastname ${LASTNAME} \
        --email ${EMAIL}

    echo "Starting Airflow Scheduler..."
    airflow scheduler
}
