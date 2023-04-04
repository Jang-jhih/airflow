import requests
import zipfile
import urllib.request
import os
import shutil
import pandas as pd
from datetime import datetime
import pickle
import numpy as np
import re




def get_finance_statement(year,season):
    path = os.path.join('history', 'financial_statement', str(year) + str(season))
    balance_sheet = {}
    income_sheet = {}
    cash_flows = {}
    income_sheet_cumulate = {}


    
    for fname in os.listdir(path):
        dfs = read_html2019(os.path.join(path,fname))
        for df in dfs:
            if 'levels' in dir(df.columns):
                df.columns = list(range(df.values.shape[1]))
            # 假如html不完整，則略過
        if len(dfs) < 4:
            print('**WARRN html file broken', year, season, fname)
            continue
        
        stock_id = fname.split('.')[0]
        # 取得 balance sheet
        df = dfs[1].copy().drop_duplicates(subset=0, keep='last')
        df = df.set_index(0)
        balance_sheet[stock_id] = df[1].dropna()
        #balance_sheet = combine(balance_sheet, df[1].dropna(), stock_id)

        # 取得 income statement
        df = dfs[2].copy().drop_duplicates(subset=0, keep='last')
        df = df.set_index(0)

        # 假如有4個columns，則第1與第3條column是單季跟累計的income statement
        if len(df.columns) == 4:
            income_sheet[stock_id] = df[1].dropna()
            income_sheet_cumulate[stock_id] = df[3].dropna()
        # 假如有2個columns，則代表第3條column為累計的income statement，單季的從缺
        elif len(df.columns) == 2:
            income_sheet_cumulate[stock_id] = df[1].dropna()

        # 假如是第一季財報 累計 跟單季 的數值是一樣的
        if season == 1:
            income_sheet[stock_id] = df[1].dropna()

        # 取得 cash_flows
        df = dfs[3].copy().drop_duplicates(subset=0, keep='last')
        df = df.set_index(0)
        cash_flows[stock_id] = df[1].dropna()

        # 將dictionary整理成dataframe
        balance_sheet = pd.DataFrame(balance_sheet)
        income_sheet = pd.DataFrame(income_sheet)
        income_sheet_cumulate = pd.DataFrame(income_sheet_cumulate)
        cash_flows = pd.DataFrame(cash_flows)

        # 做清理
        ret = {'balance_sheet':clean(year, season, balance_sheet), 'income_sheet':clean(year, season, income_sheet),
                'income_sheet_cumulate':clean(year, season, income_sheet_cumulate), 'cash_flows':clean(year, season, cash_flows)}

        # 假如是第一季的話，則 單季 跟 累計 是一樣的
        if season == 1:
            ret['income_sheet'] = ret['income_sheet_cumulate'].copy()

        ret['income_sheet_cumulate'].columns = '累計' + ret['income_sheet_cumulate'].columns

        pickle.dump(ret, open(os.path.join('history', 'financial_statement', 'pack' + str(year) + str(season) + '.pickle'), 'wb'))

def clean(year, season, balance_sheet):

    if len(balance_sheet) == 0:
        return balance_sheet
    balance_sheet = balance_sheet.transpose().reset_index().rename(columns={'index':'stock_id'})


    if '會計項目' in balance_sheet:
        s = balance_sheet['會計項目']
        balance_sheet = balance_sheet.drop('會計項目', axis=1).apply(pd.to_numeric)
        balance_sheet['會計項目'] = s.astype(str)

    balance_sheet['date'] = afterIFRS(year, season)

    balance_sheet['stock_id'] = balance_sheet['stock_id'].astype(str)
    balance = balance_sheet.set_index(['stock_id', 'date'])
    return balance
        

def afterIFRS(year, season):
    season2date = [ datetime(year, 5, 15),
                    datetime(year, 8, 14),
                    datetime(year, 11, 14),
                    datetime(year+1, 3, 31)]

    return pd.to_datetime(season2date[season-1].date())



def read_html2019(file):
    dfs = pd.read_html(file)
    return [pd.DataFrame(), patch2019(dfs[0]), patch2019(dfs[1]), patch2019(dfs[2])]
      
def remove_english(s):
    result = re.sub(r'[a-zA-Z()]', "", s)
    return result

def patch2019(df):
    df = df.copy()
    dfname = df.columns.levels[0][0]

    df = df.iloc[:,1:].rename(columns={'會計項目Accounting Title':'會計項目'})


    refined_name = df[(dfname,'會計項目')].str.split(" ").str[0].str.replace("　", "").apply(remove_english)

    subdf = df[dfname].copy()
    subdf['會計項目'] = refined_name
    df[dfname] = subdf

    df.columns = pd.MultiIndex(levels=[df.columns.levels[1], df.columns.levels[0]],codes=[df.columns.codes[1], df.columns.codes[0]])

    def neg(s):

        if isinstance(s, float):
            return s

        if str(s) == 'nan':
            return np.nan

        s = s.replace(",", "")
        if s[0] == '(':
            return -float(s[1:-1])
        else:
            return float(s)

    df.iloc[:,1:] = df.iloc[:,1:].applymap(neg)
    return df

def check_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def download_finance_statement(date):
    def tran_date(date):
        year = date.year
        if date.month == 3:
            season = 4
            year = year - 1
            month = 11
            return year, season, month
        elif date.month == 5:
            season = 1
            month = 2
            return year, season, month
        elif date.month == 8:
            season = 2
            month = 5
            return year, season, month
        elif date.month == 11:
            season = 3
            month = 8
            return year, season, month
        else:
            return None
    
    year, season, month = tran_date(date)
    # remove the directory if it exists
    path = os.path.join('history', 'financial_statement', str(year) + str(season))
    if os.path.isdir(path):
        shutil.rmtree(path)

    # check if the directory exists
    dict_tree = {'history': {'financial_statement': {}}}
    # create the directory
    for k, v in dict_tree.items():
        check_dir(k)
        for k1, v1 in v.items():
            check_dir(os.path.join(k, k1))
            for k2, v2 in v1.items():
                check_dir(os.path.join(k, k1, k2))
    
    # download the zip file
    download_finance_zipfile(year, season)
    # unzip the zip file
    unzip_finance_zipfile(path)
    # rename the file
    rename_finance_statement(path)
    # remove the zip file
    os.remove("finance.zip")
    return True

def rename_finance_statement(path):
    fnames = [f for f in os.listdir(path) if f[-5:] == '.html']
    fnames = sorted(fnames)

    newfnames = [f.split("-")[5] + '.html' for f in fnames]

    for fold, fnew in zip(fnames, newfnames):
        if len(fnew) != 9:
            os.remove(os.path.join(path, fold))
            continue

        if not os.path.exists(os.path.join(path, fnew)):
            os.rename(os.path.join(path, fold), os.path.join(path, fnew))
        else:
            os.remove(os.path.join(path, fold))
    return True

def download_finance_zipfile(year, season):
    url = "https://mops.twse.com.tw/server-java/FileDownLoad?step=9&fileName=tifrs-"+str(year)+"Q"+str(season)\
            +".zip&filePath=/home/html/nas/ifrs/"+str(year)+"/"
    
    chunk_size = 1024
    r = requests.get(url, stream=True)
    with open("finance.zip", "wb") as f:
        for chunk in r.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
    return True

def unzip_finance_zipfile(path):
    with zipfile.ZipFile("finance.zip", "r") as zip_ref:
        zip_ref.extractall(path)
    return True



