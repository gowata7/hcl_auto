import requests
import os
import pandas as pd
from dotenv import load_dotenv
import urllib3
import subprocess
from openpyxl import Workbook

from datetime import datetime, timedelta
from x_config import *
import psycopg2
from psycopg2.extras import RealDictCursor

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# .env 로드
load_dotenv(dotenv_path="config/ctrix.env")

# 환경변수 로드
# IP 리스트 만들기
NS_IPS_FR2 = os.getenv("NS_IPS_FR2", "").split(",")
NS_IPS_FR7 = os.getenv("NS_IPS_FR7", "").split(",")

# 각각 공백 제거
ip_list_fr2 = [ip.strip() for ip in NS_IPS_FR2 if ip.strip()]
ip_list_fr7 = [ip.strip() for ip in NS_IPS_FR7 if ip.strip()]

NITRO_USERNAME = os.getenv("NITRO_USERNAME")
NITRO_PASSWORD = os.getenv("NITRO_PASSWORD")
HEADERS = {"Content-Type": "application/json"}
VERIFY_SSL = False  # 자체서명 인증서 무시

VPN_FR2_NAME = "EU2-FR2"
VPN_FR7_NAME = "EU2-FR7"
USERNAME = "spark"
PASSWORD = "tmvkzm1!"

# IP와 Tenant 매핑 로딩
IP_TENANT_MAPPING = {}
tenant_mapping_fr2 = os.getenv("TENANT_MAPPING_FR2", "")
tenant_mapping_fr7 = os.getenv("TENANT_MAPPING_FR7", "")

for item in tenant_mapping_fr2.split(","):
    if ":" in item:
        ip, tenant = item.split(":")
        IP_TENANT_MAPPING[ip.strip()] = tenant.strip()

for item in tenant_mapping_fr7.split(","):
    if ":" in item:
        ip, tenant = item.split(":")
        IP_TENANT_MAPPING[ip.strip()] = tenant.strip()

print("mapping info!", IP_TENANT_MAPPING)

# VPN 관련 함수
def is_vpn_connected(vpn_name):
    result = subprocess.run(['rasdial'], capture_output=True, text=True)
    return vpn_name.lower() in result.stdout.lower()

def connect_vpn(vpn_name, username, password):
    print(f"[INFO] Connecting to VPN: {vpn_name}")
    subprocess.run(['rasdial', vpn_name, username, password])

def disconnect_vpn(vpn_name):
    print(f"[INFO] Disconnecting VPN: {vpn_name}")
    subprocess.run(['rasdial', vpn_name, '/disconnect'])

# Citrix API 함수
def login(session, base_url):
    url = f"{base_url}/config/login"
    payload = {"login": {"username": NITRO_USERNAME, "password": NITRO_PASSWORD}}
    response = session.post(url, json=payload, headers=HEADERS)
    response.raise_for_status()

def get_lb_vips(session, base_url):
    url = f"{base_url}/config/lbvserver"
    response = session.get(url, headers=HEADERS)
    response.raise_for_status()
    lb_list = response.json().get("lbvserver", [])
    return lb_list

def logout(session, base_url):
    url = f"{base_url}/config/logout"
    payload = {"logout": {}}
    session.post(url, json=payload, headers=HEADERS)

# LB 수집 함수
def collect_lb_info(region, vpn_name, ip_list):
    if is_vpn_connected(vpn_name):
        print(f"[INFO] VPN {vpn_name} is already connected.")
    else:
        print(f"[INFO] VPN {vpn_name} not connected. Attempting connection...")
        connect_vpn(vpn_name, USERNAME, PASSWORD)

    lb_data = []
    for ip in ip_list:
        tenant = IP_TENANT_MAPPING.get(ip, "UNKNOWN")
        print(f"[INFO] Collecting LB info from {tenant} ({ip})")
        base_url = f"https://{ip}/nitro/v1"
        session = requests.Session()
        session.verify = VERIFY_SSL

        try:
            login(session, base_url)
            lb_list = get_lb_vips(session, base_url)

            for lb in lb_list:
                lb_name = lb.get('name')
                lb_ip = lb.get('ipv46')
                lb_port = lb.get('port')
                service_type = lb.get('servicetype')
                
                if lb_ip == "0.0.0.0":
                    continue
                
                lb_data.append([tenant, ip, lb_name, lb_ip, lb_port, service_type])

        except requests.RequestException as e:
            print(f"❌ 오류 발생 ({ip}):", e)

        finally:
            logout(session, base_url)

    disconnect_vpn(vpn_name)
    
    return lb_data  # ✅ DataFrame이 아닌 리스트 반환

def get_this_week_range():
    from datetime import datetime, timedelta
    today = datetime.now().date()
    weekday = today.weekday()  # 0=월, 1=화, ..., 6=일

    # 전주 동일 요일부터 오늘까지
    start_date = today - timedelta(days=7)
    end_date = today

    return start_date, end_date

def fetch_weekly_added_lbs():
    start_date, end_date = get_this_week_range()
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT 
                tenant, lb_name, lb_vip, port, service_type,
                make_date(year::int, month::int, day::int) AS date
            FROM added_loadbalancers
            WHERE make_date(year::int, month::int, day::int) BETWEEN %s AND %s
            ORDER BY date;
        """, (start_date, end_date))
        rows = cur.fetchall()
    conn.close()
    return rows

def fetch_weekly_deleted_lbs():
    start_date, end_date = get_this_week_range()
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT 
                tenant, lb_name, lb_vip, port, service_type,
                make_date(year::int, month::int, day::int) AS date
            FROM deleted_loadbalancers
            WHERE make_date(year::int, month::int, day::int) BETWEEN %s AND %s
            ORDER BY date;
        """, (start_date, end_date))
        rows = cur.fetchall()
    conn.close()
    return rows

def compare_yesterday():
    from datetime import datetime, timedelta
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


def add_document_lb(df_today, df_added, df_deleted):
    from datetime import datetime, timedelta
    current_date = datetime.now().strftime("%Y%m%d")

    document.add_heading('LB 현황', level=1) 
    total = len(df_today)
    
    document.add_paragraph(f'총 {total}건', style='List Bullet')

    # Pivoting
    df = preprocess_df_LB(df_today)
    # pivot, total = getPivotTable(df, month)
    
    # Chart - Pie 차트
    region_pivot, _ = getPivotTable_new(df, 'Tenant')
    # tenant_pivot, _ = getPivotTable_new(df, 'Tenant')
    
    source1 = region_pivot
    # source2 = tenant_pivot
    
    print(source1)
    # print(source2)
    
    # Chart
    # if incompleted == 0:
    chart1 = getPieChart_tenant(source1)
    # chart2 = getPieChart_tenant(source2)
    # else:
    #     source = flatten_2d(data)
    #     chart = getStackedHBarChart(source)    
    
    # source = pivot
    # if incompleted == 0:
    #     chart = getPieChart(source)
    # else:
    #     chart = getStackedHBarChart1(source)
    chart1.save(f'./charts/LB_1.png')
    # chart2.save(f'./charts/vm_2.png')

    # p = document.add_paragraph('')
    # run = p.add_run()
    # run.add_break(WD_BREAK.LINE)
    
    table = document.add_table(rows=1, cols=1)
    cell = table.rows[0].cells[0]
    paragraph = cell.paragraphs[0]
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER  # 수평 중앙 정렬
    run = paragraph.add_run("테넌트별")
    run.font.size = Pt(12)  # 폰트 크기 조절 (선택)
    run.bold = True  # 굵게 (선택)
    
    # 이미지 추가 (별도 문단 생성하여 아래로 정렬되게)
    paragraph_img = cell.add_paragraph()
    paragraph_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_img = paragraph_img.add_run()
    run.add_picture(f'./charts/LB_1.png')
    # run.add_picture(f'./charts/LB_1.png', width=Inches(3.3))
    
    # Document
    document.add_paragraph(f'전일 대비 추가된 LB({len(df_added)}건)', style='List Bullet')
    
    if len(df_added) == 0:
        pass
    else:
        addTable_LB(df_added)
        
    p = document.add_paragraph('')
    run = p.add_run()
    run.add_break(WD_BREAK.LINE)
    
    document.add_paragraph(f'전일 대비 삭제된 LB({len(df_deleted)}건)', style='List Bullet')
    # A-B (삭제된 건)
    # df_result_sub = pd.concat([df_premonth,df_curmonth,df_curmonth]).drop_duplicates(keep=False)
    # print(df_result_sub)
    
    if len(df_deleted) == 0:
        pass
    else:
        addTable_LB(df_deleted)

    p = document.add_paragraph('')
    run = p.add_run()
    run.add_break(WD_BREAK.LINE)

    start_date, end_date = get_this_week_range()

    fetch_weekly_added_lbs()
    weekly_lbs_added = fetch_weekly_added_lbs()
    df_weekly_added = pd.DataFrame(weekly_lbs_added)
    print("weekly_lbs_added:", df_weekly_added)
    document.add_paragraph(f'1주 간({start_date}~{end_date}) 생성된 LB 목록 ({len(df_weekly_added)}건)', style='List Bullet')
    
    if weekly_lbs_added:
        addTable_loadbalancer(df_weekly_added)
    else:
        document.add_paragraph('1주 간 생성된 LB이 없습니다.', style='List Bullet')
    
    p = document.add_paragraph('')
    run = p.add_run()
    run.add_break(WD_BREAK.LINE)

    fetch_weekly_deleted_lbs()
    weekly_lbs_deleted = fetch_weekly_added_lbs()
    df_weekly_deleted = pd.DataFrame(weekly_lbs_deleted)
    print("weekly_lbs_deleted:", df_weekly_deleted)
    document.add_paragraph(f'1주 간({start_date}~{end_date}) 삭제된 LB 목록 ({len(df_weekly_deleted)}건)', style='List Bullet')
    
    if weekly_lbs_deleted:
        addTable_loadbalancer(df_weekly_deleted)
    else:
        document.add_paragraph('1주 간 삭제된 LB이 없습니다.', style='List Bullet')

    document.add_page_break()

    document.save(f'C:\\Beomjun\\csv\\total_report_{current_date}.docx')

# 최종 실행
if __name__ == "__main__":

    current_date = datetime.now().strftime("%Y%m%d")
    ods_file = f"C:\\Beomjun\\csv\\LB\\lb_info_{current_date}.ods"

    print("[INFO] Starting collection for FR2")
    fr2_data = collect_lb_info("FR2", VPN_FR2_NAME, ip_list_fr2)

    print("[INFO] Starting collection for FR7")
    fr7_data = collect_lb_info("FR7", VPN_FR7_NAME, ip_list_fr7)

    # ✅ 데이터 병합
    combined_data = fr2_data + fr7_data
    columns = ["Tenant", "NS_IP", "LB_Name", "LB_VIP", "Port", "Service_Type"]
    df_combined = pd.DataFrame(combined_data, columns=columns)

    # # ✅ ODS 파일 저장
    with pd.ExcelWriter(ods_file, engine='odf') as writer:
        df_combined.to_excel(writer, sheet_name="LB_Info", index=False)

    df_added, df_deleted = compare_yesterday()
    add_document_lb(df_combined, df_added, df_deleted)
    
    print(f"\n✅ ODS 파일이 생성되었습니다: {ods_file}")