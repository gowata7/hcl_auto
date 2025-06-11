import requests
import os
import csv
from dotenv import load_dotenv
from datetime import datetime, timedelta
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# .env 로드
load_dotenv(dotenv_path="config/ctrix.env")

# 환경변수 로드
NS_IPS_FR2 = os.getenv("NS_IPS_FR2", "")
NITRO_USERNAME = os.getenv("NITRO_USERNAME")
NITRO_PASSWORD = os.getenv("NITRO_PASSWORD")
HEADERS = {"Content-Type": "application/json"}
VERIFY_SSL = False  # 자체서명 인증서 무시

# IP와 Tenant 매핑을 .env 파일에서 로드
IP_TENANT_MAPPING = {}

# .env에서 IP-Tenant 매핑 로딩
tenant_mapping = os.getenv("TENANT_MAPPING_FR2", "")
for item in tenant_mapping.split(","):
    if ":" in item:
        ip, tenant = item.split(":")
        IP_TENANT_MAPPING[ip.strip()] = tenant.strip()

print("mapping!", IP_TENANT_MAPPING)

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
    
    if lb_list:
        print("[DEBUG] Available Keys for LB Object:")
        print(lb_list[0].keys())  # 첫 번째 LB의 모든 키 출력

    return lb_list


def logout(session, base_url):
    url = f"{base_url}/config/logout"
    payload = {"logout": {}}
    session.post(url, json=payload, headers=HEADERS)


if __name__ == "__main__":
    ip_list = [ip.strip() for ip in NS_IPS_FR2.split(",") if ip.strip()]

    current_date = datetime.now().strftime("%Y%m%d")

    # CSV 파일로 결과 저장
    csv_file = f"lb_vip_list_FR2_{current_date}.csv"
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Tenant", "NS_IP", "LB_Name", "LB_VIP", "Port" , "Service_Type"])

        for ip in ip_list:
            tenant = IP_TENANT_MAPPING.get(ip, "UNKNOWN")
            print(f"ip:{ip}, tenant:{tenant}")
            base_url = f"https://{ip}/nitro/v1"
            session = requests.Session()
            session.verify = VERIFY_SSL

            try:
                login(session, base_url)
                lb_list = get_lb_vips(session, base_url)

                print(f"\n📋 LB VIP 목록 ({ip}): 총 {len(lb_list)}개")
                for lb in lb_list:
                    lb_name = lb.get('name')
                    lb_ip = lb.get('ipv46')
                    lb_port = lb.get('port')
                    service_type = lb.get('servicetype')

                    writer.writerow([tenant, ip, lb_name, lb_ip, lb_port, service_type])
                    # print(f" - {lb_name} ({lb_ip} / {service_type})")

            except requests.RequestException as e:
                print(f"❌ 오류 발생 ({ip}):", e)

            finally:
                logout(session, base_url)

    print(f"\n✅ CSV 파일이 생성되었습니다: {csv_file}")
