import pandas as pd
import psycopg2

def get(dataset):
    #connect to database
    connection = connect()
    #dataset = "price:收盤價"

    table = dataset.split(':')[0] 
    column = dataset.split(':')[1]
    sql = f"select date,{column} from public.{table}"

    #execute query
    df = pd.read_sql(sql, connection)
    df.set_index('date', inplace=True)
    return df

def connect():
    connection = psycopg2.connect(
                host="localhost",
                port="5432",
                dbname="stock",
                user="postgres",
                password="postgres"
            )
    return connection