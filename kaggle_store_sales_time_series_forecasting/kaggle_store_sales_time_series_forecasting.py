import os
import pandas as pd

os.chdir('C:/Data-Analysis-Practice/kaggle_store_sales_time_series_forecasting/data')

train = pd.read_csv('train.csv')
stores = pd.read_csv('stores.csv')
transactions = pd.read_csv('transactions.csv')
oil = pd.read_csv('oil.csv')
holidays_events = pd.read_csv('holidays_events.csv')

print('학습 데이터 기본 정보')
print(train.info())
print()

# 판매 데이터 기본 통계량
print('train.describe() = \n', train.describe())

# 매장 데이터 기본 정보
# head()는 Pandas DataFrame의 상위(앞부분) 데이터를 미리보기 위해 사용하는 메서드. (디폴트 값 : 상위 5개 행.)
print('stores.head() = \n', stores.head()) 

# 원유 가격 데이터 기본 정보
print('oil.head() = \n', oil.head())
