from io import BytesIO
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime
from PIL import Image
from time import sleep
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
mpl.rcParams['axes.unicode_minus']=False

import os
import glob




screenshots_path = 'ScreenShots'

isExist = os.path.exists(screenshots_path)
if not isExist:
    os.makedirs(screenshots_path)
    print("The new directory is created!")

# 리포트 폴더 지정
pdf_path = 'Reports'

# 리포트 폴더 존재 유무 체크 (필요 시 생성)
isExist = os.path.exists(pdf_path)
if not isExist:
    os.makedirs(pdf_path)
    print("The new directory is created!")



    


def createpdf(region):
    
    sentence_dict = {
        "KR": {
            "sentence_h1": [
                'KR1 상단 레거시 네트워크 - ISP회선(Internet, SMS, AWS) Traffic, FW CPU/Session',
                'KR2 상단 네트워크 - ISP회선(Internet, 차량DATA/SMS, AWS) Traffic',
                'KR1 TMS L7 - CPU,Memory,Connection,SNAT Pool Status, L7↔Backbone Traffic',
                'KR1 Cloud L7 - CPU, Memory, Service/SNAT Connection',
                'KR1 Network - CGN CPU,MEM, A10/F5 ServiceConnection, BorderLeaf/CGN Traffic',
                'KR2 Network - 의왕↔상암 전용회선 Traffic, Edge↔Router Traffic, NetworkLeaf↔FW/L7 Traffic, FW/L7 CPU/Memory/Connection',
                'KR1 TMS BM - CPU, Memory, Disk Free(%)',
                'KR1 Cloud BM - CPU, Memory, Disk Free(%)',
                'KR2 BM - CPU, Memory, Disk Free(%)',
                'KR1 VM - CPU, Memory, Disk Free(%)',
                'KR2 VM - CPU, Memory, Disk Free(%)',
                'KR1 DB - CPU, Memory, session',
                'KR2 DB - CPU, Memory, session',
                'KR1 CLOUD Netapp(NVME) - DISK usage, Spine↔Netapp CinderTraffic',
                'KR1 TMS,CDO Netapp(SAS,SSD) - DISK usage, Spine↔Netapp CinderTraffic',
                'KR1 TMS Netapp(SAS,SSD) - DISK usage, Spine↔Netapp CinderTraffic',
                'Storage: 1센터 신운영계 스토리지 클러스터 #1의 IOPS, Throughput 정보',
                'Storage: 1센터 신운영계 스토리지 클러스터 #2의 IOPS, Throughput 정보',
                'Storage: 1센터 구운영계 스토리지 클러스터의 IOPS, Throughput 정보',
                '',
                '',
                '',
                'Storage: 2센터 운영계 스토리지 클러스터 #1의 IOPS, Throughput 정보',
                'Storage: 2센터 운영계 스토리지 클러스터 #2의 IOPS, Throughput 정보',
                'Storage: 2센터 운영계 스토리지 클러스터 #3의 IOPS, Throughput 정보',
                'Storage: 2센터 운영계 스토리지 클러스터 #4의 IOPS, Throughput 정보',
                'Storage: 2센터 운영계 스토리지 클러스터 #5의 IOPS, Throughput 정보',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
            ],
            "sentence_h2": [
                '',
                '',
                '메모리 70% 이상 일경우 유의하여 모니터링',
                '',
                '',
                'IP 1개당 최대 NAT Connection 약 63000여개',
                'BM(Bare Metal): CCS내 모든 물리서버 대상 Worst Top 10 정보. Red가 아니면 모두 정상 (Red 기준 : CPU 10% 이하, 메모리 1G이하, free Disk 10% 이하)',
                'BM(Bare Metal): CCS내 모든 물리서버 대상 Worst Top 10 정보. Red가 아니면 모두 정상 (Red 기준 : CPU 10% 이하, 메모리 1G이하, Usage 90% 이상)',
                'BM(Bare Metal): CCS내 모든 물리서버 대상 Worst Top 10 정보. Red가 아니면 모두 정상 (Red 기준 : CPU 10% 이하, 메모리 3G이하, Usage 90% 이상)',
                'VM: CCS내 모든 가상서버 대상 Worst Top 10 정보 (Red 기준 : CPU 10% 이하, 메모리 500M이하, free Disk 10% 이하)',
                'VM: CCS내 모든 가상서버 대상 Worst Top 10 정보 (Red 기준 : CPU 10% 이하, 메모리 500M이하, free Disk 10% 이하)',
                '',
                '',
                '',
                '',
                '',
                '비교 수치 일평균 peak iops / peak throughput (Mbps)',
                '비교 수치 일평균 peak iops / peak throughput (Mbps)',
                '비교 수치 일평균 peak iops / peak throughput (Mbps)',
                '',
                '',
                '',
                '비교 수치 일평균 peak iops / peak throughput (Mbps)',
                '비교 수치 일평균 peak iops / peak throughput (Mbps)',
                '비교 수치 일평균 peak iops / peak throughput (Mbps)',
                '비교 수치 일평균 peak iops / peak throughput (Mbps)',
                '비교 수치 일평균 peak iops / peak throughput (Mbps)',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
            ],
            "sentence_h3": [
                'http://10.7.19.118:3000/d/Ax-HFsa4z/yiwang-ccs-bordermoniteoring-keulraudeuunyeongsenteo?orgId=1&from=now-2d&to=now&refresh=30m',
                'https://hubble-apne2-prd.platform.hcloud.io/grafana/d/RbJ9FxXnk/inteones-caryang-data-sms-hoeseon?orgId=13&from=now-2d&to=now',
                'http://10.11.67.29:3000/d/tdbzxsNnz1/kr-a10-3030-old-a10?orgId=1&refresh=5m&from=now-2d&to=now',
                'http://10.11.67.29:3000/d/ixuLyos7k/kr-lb-f5?from=now-2d&to=now&orgId=1&refresh=5m',
                'http://10.11.67.29:3000/d/-zbrCFr7g/1senteo-ccs-neteuweokeu-jonghab-moniteoring?orgId=1&from=now-2d&to=now',
                'http://10.11.67.29:3000/d/9zxCEzp4k/kr-2senteo-prd-ccs-neteuweokeu-jonghab-moniteoring?orgId=1&refresh=5m',
                'http://10.11.67.29:3000/d/vGUN6GW4z/kr-1senteo-prd-old-bm-resources?orgId=1&from=now-30m&to=now&refresh=30m',
                'http://10.11.67.29:3000/d/yo86eMWVz/kr-1senteo-prd-new-bm-resources?orgId=1&from=now-30m&to=now&refresh=30m',
                'http://10.11.67.29:3000/d/U_asi7W4z/kr-2senteo-prd-bm-resources?orgId=1&refresh=30m&from=now-30m&to=now',
                'http://10.11.67.29:3000/d/yVNMjMZVk/kr-1senteo-prd-vm-resources?orgId=1&refresh=30m&from=now-30m&to=now',
                'http://10.11.67.29:3000/d/Jxvrz7Z4k/kr-2senteo-prd-vm-resources?orgId=1&from=now-30m&to=now&refresh=30m',
                'http://10.11.67.29:3000/d/JU5R-_m4k/kr-1senteo-prd-db-resource-usage-top-20?orgId=1&from=now-6h&to=now&refresh=30m',
                'http://10.11.67.29:3000/d/bxdzB_iVz/kr-2senteo-prd-db-resource-usage-top-20?orgId=1&refresh=30m&from=now-6h&to=now',
                'http://10.11.67.29:3000/d/MWXLP7K4z1/kr-1center-netapp-nvme-dash-board?orgId=1&refresh=1d',
                'http://10.11.67.29:3000/d/jhvYINK4z2/kr-1centor-old-prd-and-new-prd-big-data?orgId=1&refresh=1d',
                'http://10.11.67.29:3000/d/gHJ-NHK4k3/kr-1centor-stg-netapp-dash-board?orgId=1&refresh=1d',
                'https://10.7.0.231/clusters/53770/explorer',
                'https://10.7.0.231/clusters/133326/explorer',
                'https://10.7.0.231/clusters/15462/explorer',
                'http://10.11.67.29:3000/d/ytGbd1UVk/kr2-prd_netapp?orgId=1&refresh=1d',
                'http://10.11.67.29:3000/d/IFrv6NWIk/kr-2center-netapp-prd-manila?orgId=1&refresh=1d',
                'http://10.11.67.29:3000/d/LIdYdJU4z/kr2_stg_netapp?orgId=1',
                'https://172.16.9.211/sysmgr/v4/',
                'https://172.16.9.216/sysmgr/v4/',
                'https://172.16.9.221/sysmgr/v4/',
                'https://172.16.9.226/sysmgr/v4/',
                'https://172.16.9.231/sysmgr/v4/',
                'https://hubble-apne2-prd.platform.hcloud.io/grafana/d/coBoVkG4z/kr-apne1-rancher-local?orgId=27',
                'http://10.11.67.29:3000/d/1HihRd54k/coc-k8s-summary-dashboard-alert-system-kr1-kr_devworks_prd_cluster?orgId=1',
                'http://10.11.67.29:3000/d/oOYkgdc4z/coc-k8s-summary-dashboard-alert-system-kr1-dkc2-hpkr?orgId=1',
                'http://10.11.67.29:3000/d/95RgRd54z/coc-k8s-summary-dashboard-alert-system-kr1-dkc2-kpg?orgId=1',
                'http://10.11.67.29:3000/d/q20rev5Vz/coc-k8s-summary-dashboard-alert-system-kr1-dkc2-kpl?orgId=1',
                'http://10.11.67.29:3000/d/X0-SRdc4z/coc-k8s-summary-dashboard-alert-system-kr1-kr_svchub_prd_cluster?orgId=1',
                'http://10.11.67.29:3000/d/Zx4vgdcVz/coc-k8s-summary-dashboard-alert-system-kr1-kr_svchubcore_prd_cluster?orgId=1',
                'http://10.11.67.29:3000/d/KeocRd5Vz/coc-k8s-summary-dashboard-alert-system-kr1-kr_svchubutil_prd_cluster?orgId=1',
                'http://10.11.67.29:3000/d/Njzv9SZIk/coc-k8s-summary-dashboard-alert-system-krbig-vdsp-prd?orgId=1',
                'http://10.11.67.29:3000/d/Ig7ngd5Vk/coc-k8s-summary-dashboard-alert-system-kr1-kr_vtwin_prd_cluster?orgId=1',
                'http://10.11.67.29:3000/d/8IhZgdcVz/coc-k8s-summary-dashboard-alert-system-kr1-kr_vtwin2_prd_cluster?orgId=1',
                'https://hubble-apne2-prd.platform.hcloud.io/grafana/d/GgRmDQ-4z/kr_apne2_rancher_cluster-prd?orgId=27',
                'https://hubble-apne2-prd.platform.hcloud.io/grafana/d/rBwSwVJVk/ccs_prd_cluster?orgId=27',
            ]
        },
        "EU": {
            "sentence_h1": [
                '',
                '',
                '',
                'BM(Bare Metal): CCS내 모든 물리서버 대상 Worst Top 10 정보. Red가 아니면 모두 정상',
                'VM: CCS EU 내 모든 가상서버 대상 Worst Top 10  정보.',
                'EU DB : EU PRD DB 정보 (CPU, Memory, session)',
                '',
                'Storage: 운영계 스토리지 클러스터 의 IOPS, Throughput 정보',
                '',
                '',
                '',
                '',
                '',
            ],
            "sentence_h2": [
                '',
                '',
                '',
                '(Red 기준 : CPU 10% 이하, 메모리 300M이하, free Disk 10% 이하)',
                '(Red 기준 : CPU 10% 이하, 메모리 500M이하, free Disk 10% 이하) ',
                '',
                '',
                '',
                '비교 수치 일평균 peak iops / peak throughput (Mbps)',
                '',
                '',
                '',
                '',
            ],
            "sentence_h3": [
                'http://10.11.67.29:3000/d/BfKKMwcVz/eutms-a10-resource-monitor?orgId=1&refresh=5m',
                'http://10.11.67.29:3000/d/HK5wzuFVk2/eutms-fw_resource-monitor?orgId=1&refresh=5m',
                'http://10.11.67.29:3000/d/MtWXiuFVz/eu-prd-ccs-neteuweokeu-jonghab-moniteoring?orgId=1',
                'http://10.11.67.29:3000/d/ZdXDq9F4k/eu-bm-and-netapp-resource?orgId=1',
                'http://10.11.67.29:3000/d/_us9CrK4z/eu-vm-resource?orgId=1',
                'http://10.11.67.29:3000/d/t4xORuFVz/eu-prd-db-resource-usage-top-20?orgId=1',
                'http://10.11.67.29:3000/d/y0-T77cVk/eu_mongodb?orgId=1',
                'http://10.11.67.29:3000/d/bhPMpo54k/eu-netapp-dash-board',
                'https://10.7.0.231/clusters/69010/explorer',
                'http://10.11.67.29:3000/d/k4uJRdc4z/coc-k8s-summary-dashboard-alert-system-eu-1?orgId=1',
                'http://10.11.67.29:3000/d/BBEbgOc4k/coc-k8s-summary-dashboard-alert-system-eu-2?orgId=1',
                'http://10.11.67.29:3000/d/6yD-Rdc4k/coc-k8s-summary-dashboard-alert-system-eu-3?orgId=1',
                'http://10.11.67.29:3000/d/niGBgO5Vz/coc-k8s-summary-dashboard-alert-system-eu-4?orgId=1',
            ]
        },
        "RU": {
            "sentence_h1": [
                '',
                '',
                '',
                'BM(Bare Metal): CCS내 모든 물리서버 대상 Worst Top 10 정보. Red가 아니면 모두 정상',
                'VM: CCS내 모든 가상서버 대상 Worst Top 10  정보.',
                'RU DB : RU PRD DB 정보 (CPU, Memory, session)',
                'Storage: 운영계 스토리지 클러스터 의 IOPS, Throughput 정보',
                '',
            ],
            "sentence_h2": [
                '',    
                '',
                '',
                '(Red 기준 : CPU 10% 이하, 메모리 1G이하, free Disk 10% 이하)',
                '(Red 기준 : CPU 10% 이하, 메모리 500M이하, free Disk 10% 이하)',
                '',
                '비교 수치 일평균 peak iops / peak throughput (Mbps)',
                '',
            ],
            "sentence_h3": [
                'http://10.11.67.29:3000/d/MYEQGw5Vk/rutms-a10-resource-monitor?orgId=1',
                'http://10.11.67.29:3000/d/HK5wzuFVkasdf/rutms-fw_resource-monitor?orgId=1',
                'http://10.11.67.29:3000/d/-FwPmOcVz/ru-prd-ccs-neteuweokeu-jonghab-moniteoring?orgId=1&refresh=1h',
                'http://10.11.67.29:3000/d/rDJA39K4z/ru-bm-and-netapp-resource?orgId=1',
                'http://10.11.67.29:3000/d/HEd3C9FVk/ru-vm-resource?orgId=1',
                'http://10.11.67.29:3000/d/3MMHzXKVz/ru-prd-db-resource-usage-top-20?orgId=1',
                'https://10.7.0.231/clusters/70559/explorer',
                'http://10.11.67.29:3000/d/Rv-oDy54k/ru-netapp-dash-board?orgId=1',
            ]
        },
        "NA": {
            "sentence_h1": [
                '',
                '',
                '',
                'BM(Bare Metal): CCS NA 내 모든 물리서버 대상 Worst Top 10 정보. Red가 아니면 모두 정상',
                'VM: CCS NA 내 모든 가상서버 대상 Worst Top 10  정보.',
                'NA DB : NA PRD DB 정보 (CPU, Memory, session)',
                '',
                '',
                'Storage: 운영계 스토리지 클러스터 의 IOPS, Throughput 정보',
                'Storage: 운영계 스토리지 클러스터 의 IOPS, Throughput 정보',
                '',
                '',
                '',
                '',
                '',
            ],
            "sentence_h2": [
                '',
                '',
                '',
                '(Red 기준 : CPU 10% 이하, 메모리 1G이하, free Disk 10% 이하)',
                '(Red 기준 : CPU 10% 이하, 메모리 500M이하, free Disk 10% 이하)',
                '',
                '',
                '',
                '비교 수치 일평균 peak iops / peak throughput (Mbps)',
                '비교 수치 일평균 peak iops / peak throughput (Mbps)',
                '',
                '',
                '',
                '',
                '',
            ],
            "sentence_h3": [
                 'http://10.11.67.29:3000/d/EHCxmuK4k/natms-a10-resource-monitor?orgId=1',
                'http://10.11.67.29:3000/d/HK5wzuFVk22/natms-fw_resource-monitor?orgId=1&refresh=5m',
                'http://10.11.67.29:3000/d/--HdWuF4k/na-prd-ccs-neteuweokeu-jonghab-moniteoring?orgId=1',
                'http://10.11.67.29:3000/d/67-wNjK4k/na-bm-and-netapp-resource?orgId=1',
                'http://10.11.67.29:3000/d/0azeCrF4k/na-vm-resource?orgId=1',
                'http://10.11.67.29:3000/d/7DOFRuKVz/na-prd-db-resource-usage-top-20?orgId=1',
                'http://10.11.67.29:3000/d/1Igbn754k/na_mongodb?orgId=1',
                'http://10.11.67.29:3000/d/LjsjmuF4z/na-prd-netapp-dash-board?orgId=1',
                'https://10.7.0.231/clusters/6035/explorer',
                'https://10.7.0.231/clusters/82788/explorer',
                'http://10.11.67.29:3000/d/DJdDeD5Vz/coc-k8s-summary-dashboard-alert-system-na-1?orgId=1',
                'http://10.11.67.29:3000/d/FnMc6vc4k/coc-k8s-summary-dashboard-alert-system-na-2?orgId=1',
                'http://10.11.67.29:3000/d/iBqceD5Vk/coc-k8s-summary-dashboard-alert-system-na-3?orgId=1',
                'http://10.11.67.29:3000/d/lxRheD5Vz/coc-k8s-summary-dashboard-alert-system-na-4?orgId=1',
                'http://10.11.67.29:3000/d/OYNJ6v5Vz/coc-k8s-summary-dashboard-alert-system-na-5?orgId=1',
            ]
        },
        "SG": {
            "sentence_h1": [
                '',
                '',
                '',
                'BM(Bare Metal): CCS SG 내 모든 물리서버 대상 Worst Top 10 정보. Red가 아니면 모두 정상',
                'VM: CCS SG 내 모든 가상서버 대상 Worst Top 10  정보.',
                'SG DB : SG PRD DB 정보 (CPU, Memory, session)',
                '',
                'Storage: 운영계 스토리지 클러스터 의 IOPS, Throughput 정보',
                'Storage: 운영계 스토리지 클러스터 의 IOPS, Throughput 정보',
                '',
                '',
                '',
                '',
                '',
                '',
            ],
            "sentence_h2": [
                '',
                '',
                '',
                '(Red 기준 : CPU 10% 이하, 메모리 3G이하, free Disk 10% 이하)',
                '(Red 기준 : CPU 10% 이하, 메모리 370M이하, free Disk 10% 이하)',
                '',
                '',
                '',
                '비교 수치 일평균 peak iops / peak throughput (Mbps)',
                '비교 수치 일평균 peak iops / peak throughput (Mbps)',
                '',
                '',
                '',
                '',
                '',
            ],
            "sentence_h3": [
                'http://10.11.67.29:3000/d/sjElzXFVk/sg_f5_monitor?orgId=1',
                'http://10.11.67.29:3000/d/0kQdZuFVk/sg-fw-monitor?orgId=1',
                'http://10.11.67.29:3000/d/qstVWXF4z/sg-prd-ccs-neteuweokeu-jonghab-moniteoring?orgId=1',
                'http://10.11.67.29:3000/d/dPViDjKVk/sg-bm-and-netapp-resource?orgId=1',
                'http://10.11.67.29:3000/d/5bY3CrK4z/sg-vm-resource?orgId=1',
                'http://10.11.67.29:3000/d/RJrKguFVz/sg-prd-db-resource-usage-top-20?orgId=1',
                'http://10.11.67.29:3000/d/sWpQ77c4k/sg_mongodb?orgId=1',
                'http://10.11.67.29:3000/d/Bh1NWuF4k/sg-netapp-dash-board?orgId=1',
                'https://10.107.48.110/sysmgr/v4/',
                'https://10.107.48.130/sysmgr/v4/',
                'http://10.11.67.29:3000/d/s-HlRO5Vk/coc-k8s-summary-dashboard-alert-system-1',
                'http://10.11.67.29:3000/d/6bgugO5Vk/coc-k8s-summary-dashboard-alert-system-2?orgId=1',
                'http://10.11.67.29:3000/d/26t9gdcVz/coc-k8s-summary-dashboard-alert-system-3?orgId=1',
                'http://10.11.67.29:3000/d/1R13gO54k/coc-k8s-summary-dashboard-alert-system-4?orgId=1',
                'http://10.11.67.29:3000/d/bxw6gOc4z/coc-k8s-summary-dashboard-alert-system-5?orgId=1',
            ]
        },
        "CN": {
            "sentence_h1": [
                '',
                '',
                '',
                'BM(Bare Metal): CCS CN 내 모든 물리서버 대상 Worst Top 10 정보. Red가 아니면 모두 정상',
                'VM: CCS CN 내 모든 가상서버 대상 Worst Top 10  정보.',
                'CN DB : CN PRD DB 정보 (CPU, Memory, session)',
                '',
                'Storage: 운영계 스토리지 클러스터 의 IOPS, Throughput 정보',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
            ],
            "sentence_h2": [
                '',
                '',
                '',
                '(Red 기준 : CPU 10% 이하, 메모리 500M이하, free Disk 10% 이하)',
                '(Red 기준 : CPU 10% 이하, 메모리 300M이하, free Disk 10% 이하)',
                '',
                '',
                '비교 수치 일평균 peak iops / peak throughput (Mbps)',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
            ],
            "sentence_h3": [
                'http://10.11.67.29:3000/d/CNA10PRDMON/cntms-a10-resource-monitor-2?orgId=1&from=now-24h&to=now',
                'http://10.11.67.29:3000/d/HK5wzuFVk/cntms-fw_resource-monitor?orgId=1',             
                'http://10.11.67.29:3000/d/KEzWdkx4k/cn-prd-ccs-neteuweokeu-jonghab-moniteoring_cn_local_bm?orgId=1',
                'http://10.11.67.29:3000/d/y8fH39F4z/cn-bm-and-netapp-resource_cn_bm?orgId=1',
                'http://10.11.67.29:3000/d/0wC_C9KVk/cn-vm-resource?orgId=1',
                'http://10.11.67.29:3000/d/cuCvRXFVz/cn-prd-db-resource-usage-top-20?orgId=1',
                'http://10.11.67.29:3000/d/UV_0nn54z/cn_mongodb?orgId=1',
                'http://10.11.67.29:3000/d/gCFdtpc4k/cn-netapp-dash-board?orgId=1',
                'https://10.7.0.231/clusters/124202/explorer',
                'http://10.11.67.29:3000/d/6-ohBrAVk/coc-k8s-summary-dashboard-alert-system-hpg?orgId=1',
                'http://10.11.67.29:3000/d/tPHGkO54z/coc-k8s-summary-dashboard-alert-system-2?orgId=1',
                'http://10.11.67.29:3000/d/0SInzdcVk/coc-k8s-summary-dashboard-alert-system-3?orgId=1',
                'http://10.11.67.29:3000/d/gTW4kOcVz/coc-k8s-summary-dashboard-alert-system-4?orgId=1',
                'http://10.11.67.29:3000/d/HUDSkd54k/coc-k8s-summary-dashboard-alert-system-5?orgId=1',
                'http://10.11.67.29:3000/d/qSoHkdcVz/coc-k8s-summary-dashboard-alert-system-6?orgId=1',
                'http://10.11.67.29:3000/d/cYaDzOcVk/coc-k8s-summary-dashboard-alert-system-7?orgId=1',
                'http://10.11.67.29:3000/d/pJ-dkO5Vz/coc-k8s-summary-dashboard-alert-system-8?orgId=1',
                'http://10.11.67.29:3000/d/vRN5zOcVk/coc-k8s-summary-dashboard-alert-system-9?orgId=1',
            ] 
         },
        "Jennifer": {
            "sentence_h1": [
                '',
                '',
                '',
                '',
                '',
            ],
            "sentence_h2": [
                '',
                '',
                '',
                '',
                '',
            ],
            "sentence_h3": [
                '',
                '',
                '',
                '',
                '',
            ] 
         }
    }
     
    # 언어에 따른 문장 선택
    if region in sentence_dict:

        sentences = sentence_dict[region]
        sentence_h1 = sentences["sentence_h1"]
        sentence_h2 = sentences["sentence_h2"]
        sentence_h3 = sentences["sentence_h3"]
    
    else:
        print("Unsupported language:", region)
        return


    
    if region == 'KR':
        common_filenames = [
            "01_%s_network_*.png",
            "02_%s_network_2_*.png",
            "03_%s_lb_a10_*.png",
            "04_%s_lb_f5_*.png",
            "05_%s_total_1_*.png",
            "06_%s_total_2_*.png",
            "07_%s_host_1_*.png",
            "08_%s_host_1_new_*.png",
            "09_%s_host_2_*.png",
            "10_%s_vm_1_*.png",
            "11_%s_vm_2_*.png",
            "12_%s_database_1_*.png",
            "13_%s_database_2_*.png",
            "14_%s_netapp_nvme_*.png",
            "15_%s_netapp_old_new_prd_bigdata_*.png",
            "16_%s_netapp_stg_*.png",
            "17_%s_storage_new_1_*.png",
            "18_%s_storage_new_2_*.png",
            "19_%s_storage_old_1_*.png",
            "20_%s_netapp_prd_2center_*.png",
            "21_%s_netapp_manila_prd_2center_*.png",
            "22_%s_netapp_stg_2center_*.png",
            "23_%s_storage_2center_fas_03r02_*.png",
            "24_%s_storage_2center_aff_03r02_*.png",
            "25_%s_storage_2center_fas_03r03_*.png",
            "26_%s_storage_2center_aff_03r03_*.png",
            "27_%s_storage_2center_fas_03r04_*.png",
            "28_%s_k8s_cluster_1center_ccskr_rancher_prd_*.png",
            "29_%s_k8s_cluster_1center_ccskr_devworks_prd_*.png",
            "30_%s_k8s_cluster_1center_ccskr_dkc2hpkr_prd_*.png",
            "31_%s_k8s_cluster_1center_ccskr_dkc2kpgkr_prd_*.png",
            "32_%s_k8s_cluster_1center_ccskr_dkc2kplkr_prd_*.png",
            "33_%s_k8s_cluster_1center_ccskr_svchub_prd_*.png",
            "34_%s_k8s_cluster_1center_ccskr_svchubcore_prd_*.png",
            "35_%s_k8s_cluster_1center_ccskr_svchubutil_prd_*.png",
            "36_%s_k8s_cluster_1center_kr_vdsp_prd_*.png",
            "37_%s_k8s_cluster_1center_ccskr_vtwin_prd_*.png",
            "38_%s_k8s_cluster_1center_ccskr_vtwin2_prd_*.png",
            "39_%s_k8s_cluster_2center_ccskr2_rancher_prd_*.png",
            "40_%s_k8s_cluster_2center_ccs_prd_*.png",
    ]
        
    elif region == 'EU':
        common_filenames = [
        '01_%s_lb(a10)_*.png',
        '02_%s_fw_1_*.png',
        '03_%s_total_1_*.png',
        '04_%s_host_1_*.png',
        '05_%s_vm_1_*.png',
        '06_%s_database_1_*.png',
        '07_%s_mongo_*.png',
        '08_%s_netapp_info_*.png',
        '09_%s_storage_1_*.png',
        '10_%s_cluster_info_1_*.png',
        '11_%s_cluster_info_2_*.png',
        '12_%s_cluster_info_3_*.png',
        '13_%s_cluster_info_4_*.png'
    ]
  
    elif region == 'SG':
        common_filenames = [
        '01_%s_lb(f5)_*.png',
        '02_%s_fw_1_*.png',
        '03_%s_total_1_*.png',
        '04_%s_host_1_*.png',
        '05_%s_vm_1_*.png',
        '06_%s_database_*.png',
        '07_%s_mongo_*.png',
        '08_%s_storage_1_*.png',
        '09_%s_storage_2_*.png',
        '10_%s_netapp_info_*.png',
        '11_%s_cluster_info_1_*.png',
        '12_%s_cluster_info_2_*.png',
        '13_%s_cluster_info_3_*.png',
        '14_%s_cluster_info_4_*.png',
        '15_%s_cluster_info_5_*.png',
    ]
    
    elif region == 'CN':
        common_filenames = [
        "01_%s_lb(a10)_*.png",
        "02_%s_fw_1_*.png",
        "03_%s_total_1_*.png",
        "04_%s_host_1_*.png",
        "05_%s_vm_1_*.png",
        "06_%s_database_1_*.png",
        "07_%s_mongo_*.png",
        "08_%s_netapp_info_*.png",
        "09_%s_storage_1_*.png",
        "10_%s_u_cluster_1_*.png",
        "11_%s_u_cluster_2_*.png",
        "12_%s_u_cluster_3_*.png",
        "13_%s_u_cluster_4_*.png",
        "14_%s_u_cluster_5_*.png",
        "15_%s_u_cluster_6_*.png",
        "16_%s_u_cluster_7_*.png",
        "17_%s_u_cluster_8_*.png",
        "18_%s_u_cluster_9_*.png",
]
    
    elif region == 'NA':
        common_filenames = [
        "01_%s_lb(a10)_*.png",
        "02_%s_fw_1_*.png",
		"03_%s_total_1_*.png",
        "04_%s_host_1_*.png",
        "05_%s_vm_1_*.png",
        "06_%s_database_1_*.png",
        "07_%s_mongo_*.png",
        "08_%s_netapp_info_*.png",
        "09_%s_storage_1_*.png",
        "10_%s_storage_2_*.png",
		"11_%s_cluster_info_1_*.png",
        "12_%s_cluster_info_2_*.png",
        "13_%s_cluster_info_3_*.png",
        "14_%s_cluster_info_4_*.png",
        "15_%s_cluster_info_5_*.png",
]

    elif region == 'RU':
        common_filenames = [
        "01_%s_lb(a10)_*.png",
        "02_%s_fw_1_*.png",
        "03_%s_total_1_*.png",
        "04_%s_host_1_*.png",
        "05_%s_vm_1_*.png",
        "06_%s_database_1_*.png",
        "07_%s_netapp_info_*.png",
        "08_%s_storage_1_*.png",
    
]
    
    elif region == 'Jennifer':
        common_filenames = [
        "%s_TMS_MAIN_*.png",
        "%s_TMS_Gen1_*.png",
        "%s_TMS_Gen2_*.png",
        "%s_TMS_ETC_*.png",
        "%s_TMS_SBS_VOICE_*.png",   
]



       
    try:
        filelist_delete = []
        
        for filename_pattern in common_filenames:
            filenames = glob.glob(os.path.join('ScreenShots', filename_pattern % region))
            print(filenames)
            
            if not filenames:  # 파일을 찾지 못한 경우
                print("No image files found for pattern:", filename_pattern % region)
                return  # 함수 종료
            else:
                filelist_delete.append(filenames[-3])
        
        print(filelist_delete)

        for filelist in filelist_delete:
            if not filelist:
                continue
            try:
                print("Deleting file:", filelist)
                os.remove(filelist)
                print("File deleted!!!")
    
            except Exception as e:
                print("Error deleting file:", filelist)
                print(e)
            
    except Exception as e:
                    print(e)
                    print('삭제할파일이 없습니다.')

    filelist_recently = []

    for filename_pattern in common_filenames:
            filenames = glob.glob(os.path.join('ScreenShots', filename_pattern % region))
            
            if not filenames:  # 파일을 찾지 못한 경우
                print("No image files found for pattern:", filename_pattern % region)
                return  # 함수 종료
            else:
                filelist_recently.append(filenames[-1])

       

    pdf = PdfFileWriter()

    inch = 72
                    
    for i, file in enumerate(filelist_recently):  # for each slide
                        # Using ReportLab Canvas to insert image into PDF
                  
                        imgTemp = BytesIO()
                        imgDoc = canvas.Canvas(imgTemp, pagesize=(11*inch, 8.5*inch))
                        fontname = 'C:\\Users\\H2207039\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NanumBarunGothic.ttf'
                        pdfmetrics.registerFont(TTFont("NanumBarunGothic", fontname))

                        # Draw image on Canvas and save PDF in buffer
                        print(file)
                        Words = file.split(".")[0].split("\\")

                        Title = Words[1]
                        imgDoc.setFont('NanumBarunGothic', 14)
                        imgDoc.drawString(20, 580, Title)
                        imgDoc.setFont('NanumBarunGothic', 12)
                        imgDoc.drawString(20, 560, sentence_h1[i])
                        imgDoc.drawString(20, 540, sentence_h2[i])
                        imgDoc.drawString(20, 520, sentence_h3[i])
                        imgDoc.drawImage(file, 0, 0, width=780, height=590, preserveAspectRatio=True, mask='auto')
                        # x, y - start position
                        # in my case -25, -45 needed
                        imgDoc.save()
                        # Use PyPDF to merge the image-PDF into the template
                        pdf.addPage(PdfFileReader(BytesIO(imgTemp.getvalue())).getPage(0))
                    
    
    filename = region+'Infra_in_detail' + datetime.now().strftime('%Y%m%d_%H%M') + '.pdf'
    filename = os.path.join(pdf_path, filename)
    pdf.write(open(filename,"wb"))

    print("--리포트저장성공--")