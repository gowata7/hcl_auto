import requests
import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
import urllib3
import subprocess
from openpyxl import Workbook

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
                lb_data.append([tenant, ip, lb_name, lb_ip, lb_port, service_type])

        except requests.RequestException as e:
            print(f"❌ 오류 발생 ({ip}):", e)

        finally:
            logout(session, base_url)

    disconnect_vpn(vpn_name)
    columns = ["Tenant", "NS_IP", "LB_Name", "LB_VIP", "Port", "Service_Type"]
    return pd.DataFrame(lb_data, columns=columns)

# 최종 실행
if __name__ == "__main__":
    current_date = datetime.now().strftime("%Y%m%d")
    excel_file = f"C:\\Beomjun\\csv\\LB\\lb_info_{current_date}.xlsx"

    print("[INFO] Starting collection for FR2")
    df_fr2 = collect_lb_info("FR2", VPN_FR2_NAME, ip_list_fr2)
    
    print("[INFO] Starting collection for FR7")
    df_fr7 = collect_lb_info("FR7", VPN_FR7_NAME, ip_list_fr7)

    # Excel 파일에 저장
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df_fr2.to_excel(writer, sheet_name="FR2", index=False)
        df_fr7.to_excel(writer, sheet_name="FR7", index=False)

    print(f"\n✅ Excel 파일이 생성되었습니다: {excel_file}")
