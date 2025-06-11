from sqlalchemy import create_engine, Column, Integer, String, DateTime, CheckConstraint, text, Boolean
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import pandas as pd
import configparser
import models
from database import Base

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from vm_lb_1 import add_document_vm

# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.triggers.cron import CronTrigger
import time

# Base = declarative_base()

import odf.opendocument
import odf.table
import odf.text

def read_ods_table(file_path, sheet_index=0):
    from odf.opendocument import load
    from odf.table import Table, TableRow, TableCell
    from odf.text import P

    doc = load(file_path)
    sheets = doc.spreadsheet.getElementsByType(Table)
    sheet = sheets[sheet_index]
    data = []

    for row in sheet.getElementsByType(TableRow):
        row_data = []
        for cell in row.getElementsByType(TableCell):
            text_content = ''
            for p in cell.getElementsByType(P):
                text_content += str(p)
            # Remove <text:p> and </text:p> tags
            text_content = text_content.replace('<text:p>', '').replace('</text:p>', '')
            row_data.append(text_content.strip())
        data.append(row_data)

    # 첫 번째 행을 컬럼명으로 사용
    df = pd.DataFrame(data[1:], columns=data[0])
    return df

# Function to read configuration settings from an INI file
def read_config(ini_file_path, section_name):
    config = configparser.ConfigParser()
    config.read(ini_file_path)
    section = config[section_name]
    return section

def create_table(config):
    DATABASE_USER = config.get('DATABASE_USER')
    DATABASE_PASSWORD = config.get('DATABASE_PASSWORD')
    DATABASE_HOST = config.get('DATABASE_HOST')
    DATABASE_PORT = config.get('DATABASE_PORT')
    DATABASE_NAME = config.get('DATABASE_NAME')

    DATABASE_URL = f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

    engine = create_engine(DATABASE_URL, pool_size=100, max_overflow=200)
    Session = sessionmaker(bind=engine)

    # Create the table in the database
    Base.metadata.create_all(engine)

    return engine  # Return the engine


def table_exists(engine, table_name):
    # Check if the table exists in the database
    query = f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table_name}');"
    result = pd.read_sql_query(query, engine)
    table_exists = result.iloc[0, 0]

    if not table_exists:
        print(f"Table '{table_name}' does not exist.")
        return False

    # Check if the table has more than one record
    query = f"SELECT COUNT(*) FROM {table_name};"
    result = pd.read_sql_query(query, engine)
    record_count = result.iloc[0, 0]

    if record_count < 1:
        print(f"Table '{table_name}' has less than one record.")
        return False

    return True

def exists_for_today(table_name, engine):
    # 날짜 처리
    current_date = datetime.now()
    year, month, day = current_date.strftime('%Y'), current_date.strftime('%m'), current_date.strftime('%d')

    query = text(f"""
        SELECT 1 FROM {table_name}
        WHERE year = :year AND month = :month AND day = :day
        LIMIT 1
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {"year": year, "month": month, "day": day})
        return result.scalar() is not None

def update_agg_instances(engine, data):
    """Update the agg_instances table based on the provided data."""
    # Get the current date
    current_date = datetime.now()
    year = current_date.strftime('%Y')
    month = current_date.strftime('%m')
    day = current_date.strftime('%d')

    # Aggregate the data
    agg_data = data.groupby(['project_id']).size().reset_index(name='count')
    agg_data['year'] = year
    agg_data['month'] = month
    agg_data['day'] = day
    agg_data['created_at'] = current_date
    agg_data['updated_at'] = current_date

    # agg_instances 테이블 처리
    if not agg_data.empty:
        if exists_for_today("agg_instances", engine):
            print(f"[SKIPPED] Records for {year}-{month}-{day} already exist in 'agg_instances'.")
        else:
            agg_data.to_sql('agg_instances', engine, if_exists='append', index=False)
            print(f"[OK] {len(agg_data)} agg instances appended.")

# Function to connect to the database and ingest data
def ingest_data(engine, ods_file_path):

    table_name = 'instances'
#    if table_exists(engine, table_name):
#        print(f"Table '{table_name}' already exists. Skipping initial data insertion.")
#        return

    # Load data into a pandas DataFrame
    data = read_ods_table(ods_file_path)
    # print(data.columns)

    # Rearrange columns to match the schema
    data.drop(columns=['cpu', 'memory'], inplace=True, errors='ignore')
    data.rename(columns={'created_at': 'vm_created_at', 'updated_at': 'vm_updated_at','id': 'instance_id', 'name': 'instance_name'}, inplace=True)
    #data = data[['id', 'customer', 'region', 'az', 'tenant', 'instance_id', 'instance_name', 'status', 'address', 'flavor', 'availability_zone', 'hostname', 'vm_created_at', 'vm_updated_at']]

    # print("========================================")
    # print(data[data['region'].isnull()])

#     # Add missing columns with default values
#     default_values = {
#         # 'customer': 'CCS',
#         # 'region': 'KR',
#         # 'az': '1',
#         # 'tenant': 'prd',
#         # 'is_draft': False,
#         # 'is_use': True,
#         'created_at': datetime.now(),
#         'updated_at': datetime.now(),
#         # 'creator': 'admin',
#         # 'updater': 'admin'
# #       'base_deleted_at': None
#     }

#     for column_name in default_values:
#         if column_name not in data.columns:
#             data[column_name] = default_values[column_name]
    data.fillna({'availability_zone':'empty'}, inplace=True)
    data.fillna({'hostname':'empty'}, inplace=True)
    data.fillna({'address':'empty'}, inplace=True)
    # data.['availability_zone'].fillna(value='empty', inplace=True)
    # data['hostname'].fillna(value='empty', inplace=True)
    # data['address'].fillna(value='empty', inplace=True)

    with engine.begin() as connection:  # autocommit 포함
        connection.execute(text('TRUNCATE TABLE instances RESTART IDENTITY;'))
    print("1. truncate success!!")

    # After preparing data_to_append, update agg_instances
    print("2. update agg instances!!")
    update_agg_instances(engine, data)
    print(data.columns)

    # Write the filtered DataFrame to the PostgreSQL table
    data.to_sql('instances', engine, if_exists='append', index=False)
    print("3. add raw datas of instances!!")

def append_data(engine, *ods_file_path):
    _, df_added, df_deleted = add_document_vm()

    if df_added.empty and df_deleted.empty:
        print("No data to append for both added and deleted instances.")
        return

    # 날짜 처리
    current_date = datetime.now()
    year, month, day = current_date.strftime('%Y'), current_date.strftime('%m'), current_date.strftime('%d')

    # 날짜 컬럼 추가
    for df in [df_added, df_deleted]:
        df['year'] = year
        df['month'] = month
        df['day'] = day

    # 컬럼명 변경
    rename_map = {
        'id': 'instance_id',
        'name': 'instance_name',
        'created_at': 'vm_created_at',
        'updated_at': 'vm_updated_at'
    }
    df_added.rename(columns=rename_map, inplace=True)
    df_deleted.rename(columns=rename_map, inplace=True)

    # 필요한 컬럼만 필터링
    common_columns = ['instance_id', 'project_id', 'instance_name', 'status', 'flavor',
                      'address', 'availability_zone', 'hostname', 'vm_created_at', 'vm_updated_at',
                      'year', 'month', 'day']
    data_added = df_added[common_columns]
    data_deleted = df_deleted[common_columns]

    # 기본값 채우기
    for df in [data_added, data_deleted]:
        df.fillna({'availability_zone':'empty'}, inplace=True)

    # added_instances 테이블 처리
    if not data_added.empty:
        if exists_for_today("added_instances", engine):
            print(f"[SKIPPED] Records for {year}-{month}-{day} already exist in 'added_instances'.")
        else:
            data_added.to_sql('added_instances', engine, if_exists='append', index=False)
            print(f"[OK] {len(data_added)} added instances appended.")

    # deleted_instances 테이블 처리
    if not data_deleted.empty:
        if exists_for_today("deleted_instances", engine):
            print(f"[SKIPPED] Records for {year}-{month}-{day} already exist in 'deleted_instances'.")
        else:
            data_deleted.to_sql('deleted_instances', engine, if_exists='append', index=False)
            print(f"[OK] {len(data_deleted)} deleted instances appended.")

# ============================================================================================================

def update_data(engine, *ods_file_path):
    # Check if the table exists
    table_name = 'instances'

    if not table_exists(engine, table_name):
        print(f"Table '{table_name}' does not exist. Skipping data update.")
        return

    # Load data into a pandas DataFrame
    data_to_update = pd.read_csv(ods_file_path)

    data_to_update.rename(columns={'created_at': 'vm_created_at', 'updated_at': 'vm_updated_at'}, inplace=True)

    row_update_count = 0

    if data_to_update.empty:
        print("No data to update.")
        return

    # Iterate through the DataFrame and update only rows with changes
    with engine.begin() as conn:
        for index, row in data_to_update.iterrows():
            id_value = row['id']
            updated_at_value = row['vm_updated_at']

            # Check if the row exists in the database
            query = text("SELECT id FROM instances WHERE id = :id_value")
            result = conn.execute(query.bindparams(id_value=id_value))
            existing_id = result.fetchone()

            if existing_id:
                # Check if the 'updated_at' value has changed
                query = text("SELECT vm_updated_at FROM instances WHERE id = :id_value")
                result = conn.execute(query.bindparams(id_value=id_value))
                current_updated_at = result.fetchone()[0]

                current_updated_at = datetime.strftime(current_updated_at, '%Y-%m-%dT%H:%M:%SZ')

                # current_updated_at is in DB now, updated_at_value is in CSV
                if current_updated_at!= updated_at_value:
                    update_query = text(
                        "UPDATE instances "
                        "SET name = :name, "
                        "status = :status, "
                        "flavor = :flavor, "
                        "address = :address, "
                        "availability_zone = :availability_zone, "
                        "hostname = :hostname, "
                        "vm_updated_at = :vm_updated_at, "
                        "base_updated_at = now() "
                        "WHERE id = :id"
                    )
                    conn.execute(
                        update_query.bindparams(
                            name=row['name'],
                            status=row['status'],
                            flavor=row['flavor'],
                            address=row['address'],
                            availability_zone=row['availability_zone'],
                            hostname=row['hostname'],
                            vm_updated_at=row['vm_updated_at'],
                            id=row['id']
                        )
                    )
                    row_update_count +=1

                    print(f"Row with ID {id_value} updated.")
                else:
                    #print(f"Row with ID {id_value} has no changed")
                    pass
            else:
                print(f"Row with ID {id_value} does not exist in the database")

    print("Update process completed")
    print(f"{row_update_count} row updated.")

def mark_records_for_deletion(engine, *ods_file_path):
    # Check if the table exists
    table_name = 'instances'
    if not table_exists(engine, table_name):
        print(f"Table '{table_name}' does not exist. Skipping data update.")
        return

    # Load data from the CSV file
    data_to_be_deleted = pd.read_csv(ods_file_path)

    rows_marked_for_deletion = 0

    # Iterate through the CSV data and update each row individually
    with engine.begin() as conn:
        for index, row in data_to_be_deleted.iterrows():
            id_value = row['id']

            query = text("SELECT id FROM instances WHERE id = :id_value AND is_use = true")
            result = conn.execute(query.bindparams(id_value=id_value))
            existing_id = result.fetchone()

            if existing_id:
                update_query = text("UPDATE instances SET is_use = false WHERE id = :id_value")
                conn.execute(update_query.bindparams(id_value=id_value))
                rows_marked_for_deletion += 1

    print(f"{rows_marked_for_deletion} records marked for deletion.")


#def scheduled_tasks(engine, initial_ods_file_path, after_ods_file_path, deletion_ods_file_path):
#def scheduled_tasks(engine, initial_ods_file_path, after_ods_file_path):
#    ingest_data(engine, initial_ods_file_path)
#    append_data(engine, after_ods_file_path)
    #time.sleep(60)
#    update_data(engine, after_ods_file_path)
#   mark_records_for_deletion(engine, deletion_ods_file_path)

def main():
    ini_file_path = 'C:\\Beomjun\\db\\env.ini'
    section_name = 'common'
    config = read_config(ini_file_path, section_name)

    engine = create_table(config)
#    create_table(config)
    current_date = datetime.now().strftime("%Y%m%d")
#    after_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
#    print(after_date)

#    initial_ods_file_path = './vm/VMlist_eu_1_prd_{}.csv'.format(current_date)
#    initial_ods_file_path = 'inventory_{}.csv'.format(current_date)
#    initial_ods_file_path = '/home/centos/inventory/vm/VM_inventory_{}.csv'.format(current_date)

    ods_file_path = f'C:\\Beomjun\\csv\\VM\\vm_info_{current_date}.ods'
    
    # ods_file_path = f'C:\\Beomjun\\csv\\VM\\vm_info_20250603.ods'
    print(ods_file_path)
#    append_data(engine, ods_file_path)
#    update_data(engine, ods_file_path)
#    mark_records_for_deletion(engine, ods_file_path)

    ingest_data(engine, ods_file_path)
    append_data(engine)


if __name__ == "__main__":
    main()
