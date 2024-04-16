from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# 크롤링 모듈
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains

from app.models import Hotkeywords
from app.models import Dailykeyword
from django.db.models import F
from datetime import datetime

import os

#데이터 분석
from collections import Counter
from konlpy.tag import Hannanum, Okt

class CrawlingRouter(APIView):
    def get(self, request):
        return Response({'success':True})
    

    #데이터 분석
    def WordParsing(self,news_data):
        okt = Okt() #twitter 형태소 분석기: 속도가 중요하고, 대량의 텍스트 데이터를 다루는 경우에 유용함.
        
        nouns_list =[]
        for i in range(len(news_data)):
            #무의미한 문자 삭제
            data = news_data[i]
            
            replace_list = ["‘","’","”","“",'"',"'","[포토]","[사설]","[CarTalk]","...","…","[단독]"]
            for j in replace_list:
                data = data.replace(j, "")
            

            nouns = okt.nouns(data)
            nouns_list += nouns
            
        nouns_list = [x for x in nouns_list if len(x)>1] #한 글자 삭제

        counter = Counter(nouns_list)
        result = counter.most_common(10) #상위 10개 데이터
        
        return result


            
    #크롤링(데이터 가져오기)
    def post(self, request):
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 백그라운드에서 실행
        
        Hotkeywords.objects.all().delete() # 원래 데이터 삭제
        
        #크롬 실행
        with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options) as driver:            
            #언론사 뉴스 홈-> 경향신문(첫번째)
            driver.get("https://news.naver.com/main/officeList.naver")
            button = driver.find_element(By.XPATH, '//*[@id="groupOfficeList"]/table/tbody/tr[1]/td/ul/li[1]/a')
            ActionChains(driver).click(button).perform()
            driver.implicitly_wait(5)
            
            news_data=[]
            #버튼으로 언론사 페이지네이션
            for i in range(2,11): 
                button = driver.find_element(By.XPATH, '//*[@id="main_content"]/div[1]/div/div/ul/li[{}]/a'.format(i))
                ActionChains(driver).click(button).perform()
                driver.implicitly_wait(10)
                
                #요약기사(첫 페이지기사만)
                #ul[1]
                for i in range(1, 11): #첫 페이지 앞단 10개까지있음
                    element = driver.find_element(By.XPATH,'//*[@id="main_content"]/div[2]/ul[1]/li[{}]/dl/dt[last()]/a'.format(i))
                    news_data.append(element.text)
                #ul[2]
                for i in range(1, 11): #첫 페이지 뒷단 10개까지있음
                    element = driver.find_element(By.XPATH,'//*[@id="main_content"]/div[2]/ul[2]/li[{}]/dl/dt[last()]/a'.format(i))    
                    news_data.append(element.text)

            #형태소 분석 -> 결과 이미지 저장 경로(해야할 일: 메인 서버 DB로 경로 바꾸기)   
            counter_data = self.WordParsing(news_data)


            #DB에 저장
            for i in range(10):
                keyword_text = counter_data[i][0]
                count = counter_data[i][1]

                # 오늘 날짜를 가져옵니다.
                today = datetime.now().date()
                
                # 오늘 날짜에 해당하는 Dailykeyword 레코드가 이미 존재하는지 확인합니다.
                existing_record = Dailykeyword.objects.filter(keyword_text=keyword_text, keyword_date__date=today).first()
                
                if existing_record:
                    # 이미 존재하는 레코드가 있다면 count를 업데이트 합니다.
                    existing_record.count = F('count') + count
                    existing_record.save()
                else:
                    # 존재하지 않는다면 새로운 레코드를 생성합니다.
                    Dailykeyword.objects.create(
                        keyword_text=keyword_text,
                        count=count
                    )
                Hotkeywords.objects.create(
                    keyword_text=keyword_text,
                    count=count
                )

            return Response({'counter_data':counter_data})