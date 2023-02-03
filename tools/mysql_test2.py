import pymysql
import os

connection = pymysql.connect(
    host="mysql",
    database="stock",
    user="root",
    password="airflow"
)
cursor = connection.cursor()
cursor.execute("select @@version ")
version = cursor.fetchone()
if version:
    print('Running version: ', version)
else:
    print('Not connected.')
connection.close()