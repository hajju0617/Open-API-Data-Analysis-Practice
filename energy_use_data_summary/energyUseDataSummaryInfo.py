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

print(API_KEY)
# 기간 설정
START_DATE = datetime.datetime(2015, 1, 1)
END_DATE = datetime.datetime(2024, 12, 1)

# 날짜 범위 생성
current_date = START_DATE
date_list = []
while current_date <= END_DATE:
    date_list.append(current_date)
    current_date += relativedelta(months = +1)

results = []
failed_calls = []

print('[START] 데이터 수집 시작')

for dt in date_list:
    year = dt.strftime('%Y')
    month = dt.strftime('%m')

    url = f'{BASE_URL}/{year}/{month}'

    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # API 응답 결과 코드 확인 (INFO-000이 정상호출)
            result_code = data.get('energyUseDataSummaryInfo', {}).get('RESULT', {}).get('CODE')
            
            if result_code == "INFO-000":
                print('[SUCCESS] API 호출 성공.')
                
                rows = data.get("energyUseDataSummaryInfo", {}).get("row", [])
                personal_data_found = False 
                
                for row in rows:
                    if row.get("MM_TYPE") == "개인":
                        extracted_data = {
                                            "YEAR": row.get("YEAR"),
                                            "MON": row.get("MON"),
                                            "MM_TYPE": row.get("MM_TYPE"),
                                            "EUS": row.get("EUS"),          # 현년 전기사용량
                                            "GUS": row.get("GUS"),          # 현년 가스사용량
                                            "WUS": row.get("WUS"),          # 현년 수도사용량
                                            "HUS": row.get("HUS"),          # 현년 지역난방 사용량
                                            "REG_DATE": row.get("REG_DATE")
                                        }
                        results.append(extracted_data)
                        personal_data_found = True
                        break
                        
                if personal_data_found:
                    print(f"[OK] {year}-{month} 개인 데이터 수집 완료")
                else:
                    print(f"[FAIL] {year}-{month} '개인' 유형 데이터가 응답에 없음.")
                    failed_calls.append(f"{year}-{month} (개인 데이터 없음)")
            else:
                error_msg = data.get("energyUseDataSummaryInfo", {}).get("RESULT", {}).get("MESSAGE", "알 수 없는 API 오류")
                print(f"[API ERROR] {year}-{month} ({result_code}): {error_msg}")
                failed_calls.append(f"{year}-{month} (API 오류)")

        else:
            print(f"[HTTP ERROR] {year}-{month} status code: {response.status_code}")
            failed_calls.append(f"{year}-{month} (HTTP 오류)")
            
    except Exception as e:
        print(f"[EXCEPTION] {year}-{month} 수집 중 오류 발생: {e}")
        failed_calls.append(f"{year}-{month} (예외 발생)")

    # API 과부하 방지 딜레이
    time.sleep(0.2) 

output_file = "energyUseDataSummaryInfo_personal_2015_2024.json"

final_json_data = {
    "start_date": START_DATE.strftime('%Y-%m'),
    "end_date": END_DATE.strftime('%Y-%m'),
    "data_count": len(results),
    "failed_months": failed_calls,
    "data": results
}

try:
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(final_json_data, f, ensure_ascii=False, indent=2)
    print(f"총 {len(results)}건 저장 완료 → {output_file}")
    print(f"실패/오류 건수: {len(failed_calls)}")
except Exception as e:
    print(f"파일 저장 중 오류 발생: {e}")
