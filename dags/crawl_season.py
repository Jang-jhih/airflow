from finance.finance_statemnt import download_finance_statement, get_season
from finance.process import get_season
from datetime import datetime, timedelta
from finance.stock import date_range
from airflow.models import Variable


def download_finance_statement(year, season):
    try:
        datetime_object = Variable.get(var)
    except:
        datetime_object = datetime.strptime('20200101', '%Y%m%d')


    dates = season_range(datetime_object, datetime.now())
    for date in dates:
        year, season = get_season(date)
        print(f'Crawlar {year} {season}')
        var = f'crawl_season_{year}_{season}'
        download_finance_statement(year, season)
        Variable.set(var,date + timedelta(days=1))
