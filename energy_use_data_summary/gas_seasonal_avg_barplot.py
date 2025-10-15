import pandas as pd
import matplotlib.pyplot as plt
plt.rc('font', family='NanumBarunGothic')
import json
import os
os.chdir('C:\Data-Analysis-Practice\energy_use_data_summary\data')

with open('energyUse_personal_2015_2024_with_season.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
df = pd.DataFrame(data)
df["GUS"] = df["GUS"].astype(float)

season_order = ['봄', '여름', '가을', '겨울']
df['season'] = pd.Categorical(df['season'], categories=season_order, ordered=True)
df_sorted = df.sort_values('season')

seasonal_gas = df_sorted.groupby('season')['GUS'].mean().reset_index()

plt.figure(figsize=(15, 8))
bars = plt.bar(
    seasonal_gas['season'],     # x
    seasonal_gas['GUS']         # y
)

for bar in bars:
    yval = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width()/2.0,
        yval,
        f'{yval:,.0f}',                   
        ha='center',                      
        va='bottom'                       
    )

plt.title('2. 계절별 가스 사용량 평균')
plt.xlabel('계절')
plt.ylabel('평균 가스 사용량')
plt.grid(True)
plt.tight_layout()
plt.show()

