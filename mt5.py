import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm , trange
import time

colum={'url':[],'name':[]}


def pg(URL):
    r=requests.get(URL)
    time.sleep(2)
    soup=BeautifulSoup(r.content,"html.parser")
    if soup.find('div',{'class':'paginatorEx'})==None:
        return 1
    else:
        ancher=soup.find('div',{'class':'paginatorEx'}).find_all('a')
        finpag=int(ancher[-1].text)
        return finpag

page=int(pg("https://www.mql5.com/en/signals/mt5/list"))+1
with tqdm(total=100) as pbar:
    for i in range(1,page):
        url="https://www.mql5.com/en/signals/mt5/list/page"+str(i)
        r=requests.get(url)
        soup=BeautifulSoup(r.content,"html.parser")
        ancher=soup.find('div',{'class':'signals-table'}).find_all('div',{'class':'row signal'})
        for pt in ancher:
            hr=pt.find('div',{'class':'col-chart'}).find('div',{'class':'signal-chart'}).find('a',{'class':'signal-avatar'})
            colum['url'].append(hr.get('href'))
            name=hr.find('span',{'class':'name'})
            colum['name'].append(name.text)
        pbar.update(100//page)
    data=pd.DataFrame(colum)
    data.to_excel('mt5.xlsx')