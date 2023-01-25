# FROM apache/airflow:2.5.1
FROM apache/airflow:2.5.1-python3.9

COPY ./tools ./tools

USER root

RUN chown -R airflow ${AIRFLOW_HOME} \
    && chmod +x ./tools/*.sh \
    && chmod +x ./tools/*.txt



USER airflow

RUN pip3 install -r ./tools/requirements.txt
RUN pip3 install apache-airflow[mongo]

ENTRYPOINT [ "bash", "./tools/start_services.sh" ]
