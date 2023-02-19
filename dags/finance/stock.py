

from dateutil.rrule import rrule, DAILY, MONTHLY
from finance.require import *
import numpy as np
import io
from datetime import datetime, date
import os










def date_range(start_date, end_date):
    return [dt.date() for dt in rrule(DAILY, dtstart=start_date, until=end_date)]

def crawl_bargin(date):

    dftwe = bargin_twe(date)
    dfotc = bargin_otc(date)
    
    if '外資買進股數' in dftwe.columns:
      dftwe = dftwe.rename(columns={
        '外資買進股數': '外陸資買進股數(不含外資自營商)',
        '外資賣出股數': '外陸資賣出股數(不含外資自營商)',
        '外資買賣超股數': '外陸資買賣超股數(不含外資自營商)',
      })
    
    if len(dftwe) != 0 and len(dfotc) != 0:
        df =  merge(twe=dftwe, otc=dfotc, t2o =o2tb)
    else:
        df =  pd.DataFrame()
    df.reset_index(inplace=True)

    return df

def bargin_twe(date):
    datestr = date.strftime('%Y%m%d')

    res = requests_get(f'https://www.twse.com.tw/fund/T86?response=csv&date={datestr}&selectType=ALLBUT0999')
    try:
        df = pd.read_csv(io.StringIO(res.text.replace('=','')), header=1)
    except:
        return pd.DataFrame()

    df = combine_index(df, '證券代號', '證券名稱')
    df = preprocess(df, date)
    
    return df

def bargin_otc(date):
    datestr = otc_date_str(date)

    url = f'https://www.tpex.org.tw/web/stock/3insti/daily_trade/3itrade_hedge_result.php?l=zh-tw&o=csv&se=EW&t=D&d={datestr}&s=0,asc'
    res = requests_get(url)
    try:
        df = pd.read_csv(io.StringIO(res.text), header=1)
    except:
        return pd.DataFrame()

    df = combine_index(df, '代號', '名稱')
    df = preprocess(df, date)
    return df












def crawl_pe(date):


    dftwe = pe_twe(date)
    dfotc = pe_otc(date)


    if len(dftwe) != 0 and len(dfotc) != 0:
        df =  merge(dftwe, dfotc, o2tpe)
    else:
        df =  pd.DataFrame()

    df.reset_index(inplace=True)
    return df


def pe_twe(date):
    datestr = date.strftime('%Y%m%d')
    res = requests_get(f'https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=csv&date={datestr}&selectType=ALL')
    try:
        df = pd.read_csv(io.StringIO(res.text), header=1)
    except:
        print("empty")
        return pd.DataFrame()

    df = combine_index(df, '證券代號', '證券名稱')
    df = preprocess(df, date)
    return df

def pe_otc(date):
    datestr = otc_date_str(date)
    res = requests_get(f'https://www.tpex.org.tw/web/stock/aftertrading/peratio_analysis/pera_result.php?l=zh-tw&o=csv&charset=UTF-8&d={datestr}&c=&s=0,asc')
    try:
        df = pd.read_csv(io.StringIO(res.text), header=3)
        df = combine_index(df, '股票代號', '名稱')
        df = preprocess(df, date)
    except:
        print("empty")
        return pd.DataFrame()

    return df

o2tp = {'成交股數':'成交股數',
        '成交筆數':'成交筆數',
        '成交金額(元)':'成交金額',
        '收盤':'收盤價',
        '開盤':'開盤價',
        '最低':'最低價',
        '最高':'最高價',
        '最後買價':'最後揭示買價',
        '最後賣價':'最後揭示賣價',
      }

o2tpe = {
    '殖利率(%)':'殖利率(%)',
    '本益比':'本益比',
    '股利年度':'股利年度',
    '股價淨值比':'股價淨值比',
}

o2tb = {
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

}

o2tm = {n:n for n in ['當月營收', '上月營收', '去年當月營收', '上月比較增減(%)', '去年同月增減(%)', '當月累計營收', '去年累計營收', '前期比較增減(%)']}

def merge(twe, otc, t2o):
    #建立Rename用的Dict
    t2o2 = {k:v for k,v in t2o.items() if k in otc.columns}
    #key是舊名字，這裡用來篩選o2tm的欄位
    otc = otc[list(t2o2.keys())]
    #重新命名
    otc = otc.rename(columns=t2o2)
    # twe = twe[otc.columns & twe.columns]
    twe = twe[twe.columns.intersection(otc.columns)]
    # return twe.append(otc)
    return pd.concat([twe,otc])

def crawl_price(date):
    """
    Args:
        
    Returns:
   
    """
    

    dftwe = price_twe(date)
    time.sleep(5)
    dfotc = price_otc(date)
    if len(dftwe) != 0 and len(dfotc) != 0:
        df =  RenameAndMerge(twe = dftwe,
                                otc = dfotc,
                                t2o = ReplaceCoulmnsForPrice()['o2tp']
                                )
    else:
        df =  pd.DataFrame()


    
    df = df.apply(pd.to_numeric, errors='coerce')
    df.reset_index(inplace = True)
    return df


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


def crawl_benchmark(date):

    date_str = date.strftime('%Y%m%d')
    res = requests_get("https://www.twse.com.tw/exchangeReport/MI_5MINS_INDEX?response=csv&date=" +
                       date_str + "&_=1544020420045")

    # 利用 pandas 將資料整理成表格

    if len(res.text) < 10:
        return pd.DataFrame()

    df = pd.read_csv(io.StringIO(res.text.replace("=","")), header=1, index_col='時間')

    # 資料處理

    df = df.dropna(how='all', axis=0).dropna(how='all', axis=1)
    df.index = pd.to_datetime(date.strftime('%Y %m %d ') + pd.Series(df.index))
    df = df.apply(lambda s: s.astype(str).str.replace(",", "").astype(float))
    df = df.reset_index().rename(columns={'時間':'date'})
    df['stock_id'] = '台股指數'


    
    return df

def interest():
    res = requests_get('https://www.twse.com.tw/exchangeReport/TWT48U_ALL?response=open_data')
    res.encoding = 'utf-8'
    df1 = pd.read_csv(io.StringIO(res.text))
    
    time.sleep(5)

    res = requests_get('https://www.tpex.org.tw/web/stock/exright/preAnnounce/prepost_result.php?l=zh-tw&o=data')
    res.encoding = 'utf-8'
    
    # df = df.append(pd.read_csv(StringIO(res.text)))
    df2 = pd.read_csv(io.StringIO(res.text))
    df = pd.concat([df1,df2])

    df['date'] = df['除權息日期'].astype('str').replace('年', '/').astype('str').replace('月', '/').astype('str').replace('日', '')
    df['date'] = pd.to_datetime(str(datetime.now().year) + df['date'].astype('str').str[3:])
    df['stock_id'] = df['股票代號'].astype(str) + ' ' + df['名稱'].astype(str)
    df.set_index(['stock_id','date'],inplace=True)
    df.reset_index(inplace = True)


    # df = df.set_index([df['股票代號'].astype(str) + ' ' + df['名稱'].astype(str), 'date'])
    return df
