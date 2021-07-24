
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

import pandas as pd
import requests

def Monster(local):
    
    session = requests.Session()

    title = [] #알바title = [] #알바 제목

    result = pd.DataFrame(columns=['지역', '근무회사', '근무시간','급여','올린시간','알바설명'])  # 결과저장용 DataFrame
    new_df = pd.DataFrame(columns=['지역', '근무회사', '근무시간','급여','올린시간','알바설명'])  # append용 DataFrame


    pagenum = 1 #첫 페이지
    try:
        while(len(result) <80):  #n개 페이지에 대하여 크롤링
            print(pagenum)
            if(pagenum == 25) : break #과도한 접속 방지
            # 리스트 초기화
            area_list = []
            cName_list = []
            cTit_list = []
            pay_list = []
            time_list = []
            recently_list = []
            url = 'https://www.albamon.com/list/gi/mon_area_list.asp?page=argu&ps=50&ob=6&lvtype=1&rArea=,AREACODE&rWDate=1&Empmnt_Type=' #이건 알바천국
            url = url.replace('AREACODE', str(local))  # 지역 코드.
            url = url.replace('argu', str(pagenum))  # 페이지 1에대한 경우 이후 이는 변수로 처리할 것.

            pagenum = pagenum + 1 #다음페이지 준비
            page = session.get(url)
            c = page.content
            soup = BeautifulSoup(c, 'html.parser')
            title_ = soup.find_all('td')
            conte = soup.select_one('#form > div.listType-normal > div.gListWrap > table > tbody')
            
            #지역관련 크롤링
            area = conte.select('td.area')
            for ww in area:
                area_list.append(ww.get_text().strip().replace('스크랩\n',"")) #지역리스트 데이터 추가함
                #print(ww.get_text().strip().replace('스크랩\n',""))
                
            #==================================================================

            #알바 제목
            cName = conte.select('td.subject > div.subWrap > p.cName')
            for ww in cName:
                cName_list.append(ww.get_text().replace('\n',''))
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

            #태그의 변화 날짜는 못받아오더라
            recently_ = conte.select('td.recently')
            print(recently_)
            for ws in recently_:
                recently_list.append(ws.get_text())

            print(recently_list)

            new_df = pd.DataFrame()
            
            new_df['지역'] = area_list
            new_df['근무회사'] = cName_list
            new_df['근무시간'] = time_list
            new_df['급여'] = pay_list
            print(url)
            new_df['올린시간'] = recently_list
            new_df['알바설명'] = cTit_list    
            #print(new_df)


            result = pd.concat([result,new_df])
            result = result.drop_duplicates(['근무회사'], keep='first')  # 중복글에 대한 처리
            
            print(result)
            
            #급여 컬럼에 교육 연수생들어간거 삭제해야함.
            idx = result[result['급여'] == '교육 · 연수생'].index
            result = result.drop(idx)

            #여기 부터 월급형태의 지급알바를 제거함. 이는 알바가 아닌 정직원을 모집하는 것이기 때문
            
            result["급여형태"] = result["급여"].str.replace(',','')
            result["급여형태"] = result["급여형태"].str.replace('원','')
            result = result.astype({"급여형태":int})
            idx = result[result['급여형태']>1500000].index
            result = result.drop(idx)

            result['순서'] = range(len(result))
            result = result.set_index('순서')
            
            #[다시 급여형태 컬럼을 삭제해 주어야 함.]
            result = result.drop(['급여형태'], axis=1)
            print(len(result))


        result.to_csv('albamon.csv', encoding='CP949', index=False)


        print(result)
    finally: # 페이지가 없는 경우
        print("알바몬 인증에러")
        #result.to_csv('albamon.csv', encoding='CP949', index=False)



if __name__ == "__main__":
	Monster('B010')