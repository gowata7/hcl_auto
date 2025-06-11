from x_config import *
import time
from datetime import datetime, timedelta
from novaclient import client
import pandas as pd

import os
from keystoneauth1 import session
from keystoneauth1.identity import v3
from odf.opendocument import OpenDocumentSpreadsheet
from odf.table import Table, TableRow, TableCell
from odf.text import P
from cinderclient import client as cinder_client
from manilaclient import client as manila_client
from lb_5 import *

def create_ods_file(file_path, sheet_data_list):
    print("ODS 파일 생성 시작...")

    if os.path.exists(file_path):
        os.remove(file_path)

    doc = OpenDocumentSpreadsheet()

    for sheet_name, header, data_rows in sheet_data_list:
        print(f"📄 시트 생성: {sheet_name}")
        table = Table(name=sheet_name)

        # Header
        header_row = TableRow()
        for col in header:
            cell = TableCell(valuetype="string")
            cell.addElement(P(text=str(col)))
            header_row.addElement(cell)
        table.addElement(header_row)

        # Data rows
        for row in data_rows:
            row_element = TableRow()
            for item in row:
                cell = TableCell(valuetype="string")
                cell.addElement(P(text=str(item if item is not None else "")))
                row_element.addElement(cell)
            table.addElement(row_element)

        doc.spreadsheet.addElement(table)

    # Save file
    with open(file_path, "wb") as f:
        doc.write(f)
        f.flush()

    print(f"✅ ODS 저장 완료: {file_path}")

# 파일명 생성 함수
def get_file_and_topic_names(current_date):
    file_name = f'C:\\Beomjun\\csv\\Volume\\volume_info_{current_date}.ods'
    return file_name

def extract_cinder_data(session):
    cinder = cinder_client.Client('3', session=session)
    volumes = cinder.volumes.list(search_opts={'all_tenants': 1})

    header = ["tenant", "id", "name", "size", "status", "volume_type", "created_at", "availability_zone"]
    data = []

    for v in volumes:
        volume_type = v.volume_type or ""
        tenant = "PRD" if "prd" in volume_type.lower() else "STG" if "stg" in volume_type.lower() else ""

        row = [
            tenant,
            v.id,
            v.name,
            v.size,
            v.status,
            volume_type,
            v.created_at,
            v.availability_zone,
        ]
        data.append(row)

    return ("Cinder_Volumes", header, data)

def extract_manila_data(session):
    manila = manila_client.Client('2', session=session)
    shares = manila.shares.list(search_opts={'all_tenants': 1})

    header = ["tenant", "id", "name", "size", "status", "volume_type", "created_at", "share_proto", "export_location"]
    data = []

    for s in shares:
        volume_type = s.volume_type or ""
        tenant = "PRD" if "prd" in volume_type.lower() else "STG" if "stg" in volume_type.lower() else ""

        row = [
            tenant,
            s.id,
            s.name,
            s.size,
            s.status,
            s.volume_type,
            s.created_at,
            s.share_proto,
            s.export_location
        ]
        data.append(row)

    return ("Manila_Shares", header, data)


def nova_extract(vpn_name):
    if is_vpn_connected(vpn_name): 
        print(f"[INFO] VPN {vpn_name} is already connected.")
    else:
        print(f"[INFO] VPN {vpn_name} not connected. Attempting connection...")
        connect_vpn(vpn_name, USERNAME, PASSWORD)

    current_date = datetime.now().strftime("%Y%m%d")

    auth = v3.Password(
        auth_url='http://cloud-control-vip.eu-central.openstack.h53:5000/v3',
        username='admin',
        password='TldhTl1!',
        user_domain_name='Default',
        project_name='admin',
        project_domain_name='Default'
    )

    sess = session.Session(auth=auth)
    nova = client.Client('2.1', session=sess)

    ods_file_path = get_file_and_topic_names(current_date)
    print("ODS 파일명:", ods_file_path)

    # Cinder & Manila
    cinder_sheet = extract_cinder_data(sess)
    manila_sheet = extract_manila_data(sess)

    # #----------------------------------------------------
    # # 키값 확인 
    # cinder = cinder_client.Client('3', session=sess)
    # volumes = cinder.volumes.list(search_opts={'all_tenants': 1})
    # # 예: 첫 번째 볼륨의 모든 키 확인
    # if volumes:
    #     v = volumes[0]  # 리스트에서 첫 번째 볼륨 선택
    #     volume_dict = v.to_dict()
    
    #     print("🔍 Cinder Volume 모든 필드:")
    #     for key in volume_dict:
    #         print(f"{key}: {volume_dict[key]}")
    # else:
    #     print("❗ 볼륨이 없습니다.")

    # manila = manila_client.Client('2', session=sess)
    # shares = manila.shares.list(search_opts={'all_tenants': 1})
    # if shares:
    #     v = shares[0]  # 리스트에서 첫 번째 볼륨 선택
    #     share_dict = v.to_dict()
    
    #     print("🔍 share Volume 모든 필드:")
    #     for key in share_dict:
    #         print(f"{key}: {share_dict[key]}")
    # else:
    #     print("❗ 볼륨이 없습니다.")
    # #-----------------------------------------------------
    
    # 시트 데이터 리스트 구성
    sheets = [cinder_sheet, manila_sheet]
    create_ods_file(ods_file_path, sheets)

nova_extract(VPN_FR2_NAME)