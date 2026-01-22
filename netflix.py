import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. 데이터 로드

# 파일이 있는 위치(주소)를 이름표(path)로 붙여줍니다.
# 컴퓨터에게 "분석할 파일이 지금 여기 있어!"라고 길을 알려주는 작업입니다.
path = "./Netflix.csv"
# 엑셀과 같은 데이터 분석 도구인 '판다스(pd)'를 이용해 파일을 읽어옵니다.
# 이제 'netflix'라는 변수는 수많은 영화 정보가 담긴 '디지털 표'가 됩니다.
netflix = pd.read_csv("./Netflix.csv")

# 데이터의 가장 윗부분 5줄만 살짝 보여줍니다.
# 장부가 제대로 만들어졌는지, 내용은 어떤 느낌인지 '맛보기'로 확인하는 과정입니다.
print(netflix.head())
# 이 데이터의 '요약 보고서'를 출력합니다.
# 전체 데이터가 몇 줄인지(예: 8,000편), 빈 칸은 없는지, 각 항목이 숫자인지 글자인지 알려줍니다.
# (예: "시청 등급은 글자로 되어 있고, 출시 연도는 숫자로 되어 있네!"라고 확인하는 것)
print(netflix.info())
# 이 표에 있는 '제목 줄(항목들)'만 쭉 뽑아서 보여줍니다.
# 엑셀의 맨 윗줄 제목들(예: 제목, 감독, 장르, 국가 등)만 모아서 메뉴판처럼 보는 것입니다.
print(netflix.columns)
# 0   Show_Id       7789 non-null   object   ID
# 1   Category      7789 non-null   object   TV / MOVIE
# 2   Title         7789 non-null   object   제목
# 3   Director      5401 non-null   object   감독
# 4   Cast          7071 non-null   object   출연자
# 5   Country       7282 non-null   object   나라
# 6   Release_Date  7779 non-null   object   개봉일
# 7   Rating        7782 non-null   object   시청가능등급
# 8   Duration      7789 non-null   object   시간 기간
# 9   Type          7789 non-null   object   장르
# 10  Description   7789 non-null   object   설명




# 데이터 분석을 통한 인사이트 도출

# 1. 넷플릭스 상징색
# 넷플릭스 느낌을 주는 4가지 색상 코드를 리스트(목록)로 만듭니다.
# 강렬한 빨강, 어두운 빨강, 중간 회색, 진한 회색 순서입니다.
netflix_palette = ['#E50914', '#B20710', '#808080', '#454545']
# 시스템에 넷플릭스 전용 색상을 등록합니다.
# sns.color_palette(netflix_palette): 우리가 만든 색상 리스트를 Seaborn이 이해할 수 있는 '공식 팔레트' 형식으로 변환합니다.
# sns.set_palette(...): 변환된 팔레트를 시스템 기본값으로 설정합니다. 
# 이제부터 그리는 모든 그래프는 이 색상들을 기본으로 사용하게 됩니다.
sns.set_palette(sns.color_palette(netflix_palette))
# 설정된 색상들이 어떻게 보이는지 견본(샘플)을 그립니다.
# 가로로 나열된 4개의 색상 박스가 화면에 준비됩니다.
sns.palplot(netflix_palette)
# 준비된 견본을 화면에 최종적으로 출력합니다.
plt.show()


#2. 데이터 전처리 : 결측치(데이터에서 비어있는 칸) 처리
# 출연진(Cast), 감독(Director), 국가(Country)가 비어있는 칸을 찾아 "No Data"라고 채웁니다.
# 정보가 없다고 해서 그 영화 전체를 버리기엔 아까우니까, '정보 없음'이라는 꼬리표를 달아주는 것입니다.
netflix["Cast"] = netflix["Cast"].fillna("No Data")
netflix["Director"] = netflix["Director"].fillna("No Data")
netflix["Country"] = netflix["Country"].fillna("No Data")
# 그 외에 다른 중요한 정보(제목, 장르 등)가 하나라도 비어있는 줄은 과감히 삭제합니다.
# axis=0: 가로 줄(행) 전체를 삭제 / inplace=True: 수정한 내용을 원본 장부에 바로 저장
netflix.dropna(axis=0 , inplace=True)
# 항목별로 빈 칸(Null)이 총 몇 개인지 숫자로 합쳐서 보여줍니다.
# 깨끗하게 청소가 잘 되었다면 모든 항목 옆에 '0'이라는 숫자가 떠야 합니다.
print(netflix.isnull().sum())
 

#3. 데이터 전처리 : 피처 엔지니어링 (컴퓨터가 정답을 더 잘 맞힐 수 있도록 원재료를 가공하는 기술)
# 글자로 된 날짜를 '진짜 날짜(컴퓨터용 달력)' 데이터로 바꿉니다.
# .str.strip(): 날짜 앞뒤에 혹시나 붙어있을지 모를 불필요한 공백을 제거합니다.
# pd.to_datetime: "2024-01-22" 같은 글자를 컴퓨터가 '아, 이건 2024년 1월이구나'라고 이해하게 변환합니다.
netflix["date_added"] = pd.to_datetime(netflix["Release_Date"].str.strip())
# 변환된 날짜에서 '연도(Year)' 정보만 뽑아서 새로운 칸을 만듭니다.
# 이제 이 칸에는 2019, 2020 같은 숫자만 담기게 되어 연도별 비교가 쉬워집니다.
netflix["year_added"] = netflix["date_added"].dt.year
# 변환된 날짜에서 '월(Month)' 정보만 뽑아서 새로운 칸을 만듭니다.
# 1월부터 12월 중 어느 달에 넷플릭스 신작이 가장 많이 올라오는지 분석할 준비가 된 것입니다.
netflix["month_added"] = netflix["date_added"].dt.month


# 시청등급 매핑
age_group_map = {
    "TV-MA": "Adults",      # 성인용
    "R": "Adults",          # 성인용 (영화)
    "NC-17": "Adults",      # 18세 미만 관람 불가
    
    "TV-14": "Teens",       # 14세 이상 (청소년)
    "PG-13": "Teens",       # 13세 미만 주의 (청소년)
    
    "TV-PG": "Older Kids",  # 보호자 동반 시 어린이 가능
    "PG": "Older Kids",     # 초등학생 수준
    
    "TV-G": "Kids",         # 전체 관람가
    "TV-Y": "Kids",         # 유아용
    "TV-Y7": "Kids",        # 7세 이상 어린이
    "G": "Kids",            # 전체 관람가 (영화)
    
    "UR": "Unrated",        # 등급 미정
    "NR": "Unrated"         # 등급 없음
}

# 'Rating'(예: TV-MA, PG) 컬럼의 값들을 우리가 만든 age_group_map에 대조합니다.
# .map() 함수는 "TV-MA가 나오면 Adults라고 바꿔줘"라고 하나씩 매칭해주는 역할을 합니다.
# 그 결과물(Adults, Teens 등)을 'age_group'이라는 새로운 칸을 만들어 저장합니다.
netflix["age_group"] = netflix["Rating"].map(age_group_map)



# 기묘한 이야기(Stranger Things) 검색
# 검색할 검색어 변수
search_query = "Stranger Things"  # 찾고 싶은 작품의 이름을 검색어(search_query)로 정합니다.
# 'Title'(제목) 칸에서 검색어가 포함된 모든 줄을 찾아 'search_result'에 저장합니다.
# str.contains: 제목에 해당 글자가 포함되어 있는지 검사합니다.
# case=False: 대문자(S)든 소문자(s)든 구분하지 않고 다 찾아내라는 뜻입니다.
search_result = netflix[netflix["Title"].str.contains(search_query,case=False)]
# 찾아낸 결과 중에서 딱 필요한 항목(제목, 국가, 등급, 타입)만 선택해서 화면에 출력합니다.
# 대괄호를 두 번 쓰는 것([[ ]])은 '여러 개의 열'을 표 형태로 예쁘게 가져오겠다는 뜻입니다.
print(search_result[["Title","Country","Rating","Type"]])



# MOVIE & TV show 비율 시각화
# 도화지 크기를 가로 5, 세로 5 비율로 정사각형 모양으로 준비합니다.
# 파이 차트는 원형이기 때문에 가로세로 비율이 같아야 찌그러지지 않고 예쁘게 나옵니다.
plt.figure(figsize=(5,5))
# 'Category'(영화 또는 TV쇼) 항목별로 데이터가 몇 개씩 있는지 세어줍니다.
# 예: 영화 5000개, TV쇼 2000개 식으로 숫자를 계산해 ratio 변수에 담습니다.
ratio = netflix["Category"].value_counts()
# 파이 차트 그리기 (예쁘게 꾸미기 옵션 추가)
plt.pie(
    ratio, 
    labels = ratio.index,           # 조각 이름 (Movie, TV Show)
    autopct = '%.1f%%',             # 퍼센트 표시 (소수점 첫째 자리까지)
    startangle = 90,                # 시작 각도를 90도로 설정 (더 깔끔하게 보임)
    colors = ["#454545", "#B20710"], # 우리가 정한 넷플릭스 전용 색상
    shadow = True,                  # 입체감을 주는 '그림자' 추가
    explode = (0.05, 0),            # 첫 번째 조각(Movie)을 살짝 밖으로 빼서 강조
    textprops = {'fontsize': 12, 'fontweight': 'bold', 'color': 'black'} # 글씨 스타일
)
# 제목 설정 (폰트 크기와 색상으로 포인트!)
plt.suptitle("Movies & TV show on Netflix", fontsize=20, color='#E50914', fontweight='bold')
# 그래프 보여주기
plt.show()


# 연도별 MOVIE & TV show 수치 시각화
# 월별 MOVIE & TV show 수치 시각화
# 나라별 타겟팅 하는 연령 시각화
# 워드클라우드 (핵심 단어 시각화)