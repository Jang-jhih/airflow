FROM apache/airflow:2.5.0-python3.9
# FROM apache/airflow:2.0.2-python3.9
COPY ./tools ./tools


USER root

RUN mkdir /var/tmp/amundsen \
&& mkdir /var/tmp/amundsen/table_metadata \
&& mkdir /var/tmp/amundsen/table_metadata/relationships 



#RUN chown -R airflow ${AIRFLOW_HOME} \
#    && chmod +x ./tools \
#    && chmod +x /var/tmp/amundsen \
#    && chmod +x /var/tmp/amundsen/table_metadata \
#    && chmod +x /var/tmp/amundsen/table_metadata/relationships 


RUN chown -R airflow ${AIRFLOW_HOME} \
    && chmod 777 ./tools 

# RUN apt-get update 
# RUN apt-get install -y \
#     libmysqlclient-dev \
#     mysql-server \
#     mysql-client
#     # python3-dev





USER airflow


RUN pip3 install --upgrade pip
RUN pip3 install -r ./tools/requirements


ENTRYPOINT [ "bash", "./tools/start_services.sh" ]
