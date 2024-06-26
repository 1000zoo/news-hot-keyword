## 프로젝트 주제 : 뉴스 제목 키워드 분석 및 시각화 웹 서비스

프로젝트 진행 기간: 2024.04.16 - 2024.04.19

프로젝트 참여 인원: 5인

# 📝목차

1. 프로젝트 개요
2. 프로젝트 주제 선정 이유
3. 프로젝트 세부 결과
4. 팀원 및 역할
5. 활용 기술 및 프레임워크
6. 기대효과
7. 프로젝트 결론

# 1. 프로젝트 개요



**‘뉴스 제목 키워드 분석 및 시각화 웹 서비스: Hot Keyword’**는 네이버 뉴스 종합 10개  언론사의 기사 제목을 수집 및 분석하여 키워드를 도출하고, 시각화하는 웹 서비스이다. 기능은 크게 ‘실시간 키워드’와 ‘오늘의 키워드’가 있다.  **실시간 키워드**는 사용자의 요청을 기준으로 뉴스 기사 제목을 크롤링하고, 실시간으로 상위 키워드 10개를 도출하여 웹 페이지에 시각화한다. **오늘의 키워드**는 요청마다 모인 실시간 키워드를 재분석하여 일자별 상위 10개의 키워드를 도출하고 웹 페이지에 시각화한다. 

# 2. 프로젝트 주제 선정 이유



과거에는 포털 사이트에서 실시간 검색어를 통해 현재의 Trend를 신속하고 편리하게 확인할 수 있었다. 그러나 실시간 검색어가 사라진 지금, 직접 검색하지 않으면 현재 일어나고 있는 일을 파악하기가 어려울 뿐만 아니라, SNS에서는 가짜 뉴스가 무분별하게 퍼져 사람들이 쉽게 선동되기도 한다. 우리는 이러한 문제 해결을 위해,뉴스라는 매개체를 사용하여 사람들에게 세상에서 벌어지고 있는 일들을 정확하고 빠르게 전달하고자 한다. 또한, 긴 글을 꺼리는 경향이 있는 현대인들에게 정보를 짧게 **키워드화 및 시각화**하여 전달하고자 한다.

# 3. 프로젝트 세부 결과



### **Frontend**

1. **메인 페이지**
    
    ![1](https://github.com/1000zoo/news-hot-keyword/assets/8938679/b15887ab-5afe-4680-b8a1-61590879a08e)
    
    실시간 키워드 혹은 일일 키워드를 선택하여 원하는 정보를 DB로부터 불러온다.
    
    - 실시간 키워드: 현 시점에서 크롤링하여, 가장 빈도수가 높은 키워드 10개를 도출
    - 일일 키워드: 당일 크롤링한 결과들 중, 가장 빈도수가 높은 키워드 10개를 도출

2. **키워드 페이지**
    
    
    ![2](https://github.com/1000zoo/news-hot-keyword/assets/8938679/6d9c454d-8dfe-44a7-bde2-075bc290d50d)

    메인 페이지에서 선택한 키워드를 빈도순으로 확인할 수 있다. 키워드를 클릭하면 해당 키워드에 대한 네이버 검색 결과가 나온다. `자세히보기` 버튼을 누르면 차트 및 워드 클라우드를 확인할 수 있다.
    
3. **차트 페이지**
    
    ![3](https://github.com/1000zoo/news-hot-keyword/assets/8938679/5c6e4839-8d88-4e9c-b132-b8d117cd0a1c)

    
    좌측부터 키워드들의 막대그래프, 파이그래프, 워드 클라우드를 확인할 수 있다.
    
---
### **Backend**

1. **모델**
    
    실시간 키워드, 일일키워드 그리고 워드 클라우드를 데이터베이스에 저장하기 위한 Django 모델을 생성한다.
    

    1. **`Hotkeywords`** 모델은 크롤하고 분석한 실시간 키워드를 저장하기 위해 `keyword_text` 라는 CharField, 저장 날짜를 저장하기 위해 `keyword_date`라는 DateTimeField, 그리고 키워드의 언급 회수를 저장하기 위해 `count`라는 IntegerField로 구성되어 있다.
    2. **`Dailykeywords`** 모델은 하루 동안의 키워드를 저장하기 위해 `keyword_text` 라는 CharField, 저장 날짜를 저장하기 위해 `keyword_date`라는 DateTimeField, 그리고 키워드의 언급 회수를 저장하기 위해 `count`라는 IntegerField로 구성되어 있다.
    3. **`Wordclouds`** 모델은 실시간 키워드를 분석해서 나온 워드 클라우드 이미지 파일을 저장하기 위해 `wordcloud_img` 라는 ImageField, 저장 날짜를 저장하기 위해 `wordcloud_date`라는 DateTimeField로 구성되어 있다.
    
    
2. **분석한 데이터 저장 및 관리**
    
    전체적으로 Django의 기본 데이터베이스인 sqlite를 사용했다. DB 저장 시, 시간이 UTC 기준이었지만 필요한 시간 데이터는 한국 시간인 KST 였으므로 이를 변경하여 진행했다.
    

    1. 크롤링한 데이터를 데이터베이스에 저장하기 위해 **`post`**함수에서 `Hotkeywords`레코드를 생성하고 날짜를 기준으로 `Dailykeywords`에 중복되는 데이터는 그 데이터의 `count` 를 그만큼 증가시켰고, 중복되지 않는 데이터는 새롭게 `Dailykeywords`에 저장하도록 한다. `Hotkeywords` 레코드는 실시간 키워드와 직결되므로 데이터를 가져오기 전에 `delete()` 를 이용하여 비워준 뒤 크롤링을 진행하였다.
    2. 저장된 `Dailykeywords` 에서 `count`를 기준으로 오름차순 정렬하여 `objects.filter(*keyword_date__date*=timezone.now().date())` 를 이용해 오늘 날짜의 데이터만 가져와 데일리 키워드를 생성했다.
    3. 분석한 키워드로 생성한 워드클라우드를 임시파일에 저장하고 `ContentFile`을 생성하여 이미지 필드에 직접 저장한다.
    
---
### **Crawling**

1. **데이터 크롤링**
    
    **`post`** 함수는 HTTP POST 요청을 처리하는 메서드이다. 이 함수는 클라이언트로부터 받은 요청을 기반으로 Selenium 모듈을 기반으로 크롤링을 수행하고, 데이터를 분석한 후에 응답을 반환한다. 
    
    1. **`chrome_options`**를 설정하여 Chrome을 headless 모드로 실행한다. 이는 브라우저 창을 띄우지 않고 백그라운드에서 실행되도록 한다.
    2. **`webdriver.Chrome`**을 사용하여 크롬을 실행하고, 해당 페이지로 이동한다.
    3. 이후에는 Selenium을 사용하여 웹 페이지의 요소를 찾고 조작한다. 언론사 뉴스 홈 페이지로 이동한 후, 특정 언론사의 요약기사 뉴스 제목을 수집한다. 페이지 내에서 버튼을 클릭하여 다음 언론사 페이지로 이동하고, 각 페이지의 뉴스 제목을 수집하여 **`news_data`** 리스트에 추가한다.
    4. **`WordParsing`** 메서드를 호출하여 **`news_data`**를 분석한다. 이 메서드는 데이터를 형태소 분석하고, 가장 많이 등장한 키워드 10개를 찾아서 반환한다.
    5. 마지막으로, 형태소 분석 결과를 응답으로 반환한다.
    
    
2. **데이터 크롤링 성능 개선(최종본)**
    
    기존의 방식에서는 Selenium을 활용해 각 언론사 페이지의 버튼을 클릭하여 데이터를 수집했으나, URL 패턴(’oid’ 파라미터 변화)를 활용하여 직접 접근하는 방식을 택하여 개선했다. 이 접근 방식은 다음과 같은 프로세스를 포함한다.
    
    1. URL 구성 : ‘https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid=’의 기본 URL에 다양한 ‘oid’ 값을 붙여 언론사별 뉴스 리스트에 접근한다.
    2. 언론사 코드 : ‘032’, ‘005’, ‘020’ 등 종합 언론사를 대상으로 한다.
    3. 데이터 추출 : **`lxml`** 과 **`Xpath`**를 활용하여 HTML 문서에서 뉴스 제목을 추출한다.
    4. 데이터 처리 : 수집된 뉴스 제목은 이전 방식과 동일하게 **`news_data`** 리스트에 저장된다. 세션 관리는 **`requests.Session()`**을 통해 이루어지며, 적절한 **`User-Agent`** 설정을 통해 접근성을 보장한다.
    5. 성능 향상 : 이전 방식에 비해 크롤링에 소요되는 시간은 약 1/10로 단축되었다.  
    
    
3. **데이터 파싱 및 분석**
    
    **`WordParsing`** 함수는 크롤링된 뉴스 기사 제목 데이터를 형태소 분석하여 가장 많이 등장한 키워드를 찾는 메서드이다.
    
    1. 한글 형태소 분석기 중 하나인 **`Hannanum`**객체를 생성한다. 이 객체는 KoNLPy 라이브러리를 사용하여 한글 텍스트를 형태소 단위로 분석할 수 있다.
    2. **`news_data`**에는 크롤링된 뉴스 기사 제목이 담겨있다. 반복문을 사용하여 각 기사 제목에 대해 불필요한 문자를 제거한 후, **`Hannanum`** 객체의 **`nouns`** 메서드를 사용하여 기사 제목을 형태소 단위로 분석합니다. 이때 명사만 추출하여 리스트에 추가한다.
    3. 모든 기사 제목에 대해 명사를 추출한 후에는 한 글자 이상인 단어만을 필터링하여 **`nouns_list`** 리스트에 모은다.
    4. **`Counter`** 클래스를 사용하여 **`nouns_list`**에 등장한 단어의 빈도를 계산한다. 이를 통해 가장 많이 등장한 단어들을 찾는다.
    5. **`most_common`** 메서드를 사용하여 상위 10개의 키워드를 찾고, 이를 **`result`** 변수에 저장한다.
    6. 마지막으로, **`result`**를 반환하여 해당 함수가 호출된 곳으로 결과를 전달한다.
    
---
### **협업**

1. **소스 코드 버전 관리**
    
    Git 및 GitHub를 이용하여 소스 코드의 버전 관리를 하였다. 각 팀원은 맡은 부분을 개발한 후, '이름_기능' 형태의 브랜치를 팀의 GitHub 저장소에 생성하여 소스 코드를 업로드했다. 또한, 역할이 겹치는 경우에는 그 사람끼리 미리 소통하여 컨펌을 받고 상호 합의 후에 코드를 업로드했다. 팀장은 마지막으로 모든 코드를 확인하고, main 브랜치에 병합하였다. 모든 팀원들은 main 브랜치의 코드를 가져와서 로컬 환경에서 작업을 진행한 후, 위의 과정을 반복하여 최종 결과물을 만들었다.
    
    <img width="1021" alt="4" src="https://github.com/1000zoo/news-hot-keyword/assets/8938679/937844e7-7ce7-4c66-8135-849d82036690">

    
2. **비대면 의사소통**
    
    비대면 의사소통을 위해 Slack과 Gather town을 사용했다. Slack을 통해 회의 일정을 잡고, 브랜치 소스 코드의 푸시 현황을 공유하며, 스프린트 중에 발생한 전달사항을 공유했다. 또한, Gather town을 이용하여 매일 일일 스크럼 회의와 스프린트를 진행했다.
    
    매일 13시에 진행하는 **스크럼 회의(조례)**에서는 오늘의 할 일을 정리하고, 깃허브 main 브랜치의 소스 코드를 확인하고 개선점을 논의하며, 발생한 문제 상황을 공유했다. **스프린트**는 스크럼 회의를 바탕으로 맡은 역할을 수행하며, 13:10부터 18:50까지 진행되었다. 스프린트 중에는 모든 인원이 자유롭게 소통할 수 있도록 Gather town에 접속하여 있는것을 원칙으로 하였다. **마무리 스크럼 회의(종례)**에서는 오늘 한 일을 공유하고, 깃 현황을 공유하며, 내일 할 일을 정리했다.
    
    <img width="1021" alt="5" src="https://github.com/1000zoo/news-hot-keyword/assets/8938679/2b5135a2-f1c8-40b3-9de3-0c03440a8308">

   
3. **문서화**
    
    문서화를 위해 Notion을 활용했다. Notion을 이용하여 회의 내용을 기록하고, 기능 개발에 대한 To Do List를 작성하며, 프로젝트의 일정을 정리했다. 또한, 역할 분담 내용을 기록하고, 최종 결과물에 대한 문서화를 수행했다.
    
    Notion을 통해 각종 문서를 효율적으로 관리하고 공유함으로써 프로젝트 진행 상황을 모든 팀원이 쉽게 파악할 수 있었다. 이는 프로젝트의 효율성을 높이고, 업무 협업을 원활하게 진행하는 데 도움이 되었다고 생각한다.
    
    <img width="975" alt="6" src="https://github.com/1000zoo/news-hot-keyword/assets/8938679/6d4c83d3-4e77-4730-91eb-bc810a2d482f">

    

# 4. 팀원 및 역할



- 천지우(팀장👑)
    - 프론트엔드 및 데이터 시각화
    - Github 관리
- 권대혁
    - 백엔드 및 데이터 관리
- 최은희
    - 웹 크롤링 성능 개선
    - 보고서 작성
- 이풍훈
    - 백엔드 및 데이터 관리
- 김지원
    - 웹 크롤링 API 제작
    - main 페이지 프론트 작업
    - 보고서 작성

# 5. 활용 기술 및 프레임워크



### **Frontend**

- Html/Css
- JavaScript
- Bootstrap

### Backend

- Framework: Django(Python3)
- DataBase: Sqlite

### Crawling

- Django Rest Framework
- BeautifulSoup4
- KoNLPy

### Communication && Collaboration Tools

- Gather town
- Git/GitHub
- Slack
- Notion

# 6. 기대효과



- 실시간 키워드 및 오늘의 키워드를 제공함으로써 사용자는 현재의 트렌드와 주요 이슈를 신속하게 파악할 수 있다.
- 실시간으로 수집된 키워드를 시각화하여 제공함으로써 사용자는 간편하게 정보를 이해할 수 있다.
- 뉴스 기사 제목에서 추출된 키워드를 통해 사용자는 해당 주제에 대한 관심을 높일 수 있다.
- 가짜 뉴스에 대한 정보와 판별 능력을 향상시키고, 사용자가 더욱 신뢰할 만한 정보를 얻을 수 있도록 돕는다.
- 긴 글을 꺼리는 현대인들에게도 쉽게 접근 가능한 형태로 정보를 전달함으로써, 뉴스 소비의 편의성과 효율성을 높인다.

# 7. 프로젝트 결론



### 요약

**Hot Keyword**는 네이버 뉴스 종합 10개 언론사의 기사 제목을 수집하고 분석하여 키워드를 도출하고 시각화하는 웹 서비스이다. 사용자는 실시간 키워드 및 오늘의 키워드를 통해 현재의 트렌드와 주요 이슈를 신속하게 파악할 수 있다. 또한, 실시간으로 수집된 키워드가 시각화되어 제공되므로 사용자는 간편하게 정보를 이해할 수 있다. 이를 통해 뉴스 기사 제목에서 추출된 키워드를 통해 사용자는 해당 주제에 대한 관심을 높일 수 있으며, 가짜 뉴스에 대한 정보와 판별 능력을 향상시키고, 신뢰할 만한 정보를 얻을 수 있다. 또한, 긴 글을 꺼리는 현대인들에게도 쉽게 접근 가능한 형태로 정보를 전달함으로써, 뉴스 소비의 편의성과 효율성을 높이는데 기여한다. 따라서 **Hot Keyword**는 뉴스 소비 환경을 개선하고 사용자들의 정보 획득을 돕는 데 도움이 될 것으로 기대한다.

### 한계 및 개선점

- 한계점
    - 데이터 파싱 시, 조사, 동사 등을 제외한 명사의 유/무의미한 형태소 파악이 어렵다. 예를 들어, 아이돌 가수 팀명, 사람 이름의 경우 사전에 등재되어 있지 않기 때문에 형태소를 분리해서 판단하는 경우가 있다.
    - '평생' 과 같은 명사가 키워드로 등장하는 경우가 존재했는데, 실시간 키워드에 '평생'이라는 단어가 등장했을 때 사용자들은 “이게 어느 맥락의 '평생'을 의미하는 것일까?” 하며 의문을 가질 수 있어보였다. 단어만 등장하기 때문에 이렇게 의미가 모호할 수 있고, 크게 유의미한 결과가 아닌 것들을 제외하려면 koNLPy와 같은 툴 + 체계적인 제약 조건 또는 우리의 원하는 결과를 낼 수 있는 형태소 분리기를 만드는 것과 같이 짧은 시간 내에 해내기에는 힘든 작업을 수행해야 할 것이다.
    
- 개선점
    - 카이스트에서 개발한 Hannanum 형태소 분석기와  twitter 형태소 분석기 선택에 따라 파싱 된 데이터 결과가 달라지므로, 우리 서비스에 어떤 형태소 분석기가 적절할지 고민해 보아야 한다.
    - 실시간 키워드를 얻어올 때인 POST 요청 시에만 데이터 크롤링을 진행했는데, 이 데이터를 기반으로 데일리 키워드를 생성했었다. 그러나 실시간 키워드의 데이터를 수집하는 주기가 한쪽으로 치우친 경우, 데이터가 편향될 가능성이 존재하므로 주기를 일정하게 정한 뒤 데이터를 수집하여 데일리 키워드를 보여주는 것이 우리의 의도와 더 가까울 것으로 생각된다.
    - 일일 키워드는 실시간 데이터의 빈도수 상위 10개의 키워드를 누적하여 그 중 상위 10개를 선정하는데 이렇게되면 실시간 상위 10개 이외의 키워드는 누적되지 않는다. 키워드의 언급 빈도를 보다 정확하게 얻기 위해서는 크롤링과 모델의 구조를 수정할 필요가 있다.
