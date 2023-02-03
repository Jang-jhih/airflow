#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 14:55:11 2022

@author: jacob
"""

from finance.require import *
import numpy as np
import io



def crawl_price(date):
    """
    Args:
        
    Returns:
   
    """
    

    dftwe = price_twe(date)
    time.sleep(5)
    dfotc = price_otc(date)
    if len(dftwe) != 0 and len(dfotc) != 0:
        return RenameAndMerge(twe = dftwe,
                                otc = dfotc,
                                t2o = ReplaceCoulmnsForPrice()['o2tp']
                                )
    else:
        return pd.DataFrame()

def price_twe(date):
    """
    Args:
       
    Returns:
   
    """
    date_str = date.strftime('%Y%m%d')
    res = requests_get(f'https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date={date_str}&type=ALLBUT0999')

    if res.text == '':
        return pd.DataFrame()

    header = np.where(list(map(lambda l: '證券代號' in l, res.text.split('\n')[:500])))[0][0]

    df = pd.read_csv(io.StringIO(res.text.replace('=','')), header=header-1)
    df = combine_index(df, '證券代號', '證券名稱')
    df = preprocess(df, date)
    return df

def price_otc(date):
    """
    Args:
        
       
    Returns:
   
    """
    datestr = otc_date_str(date)
    link = f'https://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_download.php?l=zh-tw&d={datestr}&s=0,asc,0'
    res = requests_get(link)
    df = pd.read_csv(io.StringIO(res.text), header=2)

    if len(df) < 30:
        return pd.DataFrame()

    df = combine_index(df, '代號', '名稱')
    df = preprocess(df, date)
    df = df[df['成交筆數'].str.replace(' ', '') != '成交筆數']
    return df





def combine_index(df, n1, n2):

    """將dataframe df中的股票代號與股票名稱合併

    Keyword arguments:

    Args:
        df (pandas.DataFrame): 此dataframe含有column n1, n2
        n1 (str): 股票代號
        n2 (str): 股票名稱

    Returns:
        df (pandas.DataFrame): 此dataframe的index為「股票代號+股票名稱」
    """

    return df.set_index(df[n1].astype(str).str.replace(' ', '') + \
        ' ' + df[n2].astype(str).str.replace(' ', '')).drop([n1, n2], axis=1)



def preprocess(df, date):
    """
    Args:
        
       
    Returns:
   
    """
    df = df.dropna(axis=1, how='all').dropna(axis=0, how='all')
    df.columns = df.columns.str.replace(' ', '')
    df.index.name = 'stock_id'
    df.columns.name = ''
    df['date'] = pd.to_datetime(date)
    df = df.reset_index().set_index(['stock_id', 'date'])
    df = df.apply(lambda s: s.astype(str).str.replace(',',''))
    return df


def RenameAndMerge(twe, otc, t2o):
    """
    Args:
        
       
    Returns:
   
    """
    #建立Rename用的Dict
    t2o2 = {k:v for k,v in t2o.items() if k in otc.columns}
    #key是舊名字，這裡用來篩選o2tm的欄位
    otc = otc[list(t2o2.keys())]
    #重新命名
    otc = otc.rename(columns=t2o2)

    twe = twe[twe.columns.intersection(otc.columns)]

    return pd.concat([twe,otc])


#%%
def ReplaceCoulmnsForPrice():
    """
    Args:
        
       
    Returns:
   
    """
    
    DictForRename={
    'o2tp' : {'成交股數':'成交股數',
            '成交筆數':'成交筆數',
            '成交金額(元)':'成交金額',
            '收盤':'收盤價',
            '開盤':'開盤價',
            '最低':'最低價',
            '最高':'最高價',
            '最後買價':'最後揭示買價',
            '最後賣價':'最後揭示賣價',
          },
    
    'o2tpe' : {
        '殖利率(%)':'殖利率(%)',
        '本益比':'本益比',
        '股利年度':'股利年度',
        '股價淨值比':'股價淨值比',
    },
    
    'o2tb' : {
        '外資及陸資買股數': '外資買進股數',
        '外資及陸資賣股數': '外資賣出股數',
        '外資及陸資淨買股數': '外資買賣超股數',
        '投信買進股數': '投信買進股數',
        '投信賣股數': '投信賣出股數',
        '投信淨買股數': '投信買賣超股數',
        '自營淨買股數': '自營商買賣超股數',
        '自營商(自行買賣)買股數': '自營商買進股數(自行買賣)',
        '自營商(自行買賣)賣股數': '自營商賣出股數(自行買賣)',
        '自營商(自行買賣)淨買股數': '自營商買賣超股數(自行買賣)',
        '自營商(避險)買股數': '自營商買進股數(避險)',
        '自營商(避險)賣股數': '自營商賣出股數(避險)',
        '自營商(避險)淨買股數': '自營商買進股數(避險)',
        '三大法人買賣超股數': '三大法人買賣超股數',
      
      
      
        '外資及陸資(不含外資自營商)-買進股數':'外陸資買進股數(不含外資自營商)',
        '外資及陸資買股數': '外陸資買進股數(不含外資自營商)',
    
        '外資及陸資(不含外資自營商)-賣出股數':'外陸資賣出股數(不含外資自營商)',
        '外資及陸資賣股數': '外陸資賣出股數(不含外資自營商)',
    
        '外資及陸資(不含外資自營商)-買賣超股數':'外陸資買賣超股數(不含外資自營商)',
        '外資及陸資淨買股數': '外陸資買賣超股數(不含外資自營商)',
    
        '外資自營商-買進股數':'外資自營商買進股數',
        '外資自營商-賣出股數':'外資自營商賣出股數',
        '外資自營商-買賣超股數':'外資自營商買賣超股數',
        '投信-買進股數':'投信買進股數',
        '投信買進股數': '投信買進股數',
        '投信-賣出股數': '投信賣出股數',
        '投信賣股數': '投信賣出股數',
    
        '投信-買賣超股數':'投信買賣超股數',
        '投信淨買股數': '投信買賣超股數',
    
        '自營商(自行買賣)-買進股數':'自營商買進股數(自行買賣)',
        '自營商(自行買賣)買股數':'自營商買進股數(自行買賣)',
    
        '自營商(自行買賣)-賣出股數':'自營商賣出股數(自行買賣)',
        '自營商(自行買賣)賣股數':'自營商賣出股數(自行買賣)',
    
        '自營商(自行買賣)-買賣超股數': '自營商買賣超股數(自行買賣)',
        '自營商(自行買賣)淨買股數': '自營商買賣超股數(自行買賣)',
    
        '自營商(避險)-買進股數':'自營商買進股數(避險)',
        '自營商(避險)買股數': '自營商買進股數(避險)',
        '自營商(避險)-賣出股數':'自營商賣出股數(避險)',
        '自營商(避險)賣股數': '自營商賣出股數(避險)',
        '自營商(避險)-買賣超股數': '自營商買賣超股數(避險)',
        '自營商(避險)淨買股數': '自營商買賣超股數(避險)',
    
    },
    
    'o2tm' : {n:n for n in ['當月營收', '上月營收', '去年當月營收', '上月比較增減(%)', '去年同月增減(%)', '當月累計營收', '去年累計營收', '前期比較增減(%)']}
    }
    return DictForRename


def otc_date_str(date):
    """將datetime.date轉換成民國曆

    Args:
        date (datetime.date): 西元歷的日期

    Returns:
        str: 民國歷日期 ex: 109/01/01
    """
    return str(date.year - 1911) + date.strftime('%Y/%m/%d')[4:]
