# FROM apache/airflow:2.5.1
FROM apache/airflow:slim-2.5.1-python3.10

COPY ./tools ./tools

USER root

RUN chown -R airflow ${AIRFLOW_HOME} \
    && chmod +x ./tools/*.sh \
    && chmod +x ./tools/*.txt



USER airflow

# RUN pip3 install -r ./tools/requirements.txt

ENTRYPOINT [ "bash", "./tools/start_services.sh" ]
