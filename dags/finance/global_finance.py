#crawl global finance data url = "https://query1.finance.yahoo.com/v8/finance/chart/AAPL?region=US&lang=en-US&includePrePost=false&interval=2m&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance"
import requests
import json
import pandas as pd
from fake_useragent import UserAgent
import datetime


def get_request(url):
    '''Get request with random user agent'''
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    res = requests.get(url, headers=headers)
    return res.text
    


def get_stock_data(stock_id):
    '''
    Get stock data from yahoo finance
    Args:
        stock_id (str): stock id
    Returns:
        pd.DataFrame: stock data
        '''
    d = datetime.datetime.now()
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{stock_id}?period1=0&period2={str(int(d.timestamp()))}&interval=1d&events=history&=hP2rOschxO0"
    res =get_request(url)
    data = json.loads(res)
    df = pd.DataFrame(data['chart']['result'][0]['indicators']['quote'][0])
    df['timestamp'] = data['chart']['result'][0]['timestamp']
    df['date'] = pd.to_datetime(df['timestamp'], unit='s')
    df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
    return df

def get_stock_list():
    '''Get stock list from yahoo finance
    Returns:
        list: list of stock id
    '''
    url = "https://finance.yahoo.com/screener/predefined/most_actives"
    res = get_request(url)
    df = pd.read_html(res)[0]
    return df['Symbol'].tolist()


def get_stock_data_all():
    '''Get stock data from yahoo finance
    Returns:
        pd.DataFrame: stock data
    '''
    
    stock_list = get_stock_list()
    df = pd.DataFrame()
    for stock_id in stock_list:
        df = df.append(get_stock_data(stock_id))
    return df

df = get_stock_data_all()
df.to_csv('stock.csv', index=False)

