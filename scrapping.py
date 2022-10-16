from distutils.filelist import findall
from gettext import gettext
from inspect import classify_class_attrs
from lib2to3.pgen2.pgen import DFAState
from operator import index
from os import remove
from bs4 import BeautifulSoup
import requests
import datetime as dt
from datetime import datetime
from datetime import date
from datetime import timedelta

def pulls():
    html_text=requests.get('https://github.com/pandas-dev/pandas/pulls').text
    soup=BeautifulSoup(html_text,'lxml')
    a=[]
    dates=[]
    pull_req=[]
    pull_id=[]
    authors=[]
    time=datetime.now()
    #time=time.strftime('%b %d, %Y')
    for i in range(10):
        alldays=(time - timedelta(days=i)).date()
        d = alldays.strftime("%b %d, %Y")
        dates.append(d)

    jobs=soup.find_all('div',class_='Box-row Box-row--focus-gray p-0 mt-0 js-navigation-item js-issue-row')
    for job in jobs:
        request_pull=job.find('a',class_='Link--primary v-align-middle no-underline h4 js-navigation-open markdown-title').text 
        print('pull_request:',request_pull)
        pull_req.append(request_pull)
        id=job.find('span',class_='opened-by').text
        #print('id:',id)
        pull_id.append(id)
        date=job.find('relative-time',class_='no-wrap').text
        '''for i in date:
            if date not in a:
                a.append(date)
                authors.append(date)'''
        author=job.find('a',class_='Link--muted').text
        authors.append(author)
        a.append(author)


        #print('authors:',authors)

        print()
    #print(a)
    #print(dates)


    print(authors)
    print()
    print()
    print(pull_req)
    import pandas as pd
    df=pd.DataFrame(list(zip(authors, pull_req)),
               columns =['Author name', 'pull_request'])
    print(df)
    #print(pull_id)
    from itertools import islice
    import numpy as np

    result = [i for i, e in enumerate(a) if e in dates]
    result=np.diff(result)
    def getSublists(lst,lens):
        iter_lst = iter(lst)
        return [list(islice(iter_lst, x)) for x in lens]
    final=getSublists(a,result)
    #for i in final:
        #print(i)

pulls()

