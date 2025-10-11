import os
import pandas as pd
import missingno as msno
import matplotlib.pyplot as plt
# Matplotlib은 기본적으로 영문 폰트에 최적화되어 있어서 한글을 쓰면 ??처럼 깨지거나 네모(□) 로 표시됨. 그래서 한글이 지원되는 폰트를 설정해야 한글이 정상적으로 표시됨.
plt.rc('font', family='NanumBarunGothic')

os.chdir('C:/Data-Analysis-Practice/kaggle_store_sales_time_series_forecasting/data')

oil = pd.read_csv('oil.csv')


msno.matrix(oil)
plt.title("원유 가격 데이터 결측치 분포")
plt.show()

oil['date'] = pd.to_datetime(oil['date'])
plt.figure(figsize=(12, 6))
plt.plot(oil['date'], oil['dcoilwtico'])        # plt.plot() : 선형 그래프
'''
plt.plot()은 x축과 y축의 데이터를 받아서 선(line)으로 연결해 시각화하는 함수.

plt.plot(x, y)

x : 가로축 데이터
y : 세로축 데이터
이때 두 데이터의 길이는 동일해야 함.
'''
plt.title("시간에 따른 원유 가격 변화")
plt.xlabel("날짜")
plt.ylabel("원유 가격")
plt.grid(True)
plt.show()

'''
시간에 따른 원유 가격 변화는 '시간'에 따라 변화하는 흐름을 갖고 있음.
그렇기 때문에 선형 보간, 즉 이전의 값과 이후에 존재하는 값을 이용해서 그 사이의 값을 채우는 방식으로
결측치를 채우는게 적절함.
'''

