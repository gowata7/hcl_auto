import json

def get_snmp_ips_from_json(file_path):
    """
    JSON 파일에서 SNMP 타입의 IP 주소를 추출하는 함수.

    Args:
        file_path (str): JSON 파일 경로.

    Returns:
        list: SNMP 인터페이스의 IP 주소 목록.
    """
    # JSON 파일 읽기
    with open(file_path, 'r') as file:
        data = json.load(file)

    # SNMP IP 추출
    snmp_ips = []
    for host in data["zabbix_export"]["hosts"]:
        for interface in host["interfaces"]:
            if interface.get("type") == "SNMP":
                snmp_ips.append(interface.get("ip"))

    return snmp_ips

# 사용 예시
file_path = "FR7.json"
snmp_ip_list = get_snmp_ips_from_json(file_path)
print("SNMP IPs:", snmp_ip_list)
