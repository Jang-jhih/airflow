from datetime import date
from dateutil.rrule import rrule, DAILY, MONTHLY
import os
# from tqdm import tnrange, tqdm_notebook
import pickle
import sqlalchemy
import datetime
import os
import pandas as pd
from multiprocessing import cpu_count

from pyspark.sql import SparkSession
from pyspark.sql.functions import date_format
def save_to_parquet(new_data_df, tablename):
    # cores = cpu_count()
    spark = (
        SparkSession.builder
        .appName("SaveToParquet")
        # .master(f"local[{cores}]")  # 使用动态检测到的核心数
        .master("spark://spark-master:7077")
        .getOrCreate()
    )
    hdfs_path = f'hdfs://namenode:8020/datawarehouse/{tablename}'

    try:
        old_data_df = spark.read.parquet(hdfs_path)
        old_data_df_spark = old_data_df_spark.withColumn("date", date_format("date", "yyyy-MM-dd"))
        old_data_df = old_data_df_spark.toPandas()
        df = pd.concat([old_data_df, new_data_df], ignore_index=True)
        df = df.drop_duplicates()
        df = df.sort_values(by=['date'])
        df = spark.createDataFrame(df)
        df.write.parquet(hdfs_path, mode='overwrite')
        print(f'Update {tablename} to HDFS')
    except:
        new_data_df = new_data_df.sort_values(by=['date'])
        new_data_df = spark.createDataFrame(new_data_df)
        new_data_df.write.parquet(hdfs_path, mode='overwrite')
        print(f'Create {tablename} to HDFS')



#Test using only Sqlite
from sqlalchemy import create_engine
import sqlite3

def test_database(df, key):
    
    engine = create_engine('sqlite:///test.db', echo=True)
    sqlite_connection = engine.connect()
    sqlite_table = key
    df.to_sql(sqlite_table, sqlite_connection, if_exists='append')
    return True


def get_weekday(date):
    weekday = date.weekday()
    if weekday == 0:
        return "星期一"
    elif weekday == 1:
        return "星期二"
    elif weekday == 2:
        return "星期三"
    elif weekday == 3:
        return "星期四"
    elif weekday == 4:
        return "星期五"
    elif weekday == 5:
        return "星期六"
    else:
        return "星期日"




def date_range(start_date, end_date):
    return [dt.date() for dt in rrule(DAILY, dtstart=start_date, until=end_date)]

def month_range(start_date, end_date):
    return [dt.date() for dt in rrule(MONTHLY, dtstart=start_date, until=end_date)]

def season_range(start_date, end_date):

    if isinstance(start_date, datetime.datetime):
        start_date = start_date.date()

    if isinstance(end_date, datetime.datetime):
        end_date = end_date.date()

    ret = []
    for year in range(start_date.year-1, end_date.year+1):
        ret += [  datetime.date(year, 5, 15),
                datetime.date(year, 8, 14),
                datetime.date(year, 11, 14),
                datetime.date(year+1, 3, 31)]
    ret = [r for r in ret if start_date < r < end_date]
    
    return ret