
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd

import re



def Heaven(url) :
    result = pd.DataFrame()  # 결과저장용 DataFrame
    pagenum = 1
    #print(url)

    while(len(result) <= 70 ):  # 결과가 100개 넘어야 함. 아니면 진짜 없어서 15번 돌려도 없을때
        #url = 'http://www.alba.co.kr/job/area/MainLocal.asp?page=argu&pagesize=50&viewtype=L&sidocd=031&gugun=%BD%C3%C8%EF%BD%C3,&dong=%C0%FC%C3%BC&d_area=&d_areacd=&strAreaMulti=031%7C%7C%BD%C3%C8%EF%BD%C3%7C%7C%C0%FC%C3%BC%2C&hidJobKind=&hidJobKindMulti=&WorkTime=&searchterm=&AcceptMethod=&ElecContract=&HireTypeCD=&CareerCD=&CareercdUnRelated=&LastSchoolCD=&LastSchoolcdUnRelated=&GenderCD=&GenderUnRelated=&AgeLimit=0&AgeUnRelated=&PayCD=&PayStart=&WelfareCD=&Special=&WorkWeekCD=&WeekDays=&hidSortCnt=50&hidSortOrder=&hidSortDate=&WorkPeriodCD=&hidSort=&hidSortFilter=Y&hidListView=LIST&WsSrchKeywordWord=&hidWsearchInOut=&hidSchContainText='
        url_new = url.replace('argu', str(pagenum))  # 페이지 1에대한 경우 이후 이는 변수로 처리할 것.
        print(pagenum)
        print(url_new)
        html = urllib.request.urlopen(url_new)
        soup = BeautifulSoup(html, 'html.parser',from_encoding='cp949')
        if(pagenum == 15) : break

        # crawltags = '#NormalInfo > table > tbody > tr:nth-child(1)'
        number = 1  # 99까지가 한페이지 사이클임
        while number < 99:
            title = soup.select_one(
                '#NormalInfo > table > tbody > tr:nth-child(%d)' % number)
            
            #뭐지 타입 논으로뜨는거 예외처리 해주자.
            if str(type(title)) == "<class 'NoneType'>" : break

            #근무지역에 대한 컬럼
            locations = str(re.sub(
                '<.+?>', '', str(title.select('td.local.first')), 0).strip())
            locations = locations.replace('[' , '')
            locations = locations.replace(']' , '')
            company = re.sub(
                '<.+?>', '', str(title.select('td.title > a > span.company')), 0).strip()
            company = company.replace('[' , '')
            company = company.replace(']' , '')
            
            #근무시간에 대한 컬럼
            time = re.sub('<.+?>', '', str(title.select('td.data')), 0).strip()
            time = time.replace('[' , '')
            time = time.replace(']' , '')

            #급여에 대한 컬럼
            paymethod = re.sub('<.+?>', '', str(title.select('td.pay')), 0).strip()
            paymethod = paymethod.replace('[' , '')
            paymethod = paymethod.replace(']' , '')
            #올린시간에 대한 컬럼
            regdate = re.sub(
                '<.+?>', '', str(title.select('td.regDate.last')), 0).strip()

            regdate = regdate.replace('[' , '')
            regdate = regdate.replace(']' , '')
            #알바설명에 대한 컬럼
            info= re.sub(
                '<.+?>', '', str(title.select('td.title > a > span.title')), 0).strip()

            info = info.replace('[' , '')
            info = info.replace(']' , '')

            df = pd.DataFrame([[locations, company, time, paymethod, regdate, info]], columns=[
                            '지역', '근무회사', '근무시간', '급여', '올린시간','알바설명'])
            number += 2  # 다음꺼 접근해야지
            # 알바가 아닌 직원을 구하는 글에대한 필터링 작업 이거에 대해서 삭제작업 추가해야함.
            if paymethod.find("월급") == 1 or paymethod.find("연봉") == 1:
                print("cut!!")
                # idx = result[result['급여형태']>1800000].index
                # result = result.drop(idx)
                continue  # 월급준다는 거면 일단 제끼기 알바가 아닐 확률이 높기 때문임.
            else:
                result = result.append(df)

        result = result.drop_duplicates(['근무회사'], keep='first')  # 중복글에 대한 처리
        
        
        result['순서'] = range(len(result))
        result = result.set_index('순서')
        print(len(result))
        
        idx = result[result['급여'].str.contains('월급')].index ## df[조건식]
        result = result.drop(idx)
        idx = result[result['급여'].str.contains('연봉')].index ## df[조건식]
        result = result.drop(idx)

        #없앴으니까 다시 인덱싱 해주기
        result['순서'] = range(len(result))
        result = result.set_index('순서')

        pagenum = pagenum + 1
        print(result)

        #후처리로 drop_duplicate 사용해서 중복되는 것들 제거할 것

    #to_csv' 인덱스는 제거할 것
    result.to_csv('albaheaven.csv', encoding='CP949', index=False)
    #return 0



if __name__ == "__main__":
    gyeonggi_list = ['가평군' ,'고양시 덕양구' ,'고양시 일산동구','고양시 일산서구' ,'과천시' ,'광명시' ,'광주시' ,'구리시' ,'군포시' ,'김포시' ,'남양주시' ,'동두천시' ,'부천시' ,'성남시 분당구' ,'성남시 수정구' ,'성남시 중원구' ,'수원시 권선구' ,'수원시 영통구' ,'수원시 장안구', '수원시 팔달구' ,'시흥시' ,'안산시 단원구' ,'안산시 상록구' ,'안성시', '안양시 동안구' ,'안양시 만안구' ,'양주시' ,'양평군' ,'여주시 연천군' ,'오산시',' 용인시 기흥구' ,'용인시 수지구', '용인시 처인구' ,'의왕시 의정부시' ,'이천시' ,'파주시' ,'평택시' ,'포천시', '하남시' ,'화성시']
    list_file = open('albaheaven_url_list.txt', 'r',encoding='utf-8').read().split('\n')
    output = dict(zip(gyeonggi_list,list_file))
    #output['시흥시']
    Heaven(output['과천시'])