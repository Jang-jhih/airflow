#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 18:13:23 2022

@author: jacob
"""
from finance.stock import *
import os
from tqdm import tnrange, tqdm_notebook
import pickle
import sqlalchemy
import datetime
import os
import pandas as pd


#%%


def table_date_range(table_name):
    if os.path.isfile(date_range_record_file):
        with open(date_range_record_file, 'rb') as f:
            dates = pickle.load(f)
            if table_name in dates:
                return dates[table_name]
            else:
                return [None, None]
    else:
        return [None, None]
                

#%%
from datetime import date
from dateutil.rrule import rrule, DAILY, MONTHLY

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