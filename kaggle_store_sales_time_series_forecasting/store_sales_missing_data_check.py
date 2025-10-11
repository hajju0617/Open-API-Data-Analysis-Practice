import os
import pandas as pd

os.chdir('C:/Data-Analysis-Practice/kaggle_store_sales_time_series_forecasting/data')

train = pd.read_csv('train.csv')
stores = pd.read_csv('stores.csv')
transactions = pd.read_csv('transactions.csv')
oil = pd.read_csv('oil.csv')
holidays_events = pd.read_csv('holidays_events.csv')

print('train.isnull().sum() = \n', train.isnull().sum())
print("*" * 30)
print('stores.isnull().sum() = \n', stores.isnull().sum())
print("*" * 30)
print('transactions.isnull().sum() = \n', transactions.isnull().sum())
print("*" * 30)
print('oil.isnull().sum() = \n', oil.isnull().sum())
print("*" * 30)
print('holidays_events.isnull().sum() = \n', holidays_events.isnull().sum())