from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from rest_framework.views import APIView
from rest_framework.response import Response

# 크롤링 모듈
import requests
from lxml import html

from app.models import Hotkeywords
from app.models import Dailykeywords
from django.db.models import F
from datetime import datetime

import os

#데이터 분석
from collections import Counter
from konlpy.tag import  Okt, Hannanum


class CrawlingRouter(APIView):
    def get(self, request):
        return Response({'success':True})
    

    #데이터 분석
    def WordParsing(self,news_data):
        # okt = Okt() #twitter 형태소 분석기: 속도가 중요하고, 대량의 텍스트 데이터를 다루는 경우에 유용함.
        hannanum = Hannanum()
        nouns_list =[]
        for i in range(len(news_data)):
            #무의미한 문자 삭제
            data = news_data[i]
            replace_list = ["‘","’","”","“",'"',"'","[포토]","[사설]","[CarTalk]","...","…","[단독]",","]
            for j in replace_list:
                data = data.replace(j, "")
            
            nouns = hannanum.nouns(data)
            nouns_list += nouns
            
        nouns_list = [x for x in nouns_list if len(x)>1] #한 글자 삭제
        

        counter = Counter(nouns_list)
        result = counter.most_common(10) #상위 10개 데이터
        
        return result


            
    #크롤링(데이터 가져오기)
    def post(self, request):
        user_agent = getattr(settings, 'USER_AGENT', None)
        if not user_agent:
            raise ImproperlyConfigured("USER_AGENT must be set in Django settings")

        base_url = 'https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid='
        oids = ['032', '005', '020', '021', '081', '022', '023', '025', '028', '469'] # 언론사 번호
        news_data = []
        headers = {"User-Agent": user_agent}

        # Hotkeywords는 post를 요청할 때마다 delete
        Hotkeywords.objects.all().delete()

        with requests.Session() as session:
            session.headers.update(headers)
            for oid in oids:
                full_url = f"{base_url}{oid}"
                response = session.get(full_url)
                if response.status_code == 200:                                   
                    tree = html.fromstring(response.content)
                    for i in range(1, 11):  # 첫 페이지 앞단 10개
                        elements = tree.xpath(f'//*[@id="main_content"]/div[2]/ul[1]/li[{i}]/dl/dt[last()]/a')
                        news_data.extend([element.text.strip() for element in elements if element.text])
                    
                    for i in range(1, 11):  # 첫 페이지 뒷단 10개
                        elements = tree.xpath(f'//*[@id="main_content"]/div[2]/ul[2]/li[{i}]/dl/dt[last()]/a')
                        news_data.extend([element.text.strip() for element in elements if element.text])

            #형태소 분석
            counter_data = self.WordParsing(news_data)


            #DB에 저장
            for i in range(10):
                keyword_text = counter_data[i][0]
                count = counter_data[i][1]

                # 오늘 날짜를 가져옵니다.
                today = datetime.now().date()
                
                # 오늘 날짜에 해당하는 Dailykeyword 레코드가 이미 존재하는지 확인합니다.
                existing_record = Dailykeywords.objects.filter(keyword_text=keyword_text, keyword_date__date=today).first()
                
                if existing_record:
                    # 이미 존재하는 레코드가 있다면 count를 업데이트 합니다.
                    existing_record.count = F('count') + count
                    existing_record.save()
                else:
                    # 존재하지 않는다면 새로운 레코드를 생성합니다.
                    Dailykeywords.objects.create(
                        keyword_text=keyword_text,
                        count=count
                    )
                Hotkeywords.objects.create(
                    keyword_text=keyword_text,
                    count=count
                )

            return Response({'counter_data':counter_data})