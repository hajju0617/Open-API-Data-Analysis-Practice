import os
import pandas as pd
import seaborn as sns               # seaborn : matplotlib의 기능을 확장하고 고급화한 시각화 라이브러리.
import matplotlib.pyplot as plt
# Matplotlib은 기본적으로 영문 폰트에 최적화되어 있어서 한글을 쓰면 ??처럼 깨지거나 네모(□) 로 표시됨. 그래서 한글이 지원되는 폰트를 설정해야 한글이 정상적으로 표시됨.
plt.rc('font', family='NanumBarunGothic')

os.chdir('C:/Data-Analysis-Practice/kaggle_store_sales_time_series_forecasting/data')
train = pd.read_csv('train.csv')

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
print('train_enhanced = \n', train_enhanced)

total_outliers = train_enhanced['is_outlier'].sum()
total_ratio = train_enhanced['is_outlier'].mean()

print(f"이상치 개수: {total_outliers:,}건")
print(f"전체 대비 비율: {total_ratio:.2%}")

plt.figure(figsize=(15,6))
sns.stripplot(x='family', y='sales', hue=train_enhanced['is_outlier'],
              # blue : 정상, red : 이상.
              data=train_enhanced, palette={False:'blue', True:'red'})
plt.xticks(rotation=90)
plt.yscale('log')
plt.title('계열별 판매량 분포 (파랑: 정상, 빨강: 이상)')
plt.show()