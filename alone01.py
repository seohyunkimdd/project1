import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib import rc

# 음수표기 관리
import matplotlib as mpl
mpl.rc('axes', unicode_minus=False)
mpl.rcParams['axes.unicode_minus']=False

font_name = font_manager.FontProperties(fname='c:/windows/Fonts/malgun.ttf').get_name()
rc('font', family=font_name)

import pandas as pd
import numpy as np
import seaborn as sns 
import time

#--------------------------------------------------------------------------------------------
import urllib.request  
import json
import requests  
import folium

cj_data = pd.read_csv('./data/경찰청_범죄 발생 지역별 통계_20231231.csv', encoding='euc-kr')
# print(cj)

cctv_data = pd.read_csv('./data/서울시 안심이 CCTV 연계 현황.csv', encoding='cp949')
# print(cctv_data)

# 서울 지역 관련 열 인덱스 출력
seoul_columns = ['범죄대분류', '범죄중분류'] + [col for col in cj_data.columns if '서울' in col]

# 서울 데이터만 추출
seoul_data = cj_data[seoul_columns]

# 서울 데이터 출력
print(seoul_data)
