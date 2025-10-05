import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import os
os.chdir("C:/Data-Analysis-Practice/kma_1month_forecast/data")

# 기상청 1개월 예보 RSS(XML) URL
url = "https://www.kma.go.kr/repositary/xml/fct/mon/img/fct_mon1rss_108_20251002.xml"

# 1️XML 데이터 요청
response = requests.get(url)
response.encoding = "utf-8"

# BeautifulSoup으로 XML 파싱
soup = BeautifulSoup(response.text, "xml")


# 제목, 예보기간 등 메타 정보
title = soup.find("title").text
title2 = soup.find("title")
announcement_title = soup.find("item").find("title").text
link = soup.find("link").text
author = soup.find("item").find("author").text
date = soup.find("date").text
ydate = soup.find("ydate").text
next_ydate = soup.find("next_ydate").text

print("제목:", title)
print("제목2:", title2)
print("발표 제목:", announcement_title)
print("링크:", link)
print("작성자:", author)
print("예보 기간:", date)
print("발표 시각:", ydate)
print("다음 발표 시각:", next_ydate)
print("-" * 60)

meta_data = {
            "제목": title,
            "발표 제목": announcement_title,
            "링크": link,
            "작성자": author,
            "예보기간": date,
            "발표시각": ydate,
            "다음발표시각": next_ydate
}

# 전체 주차별 예보 요약 저장용.
summary_data = []

weeks = soup.find_all("week")
for i, week in enumerate(weeks, start=1):       # 시작 인덱스를 1로 지정.
    period_tag = week.find(f"week{i}_period")
    review_tag = week.find(f"week{i}_weather_review")

    if period_tag and review_tag:
        print(f"{i}주차 기간: {period_tag.text.strip()}")
        print(f"예보 내용:\n{review_tag.text.strip()}")
        print("-" * 60)

        summary_data.append({
            "주차": i,
            "기간": period_tag.text.strip(),
            "예보": review_tag.text.strip()
        })

# 지역별 상세 데이터 저장용.
local_ta_list = soup.find_all("local_ta")
region_data = []

for local_ta in local_ta_list:
    region_name_tag = local_ta.find("local_ta_name")
    if not region_name_tag:
        continue
    region_name = region_name_tag.text.strip()

    for i in range(1, 5):  # 1~4주차.
        normal_tag = local_ta.find(f"week{i}_local_ta_normalYear")
        range_tag = local_ta.find(f"week{i}_local_ta_similarRange")
        min_tag = local_ta.find(f"week{i}_local_ta_minVal")
        sim_tag = local_ta.find(f"week{i}_local_ta_similarVal")
        max_tag = local_ta.find(f"week{i}_local_ta_maxVal")

        if not (normal_tag and range_tag):
            continue

        region_data.append({
            "지역": region_name,
            "주차": i,
            "평균기온": normal_tag.text.strip(),
            "평년범위": range_tag.text.strip(),
            "확률_↓": min_tag.text.strip(),
            "확률_≈": sim_tag.text.strip(),
            "확률_↑": max_tag.text.strip()
        })

# DataFrame으로 변환.
df_summary = pd.DataFrame(summary_data)
df_region = pd.DataFrame(region_data)

# CSV 저장.
df_summary.to_csv("weather_summary.csv", index=False, encoding="utf-8")
df_region.to_csv("weather_region.csv", index=False, encoding="utf-8")

summary_json_output = {
    "metadata": meta_data,              # 메타데이터를 'metadata' 키로 한 번만 저장.
    "forecast_summary": summary_data    # 주차별 요약 데이터를 리스트로 저장.
}

# JSON 저장.
with open("weather_summary.json", "w", encoding="utf-8") as f:
    json.dump(summary_json_output, f, ensure_ascii=False, indent=2)

with open("weather_region.json", "w", encoding="utf-8") as f:
    json.dump(region_data, f, ensure_ascii=False, indent=2)

print("저장 완료. summary + region 모두 CSV/JSON로 저장됨.")
