import os
import pandas as pd
import seaborn as sns               # seaborn : matplotlib의 기능을 확장하고 고급화한 시각화 라이브러리.
import matplotlib.pyplot as plt
# Matplotlib은 기본적으로 영문 폰트에 최적화되어 있어서 한글을 쓰면 ??처럼 깨지거나 네모(□) 로 표시됨. 그래서 한글이 지원되는 폰트를 설정해야 한글이 정상적으로 표시됨.
plt.rc('font', family='NanumBarunGothic')

os.chdir('C:/Data-Analysis-Practice/kaggle_store_sales_time_series_forecasting/data')
train = pd.read_csv('train.csv')
transactions = pd.read_csv('transactions.csv')
stores = pd.read_csv('stores.csv')
oil = pd.read_csv('oil.csv')

oil_cleaned = oil.copy()
# 선형 보간법을 적용한 '시간에 따른 원유 가격 변화' 그래프.
oil_cleaned['dcoilwtico'] = oil_cleaned['dcoilwtico'].interpolate(method='linear')

# 제품 계열별 판매 데이터 IQR 계산.
family_bounds = train.groupby('family')['sales'].apply(
    # IQR 기반 이상치 상한값 계산.
    lambda x: x.quantile(0.75) + 1.5 * (x.quantile(0.75) - x.quantile(0.25))
    )
train_enhanced = train.copy()
# 각 행의 family에 맞는 이상치 상한값 매핑.
train_enhanced['upper_bound'] = train_enhanced['family'].map(family_bounds)
# 이상치 여부를 분류.
train_enhanced['is_outlier'] = train_enhanced['sales'] > train_enhanced['upper_bound']

# 판매량이 상한값 초과 시 -> 판매량을 상한값으로 대체.
train_cleaned = train.copy()
# train_enhanced['is_outlier'] : 이상치를 먼저 선택하고 여기서 'sales'컬럼만 가져옴.
# 가져온 'sales'컬럼에 train_enhanced['is_outlier'], 즉 이상치로 판정됐던 것들을 상한값으로 대체.
train_cleaned.loc[train_enhanced['is_outlier'], 'sales'] = \
    train_enhanced.loc[train_enhanced['is_outlier'], 'upper_bound']

# 판매, 거래, 원율 데이터 내 date 컬럼 데이터 datetime 데이터 타입으로 변경.
train_cleaned['date'] = pd.to_datetime(train_cleaned['date'])
transactions['date'] = pd.to_datetime(transactions['date'])
oil_cleaned['date'] = pd.to_datetime(oil_cleaned['date'])


train_cleaned['year'] = train_cleaned['date'].dt.year
train_cleaned['month'] = train_cleaned['date'].dt.month
train_cleaned['day'] = train_cleaned['date'].dt.day
train_cleaned['dayofweek'] = train_cleaned['date'].dt.dayofweek

# 주말, 월초, 월말 여부 추출.
# dayofweek : 월화수목금 -> 0, 1, 2, 3, 4 이므로 1로 저장, 그 외에는 0으로 저장.
train_cleaned['weekend'] = train_cleaned['dayofweek'].apply(lambda x: 1 if x >= 5 else 0)
train_cleaned['is_month_start'] = train_cleaned['date'].dt.is_month_start
train_cleaned['is_month_end'] = train_cleaned['date'].dt.is_month_end


# 판매, 거래 데이터 통합.
train_with_trans = pd.merge(
    train_cleaned, transactions,
    on=['date', 'store_nbr'],    # merge 조건. (즉 date가 동일하고 store_nbr이 같은 경우에 합침.)
    how='left'
)


# 매장 데이터 통합.
train_with_store = pd.merge(
    train_with_trans, stores,
    on=['store_nbr'],
    how='left'
)


# 원유 데이터 통합.
train_final = pd.merge(
    train_with_store, oil_cleaned,
    on='date',
    how='left'
)


print("최종 데이터셋 정보:")
print(f"행 개수: {train_final.shape[0]}, 열 개수: {train_final.shape[1]}")
print()
print(train_final.columns.tolist())
print()
print(train_final.head())