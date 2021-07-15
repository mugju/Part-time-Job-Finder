# 해당 코드는 GUI와 크롤링 코드를 합치기 위함임.

import sys
import csv
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pandas as pd
import numpy as np 



#크롤링 함수관련
import albaheaven_crawl as albaHeaven
import albamon_crawl as albaMon

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("alba.ui")[0]


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
            albaHeaven.Heaven()
            self.loadCSV('albaheaven.csv')
            if self.checkBox.isChecked() :
                albaMon.Monster()
                df = pd.read_csv('albamon.csv',encoding='CP949')
                df2 = pd.read_csv('albaheaven.csv',encoding='cp949')
                df3 = df.append(df2)
                df3 = df3.drop_duplicates(['근무회사'], keep='first')  # 중복글에 대한 처리
                df3.to_csv('albamerge.csv', encoding='CP949', index=False)
                self.loadCSV('albamerge.csv')

        elif self.checkBox.isChecked() :
            albaMon.Monster()
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



if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()