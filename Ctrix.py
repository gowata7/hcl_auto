import requests

# 설정: Citrix ADC 접속 정보
NS_IP = "172.28.7.11"  # Citrix 장비 IP
USERNAME = "spark"
PASSWORD = "TldhTl1!"

BASE_URL = f"https://{NS_IP}/nitro/v1"
HEADERS = {"Content-Type": "application/json"}
VERIFY_SSL = False  # SSL 인증서 무시 (자체서명 시 True로 하면 오류)

session = requests.Session()
session.verify = VERIFY_SSL

def login():
    url = f"{BASE_URL}/config/login"
    payload = {
        "login": {
            "username": USERNAME,
            "password": PASSWORD
        }
    }
    response = session.post(url, json=payload, headers=HEADERS)
    response.raise_for_status()
    print("[+] 로그인 성공")

def get_lb_vips():
    url = f"{BASE_URL}/config/lbvserver"
    response = session.get(url, headers=HEADERS)
    response.raise_for_status()
    lb_list = response.json().get("lbvserver", [])
    
    print(f"\n📋 LB VIP 목록 (총 {len(lb_list)}개):")
    for lb in lb_list:
        print(f" - {lb.get('name')} ({lb.get('ipv46')} / {lb.get('servicetype')})")
    return lb_list

def logout():
    url = f"{BASE_URL}/config/logout"
    payload = {"logout": {}}
    response = session.post(url, json=payload, headers=HEADERS)
    response.raise_for_status()
    print("\n[+] 로그아웃 완료")

if __name__ == "__main__":
    try:
        login()
        get_lb_vips()
    except requests.RequestException as e:
        print("❌ 오류:", e)
    finally:
        logout()
