import pandas as pd
import matplotlib.pyplot as plt
plt.rc('font', family='NanumBarunGothic')
import json
import os
os.chdir('C:\Data-Analysis-Practice\energy_use_data_summary\data')

with open("energy_use_personal_2015_2024_with_season.json", "r", encoding="utf-8") as f:
    date = json.load(f)
df = pd.DataFrame(date)

for column in ["EUS", "GUS", "WUS", "HUS"]:
    df[column] = df[column].astype(float)

# 총 사용량.
df['total_usage'] = df['EUS'] + df['GUS'] + df['WUS'] + df['HUS']
# 연도별 그룹화(GROUPBY)하여 각 연도별 에너지 사용량(전기, 가스, 수도, 난방, 총합) 합계를 계산.
yearly_usage = df.groupby('YEAR')[['EUS', 'GUS', 'WUS', 'HUS', 'total_usage']].sum().reset_index()


plt.figure(figsize=(15,8))
# 막대 그래프.
plt.bar(yearly_usage["YEAR"], yearly_usage["total_usage"], color='black', label='총 사용량')
# 선그래프.
plt.plot(yearly_usage["YEAR"], yearly_usage["EUS"], marker='o', label='전기(EUS)')
plt.plot(yearly_usage["YEAR"], yearly_usage["GUS"], marker='o', label='가스(GUS)')
plt.plot(yearly_usage["YEAR"], yearly_usage["WUS"], marker='o', label='수도(WUS)')
plt.plot(yearly_usage["YEAR"], yearly_usage["HUS"], marker='o', label='난방(HUS)')

plt.title("연도별 에너지 총사용량 및 세부내역 변화.")
plt.xlabel("연도")
plt.ylabel("사용량")
plt.grid(True)
plt.legend()    # 범례
plt.tight_layout()
plt.show()