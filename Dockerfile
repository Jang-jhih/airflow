# FROM apache/airflow:2.5.1
FROM apache/airflow:2.5.1-python3.9

COPY ./tools ./tools

USER root

RUN chown -R airflow ${AIRFLOW_HOME} \
    && chmod +x ./tools/*.sh \
    && chmod +x ./tools/*.txt

RUN apt-get update \
    && apt-get install -y \
        gcc freetds-dev \
        librdkafka-dev
        # python3-dev

RUN pip3 install --upgrade pip
RUN pip3 install -r ./tools/requirements.txt
RUN pip3 install apache-airflow[mongo]

RUN pip3 install --upgrade pip wheel setuptools
RUN pip3 install --upgrade acryl-datahub
RUN pip3 install acryl-datahub[airflow]





USER airflow


ENTRYPOINT [ "bash", "./tools/start_services.sh" ]
