import pandas as pd
import matplotlib.pyplot as plt
plt.rc('font', family='NanumBarunGothic')
import json
import os
os.chdir('C:\Data-Analysis-Practice\energy_use_data_summary\data')

with open("energy_use_personal_2015_2024_with_season.json", "r", encoding="utf-8") as f:
    date = json.load(f)
df = pd.DataFrame(date)
print('df["EUS"].dtype', df["EUS"].dtype)

for column in ["EUS", "GUS", "WUS", "HUS"]:
    df[column] = df[column].astype(float)
print('df["EUS"].dtype', df["EUS"].dtype)

df['total_usage'] = df['EUS'] + df['GUS'] + df['WUS'] + df['HUS']
yearly_usage = df.groupby('YEAR')['total_usage'].sum().reset_index()

plt.figure(figsize=(15,8))
                        # x축, y축.
plt.plot(yearly_usage["YEAR"], yearly_usage["total_usage"], marker='o')
plt.title("연도별 에너지 사용 총액 변화량 - 1538")
plt.xlabel("연도")
plt.ylabel("총 사용량")
plt.grid(True)
plt.tight_layout()
plt.show()

