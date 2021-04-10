from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import re

result = []  # 결과를 저장할 list
url = 'http://www.alba.co.kr/job/area/MainLocal.asp?page=argu&pagesize=50&viewtype=L&sidocd=031&gugun=%BD%C3%C8%EF%BD%C3,&dong=%C0%FC%C3%BC&d_area=&d_areacd=&strAreaMulti=031%7C%7C%BD%C3%C8%EF%BD%C3%7C%7C%C0%FC%C3%BC%2C&hidJobKind=&hidJobKindMulti=&WorkTime=&searchterm=&AcceptMethod=&ElecContract=&HireTypeCD=&CareerCD=&CareercdUnRelated=&LastSchoolCD=&LastSchoolcdUnRelated=&GenderCD=&GenderUnRelated=&AgeLimit=0&AgeUnRelated=&PayCD=&PayStart=&WelfareCD=&Special=&WorkWeekCD=&WeekDays=&hidSortCnt=50&hidSortOrder=&hidSortDate=&WorkPeriodCD=&hidSort=&hidSortFilter=Y&hidListView=LIST&WsSrchKeywordWord=&hidWsearchInOut=&hidSchContainText='
url = url.replace('argu', '1')  # 페이지 1에대한 경우 이후 이는 변수로 처리할 것.
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, 'html.parser')

#crawltags = '#NormalInfo > table > tbody > tr:nth-child(1)'
number = 1  # 99까지가 한페이지 사이클임
while number < 99:
    title = soup.select_one(
        '#NormalInfo > table > tbody > tr:nth-child(%d)' % number)

    locations = re.sub('<.+?>', '', str(title.select('td.local.first')), 0).strip()
    print(locations)  # 동네 잘나옴.

    company = re.sub(
        '<.+?>', '', str(title.select('td.title > a > span.company')), 0).strip()
    print(company)

    time = re.sub('<.+?>', '', str(title.select('td.data')), 0).strip()
    print(time)

    paymethod = re.sub('<.+?>', '', str(title.select('td.pay')), 0).strip()
    print(paymethod)

    regdate = re.sub('<.+?>', '', str(title.select('td.regDate.last')), 0).strip()
    print(regdate)

    number += 2
