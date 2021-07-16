# 해당 코드는 GUI와 크롤링 코드를 합치기 위함임.
# -*- coding: utf-8 -*-

import sys
import csv
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import pandas as pd

seoul_list = ['강남구','강동구', '강북구' , '강서구' ,'관악구','광진구' , '구로구', '금천구' , '노원구', '도봉구', '동대문구', '동작구', '마포구' , '서대문구' , '서초구', '성동구', '성북구', '송파구' , '양천구' , '영등포구' , '용산구' , '은평구' , '종로구' , '중구' , '중랑구']

list_file_s = open('albaheaven_seoul_url.txt', 'r',encoding='utf-8').read().split('\n')
heaven_Seoul = dict(zip(seoul_list,list_file_s))  #알바천국 서울지역 딕셔너리

seoul_Mon_code = ['I010','I020','I030','I040','I050','I060','I070','I080','I090','I100','I110','I120','I130','I140','I150','I160','I170','I180','I190','I200','I210','I220','I230','I240','I250',]
mon_Seoul = dict(zip(seoul_list,seoul_Mon_code))  #알바몬 경기도지역 지역코드



gyeongki_list = ['가평군' ,'고양시 덕양구' ,'고양시 일산동구','고양시 일산서구' ,'과천시' ,'광명시' ,'광주시' ,'구리시' ,'군포시' ,'김포시' ,'남양주시' ,'동두천시' ,'부천시' ,'성남시 분당구' ,'성남시 수정구' ,'성남시 중원구' ,'수원시 권선구' ,'수원시 영통구' ,'수원시 장안구', '수원시 팔달구' ,'시흥시' ,'안산시 단원구' ,'안산시 상록구' ,'안성시', '안양시 동안구' ,'안양시 만안구' ,'양주시' ,'양평군' ,'여주시', '연천군' ,'오산시',' 용인시 기흥구' ,'용인시 수지구', '용인시 처인구' ,'의왕시', '의정부시' ,'이천시' ,'파주시' ,'평택시' ,'포천시', '하남시' ,'화성시']

list_file = open('albaheaven_url_list.txt', 'r',encoding='utf-8').read().split('\n')
heaven_Gyeong = dict(zip(gyeongki_list,list_file))  #알바천국 경기도지역 딕셔너리

gyeongki_Mon_code = ['B010','B020','B030','B031','B040','B050','B060','B070','B080','B090','B100','B110','B125','B150','B160','B170','B180','B201','B190','B200','B210','B220','B221','B230','B240','B250','B260','B270','B280','B290','B300','B310','B311','B312','B320','B330','B340','B350','B360','B370','B380','B390']
mon_Gyeong = dict(zip(gyeongki_list,gyeongki_Mon_code))  #알바몬 경기도지역 지역코드

#크롤링 함수관련
import albaheaven_crawl as albaHeaven
import albamon_crawl as albaMon

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("alba.ui")[0]


# #쓰레드 선언
# class Thread_run(QThread):
#     #parent = MainWidget을 상속 받음.
#     def __init__(self, parent):
#         super().__init__(parent)
#     def run(self):
#         albaHeaven.Heaven()



#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        #테이블관련 초기화 셋팅
        # table 위젯의 컬럼을 6개로 설정
        self.tableWidget.setColumnCount(6)

        #컬럼명 지정
        self.tableWidget.setHorizontalHeaderLabels(["지역", "근무회사", "근무시간", "급여", "올린시간", "알바설명"])

        
        
        
        # QCombox 생성 및 아이템 추가 
 
        #self.comboBox = QComboBox(self)
        self.comboBox.addItem('경기')
        self.comboBox.addItem('서울')
        self.comboBox.addItem('인천')
        # 선택되면 두번째 콤보박스의 내용이 바뀜
        self.comboBox.activated[str].connect(lambda :self.selectedComboItem(self.comboBox))
        
        self.comboBox.move(40,580)
        self.comboBox_2.clear()

        
 
        self.show()




        #버튼에 기능을 연결하는 코드
        self.Crawl_start.clicked.connect(self.Crawl_start_btn)

        #알바몬만 확인
        self.onlyMon.clicked.connect(self.onlyMon_btn)
        self.onlyHeaven.clicked.connect(self.onlyHeaven_btn)

        self.albaMerge.clicked.connect(self.albaMerge_btn)

    ### CSV 파일의 경로를 파라미터로 넘겨주면 table 위젯에 공유정보 출력 메서드 ###
    def loadCSV(self, csvPath):
        shareCSV = open(csvPath, 'r', encoding='CP949')
        shareObject = csv.reader(shareCSV)
        enumerate(shareObject)
        for row, line in enumerate(shareObject):
            if row == 0 : continue
            self.tableWidget.setRowCount(row+1)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(line[0]))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(line[1]))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(line[2]))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(line[3]))
            self.tableWidget.setItem(row, 4, QTableWidgetItem(line[4]))
            self.tableWidget.setItem(row, 5, QTableWidgetItem(line[5]))


        ## 테이블 크기 자동조절
        table = self.tableWidget
        header = table.horizontalHeader()

        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)

        


        

    #크롤링 시작이 눌리면 작동할 함수
    def Crawl_start_btn(self) :
        if self.checkBox_2.isChecked() :
            if self.comboBox.currentText() == '경기': albaHeaven.Heaven(heaven_Gyeong[self.comboBox_2.currentText()])
            if self.comboBox.currentText() == '서울': albaHeaven.Heaven(heaven_Seoul[self.comboBox_2.currentText()])
            self.loadCSV('albaheaven.csv')
            if self.checkBox.isChecked() :
                if self.comboBox.currentText() == '경기': albaMon.Monster(mon_Gyeong[self.comboBox_2.currentText()])
                if self.comboBox.currentText() == '서울': albaMon.Monster(mon_Seoul[self.comboBox_2.currentText()])
                df = pd.read_csv('albamon.csv',encoding='CP949')
                df2 = pd.read_csv('albaheaven.csv',encoding='cp949')
                df3 = df.append(df2)
                df3 = df3.drop_duplicates(['근무회사'], keep='first')  # 중복글에 대한 처리
                df3.to_csv('albamerge.csv', encoding='CP949', index=False)
                self.loadCSV('albamerge.csv')

        elif self.checkBox.isChecked() :
            if self.comboBox.currentText() == '경기': albaMon.Monster(mon_Gyeong[self.comboBox_2.currentText()])
            if self.comboBox.currentText() == '서울': albaMon.Monster(mon_Seoul[self.comboBox_2.currentText()])
            self.loadCSV('albamon.csv')


        print("albaheaven run")


    #알바몬만 검색이 눌리면 작동할 함수
    def onlyMon_btn(self) :
        self.loadCSV('albamon.csv')
        print("albaMon Clicked")


    def onlyHeaven_btn(self) :
        self.loadCSV('albaheaven.csv')
        print("albaHeaven Clicked")
        

    def albaMerge_btn(self) :
        self.loadCSV('albamerge.csv')
        print("albaHeaven Clicked")


    ### 콤보박스 관련 함수
    def selectedComboItem(self,text):
    
        print(text.currentText())
        if text.currentText() == '서울':
            print("1")
            # seoul list
            
    
            # adding list of items to combo box
            self.comboBox_2.clear()
            self.comboBox_2.addItems(seoul_list)

        if text.currentText() == '경기':
            print("1")
            # seoul list
            
    
            # adding list of items to combo box
            self.comboBox_2.clear()
            self.comboBox_2.addItems(gyeongki_list)
        


if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()