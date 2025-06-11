import requests
import os
import pandas as pd
from dotenv import load_dotenv
import urllib3
import subprocess
from openpyxl import Workbook

from datetime import datetime, timedelta
# from x_config import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def compare_yesterday():
    # 날짜 설정
    current_date = datetime.now().strftime("%Y%m%d")
    yesterday_date = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
    
    print("today:", current_date)
    print("yesterday:", yesterday_date)
    
    # 경로 설정
    today_path = f"C:\\Beomjun\\csv\\LB\\lb_info_{current_date}.ods"
    yesterday_path = f"C:\\Beomjun\\csv\\LB\\lb_info_{yesterday_date}.ods"
    
    # file_path=os.path.abspath("")
    # srcpath = findfile(f"eu_adminrc_{yesterday_date}.csv.org", file_path)
    # dir, file = os.path.split(srcpath)
    # shutil.copy2(srcpath, dir+f"\eu_adminrc_{yesterday_date}.csv")
        
    # CSV 로드
    df_today = pd.read_excel(today_path, engine='odf')
    df_yesterday = pd.read_excel(yesterday_path, engine='odf')
    
    print(f"yesterday length: {len(df_today)}")
    print(f"today length: {len(df_yesterday)}")

    # 고유 키 생성: Tenant:LB_Name
    df_today['key'] = df_today['Tenant'].astype(str) + ':' + df_today['LB_Name'].astype(str)
    df_yesterday['key'] = df_yesterday['Tenant'].astype(str) + ':' + df_yesterday['LB_Name'].astype(str)

    # 차집합 연산
    today_keys = set(df_today['key'])
    yesterday_keys = set(df_yesterday['key'])

    added_keys = today_keys - yesterday_keys
    deleted_keys = yesterday_keys - today_keys

    df_added = df_today[df_today['key'].isin(added_keys)]
    df_deleted = df_yesterday[df_yesterday['key'].isin(deleted_keys)]
    
    # 결과 출력
    print("\n✅ 오늘 추가된 LB:")
    print(df_added)
    
    print("\n❌ 오늘 삭제된 LB:")
    print(df_deleted)

    return df_added, df_deleted

# 최종 실행
if __name__ == "__main__":

    current_date = datetime.now().strftime("%Y%m%d")
    ods_file = f"C:\\Beomjun\\csv\\LB\\lb_info_{current_date}.ods"

    df_added, df_deleted = compare_yesterday()