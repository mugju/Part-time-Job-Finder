from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import numpy as np
import re

result = pd.DataFrame()  # 결과저장용 DataFrame
pagenum = 1

while(len(result) <= 100):  # 결과가 100개 넘어야 함.
    url = 'http://www.alba.co.kr/job/area/MainLocal.asp?page=argu&pagesize=50&viewtype=L&sidocd=031&gugun=%BD%C3%C8%EF%BD%C3,&dong=%C0%FC%C3%BC&d_area=&d_areacd=&strAreaMulti=031%7C%7C%BD%C3%C8%EF%BD%C3%7C%7C%C0%FC%C3%BC%2C&hidJobKind=&hidJobKindMulti=&WorkTime=&searchterm=&AcceptMethod=&ElecContract=&HireTypeCD=&CareerCD=&CareercdUnRelated=&LastSchoolCD=&LastSchoolcdUnRelated=&GenderCD=&GenderUnRelated=&AgeLimit=0&AgeUnRelated=&PayCD=&PayStart=&WelfareCD=&Special=&WorkWeekCD=&WeekDays=&hidSortCnt=50&hidSortOrder=&hidSortDate=&WorkPeriodCD=&hidSort=&hidSortFilter=Y&hidListView=LIST&WsSrchKeywordWord=&hidWsearchInOut=&hidSchContainText='
    url = url.replace('argu', str(pagenum))  # 페이지 1에대한 경우 이후 이는 변수로 처리할 것.
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')

    # crawltags = '#NormalInfo > table > tbody > tr:nth-child(1)'
    number = 1  # 99까지가 한페이지 사이클임
    while number < 99:
        title = soup.select_one(
            '#NormalInfo > table > tbody > tr:nth-child(%d)' % number)

        locations = re.sub(
            '<.+?>', '', str(title.select('td.local.first')), 0).strip()

        company = re.sub(
            '<.+?>', '', str(title.select('td.title > a > span.company')), 0).strip()

        time = re.sub('<.+?>', '', str(title.select('td.data')), 0).strip()

        paymethod = re.sub('<.+?>', '', str(title.select('td.pay')), 0).strip()

        regdate = re.sub(
            '<.+?>', '', str(title.select('td.regDate.last')), 0).strip()

        df = pd.DataFrame([[locations, company, time, paymethod, regdate]], columns=[
                          '지역', '근무회사', '근무시간', '급여', '올린시간'])
        number += 2  # 다음꺼 접근해야지
        if paymethod.find("월급")== 1 or paymethod.find("연봉") == 1:
            print("cut!!")
            continue  # 월급준다는 거면 일단 제끼기 알바가 아닐 확률이 높기 때문임.
        else:
            result = result.append(df)

    result = result.drop_duplicates(['근무회사'], keep='first')
    print(result)
    print(len(result))

    pagenum = pagenum + 1

    #후처리로 drop_duplicate 사용해서 중복되는 것들 제거할 것

#to_csv'
result.to_csv('albaheaven.csv', encoding='CP949', index=False)
