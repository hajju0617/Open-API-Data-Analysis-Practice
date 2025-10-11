import os
import pandas as pd
import missingno as msno
import matplotlib.pyplot as plt
# Matplotlib은 기본적으로 영문 폰트에 최적화되어 있어서 한글을 쓰면 ??처럼 깨지거나 네모(□) 로 표시됨. 그래서 한글이 지원되는 폰트를 설정해야 한글이 정상적으로 표시됨.
plt.rc('font', family='NanumBarunGothic')

os.chdir('C:/Data-Analysis-Practice/kaggle_store_sales_time_series_forecasting/data')

oil = pd.read_csv('oil.csv')


oil_cleaned = oil.copy()

# 선형 보간법을 적용한 '시간에 따른 원유 가격 변화' 그래프.
oil_cleaned['dcoilwtico'] = oil_cleaned['dcoilwtico'].interpolate(method='linear')

plt.figure(figsize=(12, 6))
plt.plot(oil_cleaned['date'], oil_cleaned['dcoilwtico'])        # plt.plot() : 선형 그래프
plt.title("시간에 따른 원유 가격 변화를 선형 보간법으로 결측치를 처리한 후 데이터")
plt.xlabel("날짜")
plt.ylabel("원유 가격")
plt.grid(True)
plt.show()