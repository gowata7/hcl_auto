from proxmoxer import ProxmoxAPI
import pandas as pd
import re
from lb_5 import *
from datetime import datetime, timedelta

# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 여러 Proxmox 서버 연결 정보 리스트
proxmox_servers = [
    {'host': 'proxmox-eu-central-1.hcloud.io:8006', 'user': 'root@pam', 'password': 'EUccs2!@#$'},
    {'host': 'proxmox-lms-prd-eu-central-1.hcloud.io:8006', 'user': 'root@pam', 'password': 'EUccs2!@#$'},
    {'host': 'proxmox-lms-stg-eu-central-1.hcloud.io:8006', 'user': 'root@pam', 'password': 'EUccs2!@#$'},
    {'host': 'proxmox-eu-central-2.hcloud.io:8006', 'user': 'root@pam', 'password': 'EUccs2!@#$'},
    {'host': 'proxmox-lms-prd-eu-central-2.hcloud.io:8006', 'user': 'root@pam', 'password': 'EUccs2!@#$'},
    {'host': 'proxmox-lms-stg-eu-central-2.hcloud.io:8006', 'user': 'root@pam', 'password': 'EUccs2!@#$'}
]

# uptime 변환 함수
def format_uptime(seconds):
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    return f"{days}d {hours}h"

current_date = datetime.now().strftime("%Y%m%d")

# ✅ tenant 값을 추출하는 함수
def get_tenant_from_host(host):
    if 'eu-central-1' in host:
        if 'prd' in host:
            return 'FR2-PRD'
        elif 'stg' in host:
            return 'FR2-STG'
        else:
            return 'KR2-ADMIN'
    elif 'eu-central-2' in host:
        if 'prd' in host:
            return 'FR7-PRD'
        elif 'stg' in host:
            return 'FR7-STG'
        else:
            return 'FR7-ADMIN'
    else:
        return 'UNKNOWN'


def export_proxmox(vpn_name):
    if is_vpn_connected(vpn_name):
        print(f"[INFO] VPN {vpn_name} is already connected.")
    else:
        print(f"[INFO] VPN {vpn_name} not connected. Attempting connection...")
        connect_vpn(vpn_name, USERNAME, PASSWORD)
    #current_date = datetime.now().strftime("%Y%m%d")
    all_dfs = []

    for server in proxmox_servers:
        proxmox = ProxmoxAPI(server['host'], user=server['user'], password=server['password'], verify_ssl=False)
        tenant = get_tenant_from_host(server['host'])

        cluster_resources = proxmox.cluster.resources.get(type='vm')
        cluster_df = pd.DataFrame(cluster_resources)

        vm_ip_list = []
        for node in proxmox.nodes.get():
            node_name = node['node']
            vms = proxmox.nodes(node_name).qemu.get()

            for vm in vms:
                vmid = vm['vmid']
                config = proxmox.nodes(node_name).qemu(vmid).config.get()
                ipconfig = config.get('ipconfig0', None)

                ip = None
                if ipconfig:
                    match = re.search(r'ip=([\d.]+)', ipconfig)
                    if match:
                        ip = match.group(1)

                vm_ip_list.append({
                    'vmid': int(vmid),
                    'cloud_init_ip': ip
                })

        ip_df = pd.DataFrame(vm_ip_list)
        merged_df = pd.merge(cluster_df, ip_df, on='vmid', how='left')

        merged_df['cpu'] = (merged_df['cpu'] * 100).round(2)
        merged_df['mem'] = (merged_df['mem'] / (1024**3)).round(2)
        merged_df['maxmem'] = (merged_df['maxmem'] / (1024**3)).round(2)
        merged_df['maxdisk'] = (merged_df['maxdisk'] / (1024**3)).round(2)
        merged_df['uptime'] = merged_df['uptime'].apply(format_uptime)

        merged_df['tenant'] = tenant

        final_df = merged_df[['tenant', 'vmid', 'name', 'node', 'status', 'cloud_init_ip', 
                            'cpu', 'maxcpu', 'mem', 'maxmem', 'disk', 'maxdisk', 'uptime']]
        all_dfs.append(final_df)

    # ✅ 모든 서버 데이터를 하나로 합침
    combined_df = pd.concat(all_dfs, ignore_index=True)

    # ✅ Excel로 저장 (하나의 시트)
    excel_path = f"C:\\Beomjun\\csv\\Proxmox\\proxmox_info_{current_date}.xlsx"
    combined_df.to_excel(excel_path, sheet_name="Proxmox_All", index=False)

    print(f"\n✅ All Proxmox data exported to: {excel_path}")

# 최종 실행
if __name__ == "__main__":
    export_proxmox(VPN_FR2_NAME)