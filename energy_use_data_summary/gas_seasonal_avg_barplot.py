import pandas as pd
import matplotlib.pyplot as plt
plt.rc('font', family='NanumBarunGothic')
import json
import os
os.chdir('C:\Data-Analysis-Practice\energy_use_data_summary\data')

with open('energyUse_personal_2015_2024_with_season.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# DataFrame 변환
df = pd.DataFrame(data)
print(df)

print('df["GUS"].dtype = \n', df["GUS"].dtype)

df["GUS"] = df["GUS"].astype(float)
print('df["GUS"].dtype = \n', df["GUS"].dtype)
season_gas = df.groupby('season')['GUS'].mean().reset_index()
print('season_gas = \n', season_gas)

plt.figure(figsize=(10, 6))
bars = plt.bar(
    season_gas['season'], 
    season_gas['GUS']
)

for bar in bars:
    yval = bar.get_height()
    # 수치를 쉼표로 포맷팅하여 막대 위에 출력
    plt.text(
        bar.get_x() + bar.get_width()/2.0, # X 위치 (막대의 중앙)
        yval,              # Y 위치
        f'{yval:,.0f}',                    # 값 포맷팅 (정수형에 쉼표 추가)
        ha='center',                       # 가로 정렬: 중앙
        va='bottom'                       # 세로 정렬: 아래
    )

# 그래프 제목 및 레이블 설정
plt.title('2. 계절별 가스 사용량 평균')
plt.xlabel('계절 (Season)')
plt.ylabel('평균 가스 사용량')
plt.tight_layout()
plt.grid(True)
plt.show()