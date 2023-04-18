from datetime import date
from dateutil.rrule import rrule, DAILY, MONTHLY
import os
# from tqdm import tnrange, tqdm_notebook
import pickle
import sqlalchemy
import datetime
import os
import pandas as pd



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