import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import re

data_path = r"C:\AI_Project01\data"

crime_data = pd.read_csv(f"{data_path}\\5대+범죄+발생현황_20250327150529.csv")
population_data = pd.read_csv(f"{data_path}\\201912_202312_연령별인구현황_연간.csv", encoding='cp949')
cctv_data = pd.read_excel(f"{data_path}\\서울시 자치구 (연도별) CCTV 설치현황_241231.xlsx")

crime_new = crime_data[['자치구별(2)','2019','2020','2021','2022','2023']]
crime_new = crime_new.drop([0,1,2,3],axis=0)
crime_new.reset_index(drop=True,inplace=True)

population_new = population_data[['행정구역','2019년_계_총인구수','2020년_계_총인구수','2021년_계_총인구수','2022년_계_총인구수','2023년_계_총인구수']]
population_new = population_new.drop([0],axis=0)
population_new.reset_index(drop=True,inplace=True)

cctv_new = cctv_data[['Unnamed: 2','Unnamed: 8','Unnamed: 9','Unnamed: 10','Unnamed: 11','Unnamed: 12']]
cctv_new = cctv_new.drop([0,1,2,28],axis=0)
cctv_new.reset_index(drop=True,inplace=True)

crime_new.columns = [
    'District',     
    '2019',
    '2020',
    '2021',
    '2022',
    '2023'
]

population_new.columns = [
    'District',         
    '2019',
    '2020',
    '2021',
    '2022',
    '2023'
]

cctv_new.columns = [
    'District',   
    '2019',  
    '2020',  
    '2021',  
    '2022',  
    '2023'   
]

def district_name(name):
    if name.startswith("서울특별시"):
        name = name.replace("서울특별시", "")
    name = re.sub(r"\(.*\)", "", name)
    return name.strip()

crime_new['District'] = crime_new['District'].apply(lambda x: x.strip())
population_new['District'] = population_new['District'].apply(district_name)
cctv_new['District'] = cctv_new['District'].apply(lambda x: str(x).replace(" ", "").strip())

crime_axis = crime_new.melt(
    id_vars='District', 
    var_name='Year', 
    value_name='Crime'
)
population_axis = population_new.melt(
    id_vars='District',
    var_name='Year',
    value_name='Population'
)
cctv_axis = cctv_new.melt(
    id_vars='District',
    var_name='Year',
    value_name='CCTV'
)

population_axis['Population'] = population_axis['Population'].apply(lambda x: str(x).replace(",", ""))

population_axis['Population'] = population_axis['Population'].astype(int)
crime_axis['Crime'] = crime_axis['Crime'].astype(int)
cctv_axis['CCTV'] = cctv_axis['CCTV'].astype(int)

merged_Data = pd.merge(crime_axis, population_axis, on=['District', 'Year'], how='inner')
merged_DataF = pd.merge(merged_Data, cctv_axis, on=['District', 'Year'], how='inner')

merged_DataF['Year'] = merged_DataF['Year'].astype(int)
merged_DataF = merged_DataF.sort_values(by=['District', 'Year']).reset_index(drop=True)

output_file = f"{data_path}\\DataFinal.csv"
merged_DataF.to_csv(output_file, index=False, encoding='cp949')