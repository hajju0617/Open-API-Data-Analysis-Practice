import pandas as pd
import json
import os
os.chdir('C:\Data-Analysis-Practice\energy_use_data_summary\data')

with open("energyUseDataSummaryInfo_personal_2015_2024(2).json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data["data"])
print("df = \n", df)

def get_season(month):
    month = int(month)
    if month in [3, 4, 5]:
        return "봄"
    elif month in [6, 7, 8]:
        return "여름"
    elif month in [9, 10, 11]:
        return "가을"
    else:
        return "겨울"

df["season"] = df["MON"].apply(get_season)
print("df = \n", df)

df_to_json = df.to_json(force_ascii=False, indent=2, orient="records")
print("df_to_json = \n", df_to_json)

with open("energyUse_personal_2015_2024_with_season.json", "w", encoding="utf-8") as f:
    f.write(df_to_json)

