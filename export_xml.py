import xml.etree.ElementTree as ET
import csv

# ====== 설정 ======
INPUT_FILE = 'zbx_export_hosts.xml'
OUTPUT_FILE = 'snmp_ip_list.csv'

# ====== XML 파일 로드 ======
tree = ET.parse(INPUT_FILE)
root = tree.getroot()

# ====== 결과 출력 준비 ======
snmp_ips = []

# ====== SNMP 인터페이스 파싱 ======
for interface in root.findall(".//interface"):
    itype = interface.find("type")
    ip = interface.find("ip")
    
    if itype is not None and itype.text == "SNMP" and ip is not None:
        snmp_ips.append(ip.text)

# ====== 결과 출력 및 CSV 저장 ======
if snmp_ips:
    print(f"[INFO] Found {len(snmp_ips)} SNMP IP addresses.")
    
    with open(OUTPUT_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["SNMP_IP"])
        for ip in snmp_ips:
            writer.writerow([ip])
    
    print(f"[INFO] SNMP IP list saved to '{OUTPUT_FILE}'")
else:
    print("[INFO] No SNMP IP addresses found.")
