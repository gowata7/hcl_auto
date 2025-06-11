import re
import time
from datetime import datetime, timedelta
from novaclient import client
import pandas as pd
from novaclient import client
from keystoneauth1 import session
from keystoneauth1.identity import v3
from odf.opendocument import OpenDocumentSpreadsheet
from odf.table import Table, TableRow, TableCell
from odf.text import P
from keystoneclient.v3 import client as keystone_client

import psycopg2
from psycopg2.extras import RealDictCursor

current_date = datetime.now().strftime("%Y%m%d")

def create_ods_file(file_path, header, data_rows):
    print(" ODS 파일 생성 시작...")

    # Windows 경로 맞춤 설정
    file_path = file_path.replace("/", "\\")

    #  만약 동일한 파일이 있으면 삭제
    if os.path.exists(file_path):
        os.remove(file_path)

    #  ODS Document 생성
    doc = OpenDocumentSpreadsheet()
    table = Table(name="VM_Data")

    #  Header 추가
    print(f"📝 Header 추가 중: {header}")
    header_row = TableRow()
    for column_name in header:
        cell = TableCell()
        # 👉 value-type을 string으로 명시
        cell.setAttribute("valuetype", "string")
        cell.addElement(P(text=str(column_name)))
        header_row.addElement(cell)
    table.addElement(header_row)

    #  Data 추가
    print(f"📝 총 {len(data_rows)}개의 데이터가 추가됩니다.")
    for idx, row in enumerate(data_rows):
        # print(f"➡️ [{idx+1}/{len(data_rows)}] {row}")
        row_element = TableRow()
        for cell_data in row:
            if cell_data is None:
                cell_data = ""
            cell = TableCell()
            cell.setAttribute("valuetype", "string")
            cell.addElement(P(text=str(cell_data)))
            row_element.addElement(cell)
        table.addElement(row_element)

    # Table을 Spreadsheet에 추가
    print(f"💾 Spreadsheet에 Table 추가")
    doc.spreadsheet.addElement(table)

    #  파일 직접 쓰기
    print(f"💾 ODS 파일 쓰기 시작... {file_path}")
    try:
        with open(file_path, "wb") as f:
            doc.write(f)      # 명시적으로 write 수행
            f.flush()         # 버퍼에 남아있는 내용 비우기
        print(f"✅ ODS 파일 생성 완료: {file_path}")
    except Exception as e:
        print(f"❌ 파일 저장 실패: {e}")

# 파일명 생성 함수
def get_file_and_topic_names(current_date):
    file_name = f'C:\\Beomjun\\csv\\VM\\vm_info_{current_date}.ods'
    return file_name

def nova_extract(project_name, vpn_name):

    if is_vpn_connected(vpn_name):
        print(f"[INFO] VPN {vpn_name} is already connected.")
    else:
        print(f"[INFO] VPN {vpn_name} not connected. Attempting connection...")
        connect_vpn(vpn_name, USERNAME, PASSWORD)

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

    # 모든 프로젝트 VM 가져오기
    vms = nova.servers.list(search_opts={'all_tenants': 1})

    # 프로젝트 리스트
    keystone = keystone_client.Client(session=sess)
    projects = keystone.projects.list()
    project_map = {p.id: p.name for p in projects}  # id → name 맵 생성
    
    ods_file_path = get_file_and_topic_names(current_date)
    print("ODS 파일명:", ods_file_path)
    
    ods_header = [ "id", "project_id", "name", "status", "cpu", "memory", "flavor", "address", "availability_zone", "hostname", "created_at", "updated_at"]
    data_rows = []

    for vm in vms:
        project_name = project_map.get(vm._info.get('tenant_id'), "unknown")
        
        # 주소 정보 구성
        addresses_info = ""
        for key, values in vm.addresses.items():
            for addr_info in values:
                addresses_info += f'{key}:{addr_info["addr"]}\n'
        addresses_info = addresses_info.strip()

        # Flavor 정보
        try:
            flavor_id = vm.flavor['id']
            flavor = nova.flavors.get(flavor_id)
            flavor_name = flavor.name
        except Exception as e:
            flavor_name = ""

        # CPU와 메모리 추출
        cpu_match = re.search(r'(\d+)vCPU', flavor_name)
        mem_match = re.search(r'RAM(\d+)GB', flavor_name)
        cpu = int(cpu_match.group(1)) if cpu_match else None
        memory = int(mem_match.group(1)) if mem_match else None

        # AZ 값 보정
        az = vm._info.get('OS-EXT-AZ:availability_zone')
        if not az or az.lower() == "none":
            if "prd" in addresses_info.lower():
                az = "PRD"
            elif "stg" in addresses_info.lower():
                az = "STG"
            else:
                az = "unknown"

        vm_data = [
            vm.id, project_name, vm.name, vm.status, cpu, memory,
            flavor_name, addresses_info, az,
            vm._info.get('OS-EXT-SRV-ATTR:host', ''),
            vm.created, vm.updated
        ]
        data_rows.append(vm_data)
        # print("data!", vm_data)

    # ODS 파일 생성
    create_ods_file(ods_file_path, ods_header, data_rows)
    return ods_file_path

# 오래된 파일 정리
def cleanup(tenants):
    time.sleep(1)
    
    retention_period = 5
    delete_date = (datetime.now() - timedelta(days=retention_period)).strftime("%Y%m%d")
    host_dir = 'C://Beomjun//csv//'
    file_list = os.listdir(host_dir)

    for tenant in tenants:
        for file_name in file_list:
            if file_name.startswith(f'vm_eu2_{tenant}_') and file_name <= f'vm_eu2_{tenant}_{delete_date}.ods':
                file_path = os.path.join(host_dir, file_name)
                os.remove(file_path)
                print("file remove success!")

def add_document_vm():
    from datetime import datetime, timedelta
    # 날짜 설정
    yesterday_date = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")

    print("today:", current_date)
    print("yesterday:", yesterday_date)

    # 경로 설정
    today_path = f"C:\\Beomjun\\csv\\VM\\vm_info_{current_date}.ods"
    yesterday_path = f"C:\\Beomjun\\csv\\VM\\vm_info_{yesterday_date}.ods"

    # file_path=os.path.abspath("")
    # srcpath = findfile(f"eu_adminrc_{yesterday_date}.csv.org", file_path)
    # dir, file = os.path.split(srcpath)
    # shutil.copy2(srcpath, dir+f"\eu_adminrc_{yesterday_date}.csv")
        
    # CSV 로드
    df_today = pd.read_excel(today_path, engine='odf')
    df_yesterday = pd.read_excel(yesterday_path, engine='odf')

    # ID 기준으로 차집합 연산
    today_ids = set(df_today['id'])
    yesterday_ids = set(df_yesterday['id'])

    # 추가된 VM: 오늘에는 있고 어제는 없던 것
    added_ids = today_ids - yesterday_ids
    df_added = df_today[df_today['id'].isin(added_ids)]

    # 삭제된 VM: 어제는 있었는데 오늘은 없는 것
    deleted_ids = yesterday_ids - today_ids
    df_deleted = df_yesterday[df_yesterday['id'].isin(deleted_ids)]

    # 결과 출력
    print("\n✅ 오늘 추가된 VM:")
    print(df_added)

    print("\n❌ 오늘 삭제된 VM:")
    print(df_deleted)

    # for style in document.styles:
    #     print(style.name)
    
    return df_today, df_added, df_deleted

def get_this_week_range():
    from datetime import datetime, timedelta
    today = datetime.now().date()
    weekday = today.weekday()  # 0=월, 1=화, ..., 6=일

    # 전주 동일 요일부터 오늘까지
    start_date = today - timedelta(days=7)
    end_date = today

    return start_date, end_date

def fetch_weekly_added_vms():
    start_date, end_date = get_this_week_range()
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT 
                project_id, instance_name, flavor, address, availability_zone, hostname,
                make_date(year::int, month::int, day::int) AS date
            FROM added_instances
            WHERE make_date(year::int, month::int, day::int) BETWEEN %s AND %s
            ORDER BY date;
        """, (start_date, end_date))
        rows = cur.fetchall()
    conn.close()
    return rows

def fetch_weekly_deleted_vms():
    start_date, end_date = get_this_week_range()
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT 
                project_id, instance_name, flavor, address, availability_zone, hostname,
                make_date(year::int, month::int, day::int) AS date
            FROM deleted_instances
            WHERE make_date(year::int, month::int, day::int) BETWEEN %s AND %s
            ORDER BY date;
        """, (start_date, end_date))
        rows = cur.fetchall()
    conn.close()
    return rows

def add_document_table():
    
    df_today, df_added, df_deleted = add_document_vm()

    document.add_heading('VM 현황', level=1) 
    total = len(df_today)

    document.add_paragraph(f'총 {total}건', style='List Bullet')

    # Pivoting
    df = preprocess_df(df_today)
    # pivot, total = getPivotTable(df, month)

    # Chart - Pie 차트
    region_pivot, _ = getPivotTable_new(df, 'Region')
    tenant_pivot, _ = getPivotTable_new(df, 'Tenant')

    source1 = region_pivot
    source2 = tenant_pivot

    print(source1)
    print(source2)

    # Chart
    # if incompleted == 0:
    chart1 = getPieChart_region(source1)
    chart2 = getPieChart_tenant(source2)
    # else:
    #     source = flatten_2d(data)
    #     chart = getStackedHBarChart(source)    

    # source = pivot
    # if incompleted == 0:
    #     chart = getPieChart(source)
    # else:
    #     chart = getStackedHBarChart1(source)
    chart1.save(f'./charts/vm_1.png')
    chart2.save(f'./charts/vm_2.png')

    table = document.add_table(rows=1, cols=2)

    # ----------- 좌측 셀 (리전별) ------------
    cell = table.rows[0].cells[0]
    paragraph = cell.paragraphs[0]
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER  # 수평 중앙 정렬
    run = paragraph.add_run("리전별")
    run.font.size = Pt(12)  # 폰트 크기 조절 (선택)
    run.bold = True  # 굵게 (선택)

    # 이미지 추가 (별도 문단 생성하여 아래로 정렬되게)
    paragraph_img = cell.add_paragraph()
    paragraph_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_img = paragraph_img.add_run()
    run_img.add_picture('./charts/vm_1.png', width=Inches(3.3))

    # ----------- 우측 셀 (테넌트별) ------------
    cell = table.rows[0].cells[1]
    paragraph = cell.paragraphs[0]
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run("테넌트별")
    run.font.size = Pt(12)
    run.bold = True

    paragraph_img = cell.add_paragraph()
    paragraph_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_img = paragraph_img.add_run()
    run_img.add_picture('./charts/vm_2.png', width=Inches(3.3))

    # Document
    document.add_paragraph(f'전일 대비 추가된 VM({len(df_added)}건)', style='List Bullet')
    # A-B (삭제된 건)
    # df_result_sub = pd.concat([df_premonth,df_curmonth,df_curmonth]).drop_duplicates(keep=False)
    # print(df_result_sub)

    if len(df_added) == 0:
        pass
    else:
        addTable3(df_added)
        
    p = document.add_paragraph('')
    run = p.add_run()
    run.add_break(WD_BREAK.LINE)

    document.add_paragraph(f'전일 대비 삭제된 VM({len(df_deleted)}건)', style='List Bullet')
    # A-B (삭제된 건)
    # df_result_sub = pd.concat([df_premonth,df_curmonth,df_curmonth]).drop_duplicates(keep=False)
    # print(df_result_sub)

    if len(df_deleted) == 0:
        pass
    else:
        addTable3(df_deleted)

    p = document.add_paragraph('')
    run = p.add_run()
    run.add_break(WD_BREAK.LINE)

    start_date, end_date = get_this_week_range()

    fetch_weekly_added_vms()
    weekly_vms_added = fetch_weekly_added_vms()
    df_weekly_added = pd.DataFrame(weekly_vms_added)
    print("weekly_vms_added:", df_weekly_added)
    document.add_paragraph(f'1주 간({start_date}~{end_date}) 생성된 VM 목록 ({len(df_weekly_added)}건)', style='List Bullet')
    
    if weekly_vms_added:
        addTable_instance(df_weekly_added)
    else:
        document.add_paragraph('1주 간 생성된 VM이 없습니다.')
    
    p = document.add_paragraph('')
    run = p.add_run()
    run.add_break(WD_BREAK.LINE)

    fetch_weekly_deleted_vms()
    weekly_vms_deleted = fetch_weekly_added_vms()
    df_weekly_deleted = pd.DataFrame(weekly_vms_deleted)
    print("weekly_vms_deleted:", df_weekly_deleted)
    document.add_paragraph(f'1주 간({start_date}~{end_date}) 삭제된 VM 목록 ({len(df_weekly_deleted)}건)', style='List Bullet')
    
    if weekly_vms_deleted:
        addTable_instance(df_weekly_deleted)
    else:
        document.add_paragraph('1주 간 삭제된 VM이 없습니다.')

    document.add_page_break()
    # document.save(f'C:\\Beomjun\\csv\\vm_report_{current_date}.docx')


if __name__ == "__main__":
    from datetime import datetime, timedelta
    from lb_5 import *
    from x_config import *

    project_names = ['admin']
    tenants = ['adminrc']

    # 각 프로젝트에 대해 함수 실행
    for project_name in project_names:
        print("This project is", project_name)
        ods_file_path = nova_extract(project_name, VPN_FR2_NAME)
    # cleanup(tenants)

    add_document_vm()
    add_document_table()

    ods_file = f"C:\\Beomjun\\csv\\LB\\lb_info_{current_date}.ods"

    print("[INFO] Starting collection for FR2")
    fr2_data = collect_lb_info("FR2", VPN_FR2_NAME, ip_list_fr2)

    print("[INFO] Starting collection for FR7")
    fr7_data = collect_lb_info("FR7", VPN_FR7_NAME, ip_list_fr7)

    # ✅ 데이터 병합
    combined_data = fr2_data + fr7_data
    columns = ["Tenant", "NS_IP", "LB_Name", "LB_VIP", "Port", "Service_Type"]
    df_combined = pd.DataFrame(combined_data, columns=columns)

    # # ✅ ODS 파일 저장
    with pd.ExcelWriter(ods_file, engine='odf') as writer:
        df_combined.to_excel(writer, sheet_name="LB_Info", index=False)

    df_added, df_deleted = compare_yesterday()
    add_document_lb(df_combined, df_added, df_deleted)
    
    print(f"\n✅ ODS 파일이 생성되었습니다: {ods_file}")
