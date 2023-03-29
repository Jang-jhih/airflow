import requests
import zipfile
import urllib.request
import os
import shutil

def check_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)
def get_season(date):
    '''
    Get the season of the specified date.
    Parameters
    ----------
    date : datetime.date
        The date.
    Returns
    -------
    int
        The season of the specified date.
    '''
    year = date.year
    if date.month == 3:
        season = 4
        year = year - 1
        month = 11
    elif date.month == 5:
        season = 1
        month = 2
    elif date.month == 8:
        season = 2
        month = 5
    elif date.month == 11:
        season = 3
        month = 8
    else:
        return None

def download_finance_statement(year, season):
    '''
    Download the financial statement of the specified year and season.
    Parameters
    ----------
    year : int
        The year of the financial statement.
        season : int
        The season of the financial statement.
    Returns
    -------
    bool
        True if the financial statement is downloaded successfully.
        False if the financial statement is not downloaded successfully.
    '''

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
    '''
    Download the financial statement of the specified year and season.
    Parameters
    ----------
    year : int
        The year of the financial statement.
        season : int
        The season of the financial statement.
    Returns
    -------
        bool
        True if the financial statement is downloaded successfully.
        False if the financial statement is not downloaded successfully.
        '''
    # url = "https://mops.twse.com.tw/server-java/t164sb01?step=1&CO_ID=1101&SYEAR=2019&SSEASON=1&REPORT_ID=C"
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



# if __name__ == "__main__":
#     download_finance_statement(2019, 1)
