import pandas as pd
import json
import os
os.chdir('C:\Data-Analysis-Practice\energy_use_data_summary\data')

with open("energyUseDataSummaryInfo_personal_2015_2024(2).json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data["data"])
print("DataFrame 변환 = \n", df)
print("=" * 20)
print("df.head() = \n", df.head())
print("=" * 20)
print("df.info() = \n", df.info())
print("=" * 20)
print("df.describe() = \n", df.describe())
print("=" * 20)
print("df.describe(include=['object']) = \n", df.describe(include=['object']))