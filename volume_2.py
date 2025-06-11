from x_config import *
import time
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
from keystoneclient.v3 import client as keystone_client
from lb_5 import *
from datetime import datetime, timedelta

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

def extract_cinder_data(session, project_map, server_map):
    cinder = cinder_client.Client('3', session=session)
    volumes = cinder.volumes.list(search_opts={'all_tenants': 1})

    header = ["project_name", "tenant", "id", "name", "size", "status", "volume_type", "created_at", "availability_zone", "attached_to"]
    data = []

    for v in volumes:
        volume_type = v.volume_type or ""
        tenant = "PRD" if "prd" in volume_type.lower() else "STG" if "stg" in volume_type.lower() else ""

        # 프로젝트 ID 가져오기 (안전하게)
        project_id = getattr(v, 'project_id', None) or getattr(v, 'os-vol-tenant-attr:tenant_id', None)
        project_name = project_map.get(project_id, project_id or "UNKNOWN")

        # 연결된 인스턴스 이름 (server_map 이용)
        attached_names = []
        for a in v.attachments:
            server_id = a.get("server_id", "")
            if server_id:
                attached_names.append(server_map.get(server_id, server_id))
        attached_to = ",".join(attached_names)

        row = [
            project_name,
            tenant,
            v.id,
            v.name,
            v.size,
            v.status,
            volume_type,
            v.created_at,
            v.availability_zone,
            attached_to
        ]
        data.append(row)

    return ("Cinder_Volumes", header, data)

def extract_manila_data(session, project_map):
    manila = manila_client.Client('2', session=session)
    shares = manila.shares.list(search_opts={'all_tenants': 1})

    header = ["project_name", "tenant", "id", "name", "size", "status", "volume_type", "created_at", "share_proto", "export_location"]
    data = []

    for s in shares:
        volume_type = s.volume_type or ""
        tenant = "PRD" if "prd" in volume_type.lower() else "STG" if "stg" in volume_type.lower() else ""
        # 프로젝트 ID 가져오기 (안전하게)
        project_id = getattr(s, 'project_id', None) or getattr(s, 'os-vol-tenant-attr:tenant_id', None)
        project_name = project_map.get(project_id, project_id or "UNKNOWN")

        row = [
            project_name,
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
    project_map = get_project_map(sess)
    server_map = get_server_map(sess)
    cinder_sheet = extract_cinder_data(sess, project_map, server_map)
    manila_sheet = extract_manila_data(sess, project_map)

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

def get_project_map(session):
    keystone = keystone_client.Client(session=session)
    projects = keystone.projects.list()
    return {p.id: p.name for p in projects}

def get_server_map(session):
    nova = client.Client('2.1', session=session)
    servers = nova.servers.list(search_opts={'all_tenants': 1})
    return {s.id: s.name for s in servers}

nova_extract(VPN_FR2_NAME)