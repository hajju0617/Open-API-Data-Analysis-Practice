import json
import requests
import time
from dateutil.relativedelta import relativedelta
import datetime
from dotenv import load_dotenv
import os
os.chdir('C:\Data-Analysis-Practice\energy_use_data_summary\data')
load_dotenv()
API_KEY = os.getenv('API_KEY')
BASE_URL = f'http://openapi.seoul.go.kr:8088/{API_KEY}/json/energyUseDataSummaryInfo/1/7'

# 기간 설정
start_date = datetime.datetime(2015, 1, 1)
end_date = datetime.datetime(2024, 12, 1)

# 날짜 범위 생성
current_date = start_date
date_list = []
while current_date <= end_date:
    date_list.append(current_date)
    current_date += relativedelta(months = +1)

results = []
print('[START] 데이터 수집 시작')

for dt in date_list:
    year = dt.strftime('%Y')
    month = dt.strftime('%m')

    url = f'{BASE_URL}/{year}/{month}'

    try:
        response = requests.get(url, timeout=3)
        
        if response.status_code == 200:
            data = response.json()
            
            result_code = data.get("energyUseDataSummaryInfo", {}).get("RESULT", {}).get("CODE")
            
            if result_code == "INFO-000":                
                rows = data.get("energyUseDataSummaryInfo", {}).get("row", [])
                found_personal_data = False 
                
                for row in rows:
                    if row.get("MM_TYPE") == "개인":
                        extracted_data = {
                                            "YEAR": row.get("YEAR"),
                                            "MON": row.get("MON"),
                                            "MM_TYPE": row.get("MM_TYPE"),
                                            "EUS": row.get("EUS"),              # 현년 전기사용량
                                            "GUS": row.get("GUS"),              # 현년 가스사용량
                                            "WUS": row.get("WUS"),              # 현년 수도사용량
                                            "HUS": row.get("HUS"),              # 현년 지역난방 사용량
                                            "REG_DATE": row.get("REG_DATE")
                                        }
                        results.append(extracted_data)
                        found_personal_data = True
                        break
                        
                if found_personal_data:
                    print(f"[OK] {year}-{month} '개인'타입의 데이터를 수집하였음.")
                else:
                    print(f"[FAIL] {year}-{month} '개인'타입의 데이터가 응답에 존재하지 않음.")            
    except Exception as e:
        print(f"[EXCEPTION] {year}-{month} 수집 중 오류가 발생하였음 : {e}")
        
    time.sleep(0.3) 

output_file = "energy_use_data_summary_info_personal_2015_2024.json"

final_json_data = {
    "start_date": start_date.strftime('%Y-%m'),
    "end_date": end_date.strftime('%Y-%m'),
    "data_count": len(results),
    "data": results
}

try:
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(final_json_data, f, ensure_ascii=False, indent=2)
    print(f"총 {len(results)}건 저장되었음 : {output_file}")
except Exception as e:
    print(f"파일 저장 중 오류가 발생하였음 : {e}")
