import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

from Opinion.ToDatabas import *
from fake_useragent import UserAgent

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from datetime import datetime



def crawler(table_name): #主要程式

    end_page = new_page(table_name) #取得最新頁面    
    DB=DataBase(table_name=table_name)
    start_page=DB.table_date_range()
    if start_page==[None, None]:
        start_page=round(end_page/1.5)    

    for page in range(start_page, end_page, 1):
        print(page)
        url = f'https://www.ptt.cc/bbs/{table_name}/index{page}.html'
        links = links_list(url) #取得所有連結
        df = content_cralwer(links)
        df['date'] = page
        DB.Mongodb(df=df)


def StartPage(table_name):

    df = pd.read_csv(os.path.join('Datasource',f'{table_name}.csv'))
    
    df.reset_index(drop = True, inplace = True)
    start_page = df['頁數'].sort_values(ascending = False).reset_index(drop = True)[0]
    return start_page



def content_cralwer(links):

    artical_list = []
    final_content_message = []

    for artical in links:
        # artical = links[0]
        try:
            cookies = {'over18':'1'}
            ua = UserAgent()
            user_agent = ua.google
            headers = {'user-agent' : user_agent}
            req = requests.get(artical,cookies=cookies,headers = headers).text
            soup = BeautifulSoup(req,'html.parser')

            top_scope = soup.find_all('span' ,class_ = "article-meta-value")
            classfy = top_scope[2].text.split(']')[0].replace('[',"").replace('Re:',"").replace(' ',"") #取得分類，用來篩選需要的類別
            author = top_scope[0].text  #取得作者
            board = top_scope[1].text #取得版名
            tital = top_scope[2].text #取得標題
            # date = top_scope[3].text #取得日期
            date = datetime.strptime(top_scope[3].text, "%a %b %d %H:%M:%S %Y")  # 取得日期
            artical_list.append([board,classfy,author,tital,date,artical]) #合併進List，後續做DataFrame
            print(tital) #顯示爬取進度
            

            #爬取內文
            content =str(soup.find('div' ,id = 'main-container')).split('</span></div>\n')[1].split('※ 發信站')[0] #取得文章內容，後續用於jieba_fast切詞
            #爬取留言
            message = soup.find('div' ,id = 'main-container').find_all('div' ,class_="push")
            content_message = message_content(message)  #取得留言，後續用於jieba_fast切詞
            final_content_message.append([content,content_message]) #合併進List

        except:
            pass

    df1 = pd.DataFrame(artical_list,columns=['版名','分類','作者','標題','日期','url']) #命名主要欄位
    df2 = pd.DataFrame(final_content_message,columns=['內容','留言']) #命名切詞用欄位
    df3 = pd.concat([df1,df2],axis = 1) #橫向合併

    return df3




def new_page(table_name): #用於取得最新頁面
    
    if IsIndocker():
        driver = webdriver.Remote('http://selenium:4444/wd/hub',desired_capabilities=DesiredCapabilities.CHROME)
    else:
        driver = webdriver.Chrome()
    driver.get(f"https://www.ptt.cc/bbs/{table_name}/index.html")
    try:
        driver.find_element(By.NAME, "yes").click()
    except:
        pass
    driver.find_element(By.LINK_TEXT, "‹ 上頁").click() #為了顯示頁面
    new_page = driver.current_url
    new_page=int(new_page.split('/')[5].replace('index','').replace('.html','')) + 1
    # print(new_page)
    driver.quit()

    return new_page



def links_list(url): #取得PTT所有連結
    cookies = {'over18':'1'}
    req = requests.get(url,cookies=cookies).text
    soup = BeautifulSoup(req,'html.parser')

    links = []
    for i in soup.find_all('div' ,class_ = 'title'):
        try:
            links.append('https://www.ptt.cc'+i.find('a' ,href = True).get('href'))
        except:
            pass
    return links




def message_content(message):
    
    message_content = []
    for i in message:
        try:
            push_tag = i.find('span' ,class_=re.compile('hl push-tag')).text #取得"推" "噓" "中立"
            push_userid = i.find('span' ,class_=re.compile('f3 hl push-userid')).text #留言名稱
            push_content = i.find('span' ,class_=re.compile('f3 push-content')).text #留言內容
            push_ipdatetime = i.find('span' ,class_=re.compile('push-ipdatetime')).text #留言IP、日期、時間
            message_content.append([push_tag,push_userid,push_content,push_ipdatetime])
            
        except:
            pass
        
    attrs = ['type','user','content','ipdatetime']

    msgs = []
    for msg in message_content: 
        msgs.append(dict(zip(attrs,list(msg))))  #把留言內容塞進list，並轉成文字，也利於資料永久存放

    return str(msgs) 


















 





