ARG AIRFLOW_IMAGE=apache/airflow:2.4.0-python3.7
FROM $AIRFLOW_IMAGE AS airflow
COPY integration/sql /app/openlineage/integration/sql
COPY integration/common /app/openlineage/integration/common
COPY integration/airflow /app/openlineage/integration/airflow
COPY client/python /app/openlineage/client/python
COPY integration/target /app/openlineage/integration/sql/target
USER root
RUN mkdir -p /opt/data
RUN apt-get update && apt-get install -y git
COPY integration/airflow/tests/integration/data /opt/data
COPY integration/airflow/tests/integration/docker/wait-for-it.sh /opt/data/wait-for-it.sh
RUN chmod -R 777 /opt/data
RUN chmod a+rwxX -R /app/openlineage
USER airflow
RUN AIRFLOW_VERSION=`airflow version` && \
    PYTHON_VERSION=`python -c "import sys; print('{}.{}'.format(*sys.version_info))"` && \
    cd /app/openlineage/integration/sql && \
    pip install openlineage-sql --no-index --find-links target/wheels --force-reinstall && \
    cd ../airflow && \
    pip install --no-cache-dir --use-deprecated=legacy-resolver -r dev-requirements.txt \
    --constraint=https://raw.githubusercontent.com/apache/airflow/constraints-$AIRFLOW_VERSION/constraints-$PYTHON_VERSION.txt


FROM python:3.7-slim as integration
RUN mkdir -p /app && mkdir -p /opt/openlineage
RUN apt-get update && \
    apt-get install -y python3-dev default-libmysqlclient-dev build-essential
COPY integration/common /opt/openlineage/integration/common
COPY integration/airflow /opt/openlineage/integration/airflow
COPY client/python /opt/openlineage/client/python
COPY integration/airflow/integration-requirements.txt /opt/openlineage/integration/integration-requirements.txt
WORKDIR /app
COPY integration/airflow/tests/integration/*.py ./
COPY integration/airflow/tests/integration/pytest.ini ./
COPY integration/airflow/tests/integration/requests requests
RUN cd /opt/openlineage/integration/ && pip install --use-deprecated=legacy-resolver --user -r integration-requirements.txt
