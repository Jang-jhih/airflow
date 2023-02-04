#!/usr/bin/env bash

version () {

    airflow db init
    echo "Creating default user in UI..."
    airflow users create \
        --role ${ROLE} \
        --username ${USERNAME} \
        --password ${PASSWORD} \
        --firstname ${FIRSTNAME} \
        --lastname ${LASTNAME} \
        --email ${EMAIL}



    
    # airflow connections add 'my_prod_db'  --conn-uri '<conn-type>://<login>:<password>@<host>:<port>/<schema>?param1=val1&param2=val2&...'
    airflow connections add '_mongoid'  --conn-uri 'mongo://airflow:airflow@mongo:27017/'
    airflow connections add '_mysqlid'  --conn-uri 'mysql://root:airflow@mysql:3306/'
    airflow connections add '_postgresql'  --conn-uri 'postgres://airflow:airflow@postgres:5432/stock'

}
