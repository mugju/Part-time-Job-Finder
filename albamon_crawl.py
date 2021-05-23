
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import numpy as np
import re
import requests

session = requests.Session()

title = [] #알바title = [] #알바 제목

result = pd.DataFrame(columns=['근무지역', '근무회사', '근무시간','급여','올린시간','알바설명'])  # 결과저장용 DataFrame

area_list = []
cName_list = []
cTit_list = []
pay_list = []
time_list = []
recently_list = []

pagenum = 1 #첫 페이지
while(pagenum < 2):  #n개 페이지에 대하여 크롤링
    url = 'https://www.albamon.com/list/gi/mon_area_list.asp?page=1&ps=20&ob=6&lvtype=1&rArea=,B210&rWDate=1&Empmnt_Type=' #이건 알바천국
    url = url.replace('argu', str(pagenum))  # 페이지 1에대한 경우 이후 이는 변수로 처리할 것.

    pagenum = pagenum + 1 #다음페이지 준비
    page = session.get(url)
    c = page.content
    soup = BeautifulSoup(c, 'html.parser')
    title_ = soup.find_all('td')
    conte = soup.select_one('#subcontent > form > div.gListWrap > table > tbody')
    
    #지역관련 크롤링
    area = conte.select('td.area')
    for ww in area:
        area_list.append(ww.get_text().strip().replace('스크랩\n',"")) #지역리스트 데이터 추가함
        #print(ww.get_text().strip().replace('스크랩\n',""))
        
    #==================================================================

    #알바 제목
    cName = conte.select('td.subject > div.subWrap > p.cName')
    for ww in cName:
        cName_list.append(ww.get_text())
        #print(ww.get_text())

    #==================================================================
    #내용

    cTit = conte.select('td.subject > div.subWrap > p.cTit')
    for ww in cTit:
        cTit_list.append(ww.get_text())
        #print(ww.get_text())
 


    #===================================================
    #급여
    pay = conte.select('td.pay')
    #지급방식은 돈의 범위로 한다.
    #시급 일급 월급으로 
    for ww in pay:
        pay_list.append(ww.get_text().strip())
        #print(ww.get_text().strip())


    #==================================================
    #근무시간
    time = conte.select('td:nth-child(4)')
    for ww in time:
        time_list.append(ww.get_text().strip())
        #print(ww.get_text().strip())


    #================================================
    #올린시간
    recently = conte.select('td.recently > em')
    for ww in recently:
        recently_list.append(ww.get_text().strip())
        #print(ww.get_text().strip())



# area_list = []
# cName_list = []
# cTit_list = []
# pay_list = []
# time_list = []
# recently_list = []

print(area_list)
print(time_list)
# result = pd.DataFrame(columns=['근무지역', '근무회사', '근무시간','급여','올린시간','알바설명'])  # 결과저장용 DataFrame
result['근무지역'] = area_list
result['근무회사'] = cName_list
result['근무시간'] = time_list
result['급여시간'] = pay_list
result['올린시간'] = recently_list
result['알바설명'] = cTit_list

print(result)