#crawl https://index.ndc.gov.tw
#

import pandas as pd
import requests
import datetime
from fake_useragent import UserAgent

datebases = {'eco/indicators':'id=13,14,15,16,17,18,19,20,21,25,26,27,29,30,31,32,33,34,35,36,37,38,39,277',
            'eco/index':'id=13,14,15,16,17,18,19,20,21,25,26,27,29,30,31,32,33,34,35,36,37,38,39,277',
            'eco/signal':'id=7_light,12_data,12_light,15_data,15_light,17_data,17_light,18_data,18_light,19_data,19_light,20_data,20_light,21_data,21_light,36_data,36_light,37_data,37_light',
            'PMI/industry':'id=70,85,100,115,130,145&id1=0,1,2,3,4,5,6,7,8,9,10,11',
            'PMI/total':'id=55,56,57,58,59,60,61,62,63,64,65,66',
            'NMI/total':'id=160,161,162,163,164,165,166,167,168,169,170,171,172',
            'NMI/industry':'id=173,186,199,212,225,238,251,264&id1=0,1,2,3,4,5,6,7,8,9,10,11,12'}
for key in datebases:
        economic_indicator(datebases,datebases[key])

def economic_indicator(datebase,ID):
    '''Crawl economic indicator from https://index.ndc.gov.tw
    Args:
        datebase (str): datebase name
        ID (str): ID of economic indicator
    Returns:
        pd.DataFrame: economic indicator
        '''
    ref = f'https://index.ndc.gov.tw/n/excel/data/{datebase}?'
    start_year  = f'sy=2014'
    start_mom   = f'sm=1'
    end_year    = f'ey={str(datetime.datetime.now().year)}'
    end_mom     = f'em={str(datetime.datetime.now().month)}'
    SQ          = f'sq=0,0,0'
    url         = f'{ref}{start_year}&{start_mom}&{end_year}&{end_mom}&{ID}&{SQ}'

    ua = UserAgent()
    req = requests.get(url , headers={'user-agent' : ua.random})
    df = pd.read_html(req.text)[0]
    df.to_csv(f'{datebase}.csv', index=False)

    
