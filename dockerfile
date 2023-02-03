FROM apache/airflow:2.5.0-python3.9
# FROM apache/airflow:2.0.2-python3.9
COPY ./tools ./tools


USER root
RUN chown -R airflow ${AIRFLOW_HOME} \
    && chmod +x ./tools
    # && chmod +x ./tools/*.sh


USER airflow

RUN pip3 install --upgrade pip
RUN pip3 install -r ./tools/requirements


ENTRYPOINT [ "bash", "./tools/start_services.sh" ]
