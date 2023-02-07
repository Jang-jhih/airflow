FROM apache/airflow:2.5.1-python3.7


COPY ./tools ./tools

RUN pip3 install --upgrade pip
RUN pip3 install -r ./tools/requirements



