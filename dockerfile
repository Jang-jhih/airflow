FROM apache/airflow:2.5.1-python3.7


USER root

COPY ./tools ./tools
COPY ./OpenLineage/integration/airflow ./OpenLineage

RUN chmod -R 777 /usr/local/lib && chmod -R 777 /usr/local/bin
RUN chmod -R 777 ./tools && chmod -R 777 ./OpenLineage


USER airflow

RUN pip3 install --upgrade pip
RUN pip3 install -r ./tools/requirements.txt



# WORKDIR /opt/airflow/OpenLineage
# RUN pip3 install openlineage-airflow
# RUN python3 ./setup.py install


WORKDIR /opt/airflow
