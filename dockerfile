FROM apache/airflow:2.5.1

USER root


RUN apt-get update && \
  apt-get install -y --no-install-recommends gcc git libssl-dev g++ make && \
  cd /tmp && git clone https://github.com/edenhill/librdkafka.git && \
  cd librdkafka && git checkout tags/v1.9.0 && \
  ./configure && make && make install && \
  cd ../ && rm -rf librdkafka




COPY ./docker/entrypoint.sh  ./docker/entrypoint.sh 
RUN chmod -R 777 ./docker


USER airflow
RUN pip install --upgrade pip \
    && pip install acryl-datahub-airflow-plugin \
                    fake_useragent \
                    apache-airflow-providers-mongo


