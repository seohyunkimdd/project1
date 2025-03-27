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


##### 범죄 발생 현황 전처리 #####
crime_data = pd.read_csv('./data/5대+범죄+발생현황_20250327131820.csv')

# 총 범죄 발생 건수만 출력
crime_selected = crime_data[['자치구별(2)','2019','2020','2021','2022','2023']]
crime_selected = crime_selected.drop(range(0, 4), axis=0)
crime_selected.columns = ['자치구', '2019', '2020', '2021', '2022', '2023']
crime_selected.reset_index(drop=True, inplace=True)

# print(crime_selected)
'''
     자치구  2019  2020  2021  2022  2023
0    종로구  3846  3102  2712  3138  2981
1     중구  4327  3411  2861  3071  3348
2    용산구  3313  2969  2381  2967  3021
3    성동구  2512  2362  2112  2194  2023
4    광진구  4011  3601  3087  3619  3424
5   동대문구  3692  3401  2959  3253  2957
6    중랑구  4268  3726  3210  3599  3324
7    성북구  2877  2567  2411  2749  2411
8    강북구  3838  2770  2301  2832  2497
9    도봉구  2110  2179  1860  2141  1921
10   노원구  4153  3743  3425  3896  3567
11   은평구  3880  3390  3244  3487  3493
12  서대문구  2943  2533  2278  2374  2385
13   마포구  4842  3688  3540  4096  3834
14   양천구  3214  3216  3015  3169  3019
15   강서구  4924  4415  3896  4663  4296
16   구로구  4707  4175  3486  3857  3737
17   금천구  3105  2598  2439  2577  2240
18  영등포구  5820  5217  4179  4819  4418
19   동작구  3400  3200  2631  2735  2642
20   관악구  5328  5261  4444  4879  4769
21   서초구  5542  4601  3656  4459  4522
22   강남구  7304  7356  6146  6947  6763
23   송파구  5698  5410  4714  5167  5223
24   강동구  4014  3788  3458  3711  3398
'''
print()

##### CCTV 데이터 전처리 #####
cctv_data = pd.read_excel('./data/서울시 자치구 (범죄예방 수사용) CCTV 설치현황_241231.xlsx')
# print(cctv_data)

# 2019년부터 2023년 데이터 추출
cctv_selected = cctv_data[['Unnamed: 2','Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9', 'Unnamed: 10', 'Unnamed: 11']]
cctv_selected.columns = ['자치구', '2019', '2020', '2021', '2022', '2023']
cctv_selected = cctv_selected[cctv_selected['자치구'].apply(lambda x: x not in ['계', '구분'])]
cctv_selected = cctv_selected.dropna()
cctv_selected.reset_index(drop=True, inplace=True)

# print(cctv_selected)
'''
     자치구  2019  2020  2021  2022  2023
0    종로구  1327  1510  1573  1812  1872
1     중구  1242  1482  1911  2026  2157
2    용산구  1915  2058  2321  2531  2897
3    성동구  2833  3162  3519  3627  3871
4    광진구  2308  2481  3111  3370  3421
5   동대문구  2061  2166  2471  2592  3077
6    중랑구  2250  3165  3592  3856  4163
7    성북구  3238  3440  3815  4014  4216
8    강북구  1656  2337  2960  3184  3191
9    도봉구   835  1189  1684  1994  2196
10   노원구  1763  2034  2171  2284  2613
11   은평구  3141  3431  3822  4103  4369
12  서대문구  2100  2499  2591  2928  3117
13   마포구  2011  2268  2372  2500  3015
14   양천구  2928  3136  3393  3627  4064
15   강서구  1858  2346  2637  3151  3397
16   구로구  3074  3455  3842  4013  4265
17   금천구  1894  2247  2276  2498  2978
18  영등포구  2093  3250  3508  3896  3987
19   동작구  1904  2155  2181  2404  2656
20   관악구  3388  3652  3833  4029  4210
21   서초구  2938  3175  3442  3180  3343
22   강남구  5459  5796  6143  6495  6829
23   송파구  2052  2372  2520  2805  3471
24   강동구  1871  2475  2720  3086  3435
'''


##### 데이터 병합 #####
# crime_selected 데이터 형태 변환
crime_long = crime_selected.melt(id_vars='자치구', var_name='연도', value_name='범죄발생수')

# cctv_selected 데이터 형태 변환
cctv_long = cctv_selected.melt(id_vars='자치구', var_name='연도', value_name='CCTV설치수')

# 두 데이터 병합
crime_cctv = pd.merge(crime_long, cctv_long, on=['자치구', '연도'], how='inner')
crime_cctv = crime_cctv.sort_values(by=['자치구', '연도']).reset_index(drop=True)
print(crime_cctv)

# 엑셀 파일로 추출
crime_cctv.to_csv('./data/crime_cctv_data.csv', index=False, encoding='cp949')