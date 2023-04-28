FROM apache/airflow:2.5.1

USER root


RUN apt-get update && \
  apt-get install -y --no-install-recommends gcc git libssl-dev g++ make && \
  cd /tmp && git clone https://github.com/edenhill/librdkafka.git && \
  cd librdkafka && git checkout tags/v1.9.0 && \
  ./configure && make && make install && \
  cd ../ && rm -rf librdkafka







USER airflow
RUN pip install --upgrade pip \
    # && pip install acryl-datahub-airflow-plugin \
    && pip install fake_useragent \
                    apache-airflow-providers-mongo


