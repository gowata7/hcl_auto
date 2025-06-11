from proxmoxer import ProxmoxAPI
from datetime import datetime, timedelta
import urllib3
import pandas as pd
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

# Sheet 이름 변환 함수
def format_sheet_name(hostname):
    hostname = hostname.replace(':8006', '')
    hostname = re.sub(r'eu-central-1\.hcloud\.io', 'FR2', hostname)
    hostname = re.sub(r'eu-central-2\.hcloud\.io', 'FR7', hostname)
    return hostname

# Excel writer 생성
with pd.ExcelWriter(f"C:\\Beomjun\\csv\\Proxmox\\proxmox_info_{current_date}.xlsx") as writer:
    for server in proxmox_servers:
        proxmox = ProxmoxAPI(server['host'], user=server['user'], password=server['password'], verify_ssl=False)

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

        final_df = merged_df[['vmid', 'name', 'node', 'status', 'cloud_init_ip', 
                              'cpu', 'maxcpu', 'mem', 'maxmem', 'disk', 'maxdisk', 'uptime']]

        # 각 서버별로 Excel Sheet 출력
        sheet_name = format_sheet_name(server['host'])
        final_df.to_excel(writer, sheet_name=sheet_name, index=False)

        print(f"Data from {server['host']} exported to sheet '{sheet_name}'")