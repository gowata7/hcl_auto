# %load table.py
import pandas as pd
from pandas import Series, DataFrame
# from pandas_ods_reader import read_ods
from datetime import datetime, date
from dateutil.relativedelta import relativedelta, MO
from collections import defaultdict

import datetime
import altair as alt
import pandas as pd
import re  

today = datetime.date.today()
y = today.year
# m = today.month
m = today + relativedelta(months=-1)
# ym은 str형이다.
ym = today.strftime('%Y%m')

def flatten_1d(input):
    new_list = []
    for i in input:
        for j in i:
            new_list.append(j)
    return new_list

def counter(df, regex):
    region_count = 0    
    regions = []
    
    for s in df['리전']:
        list = re.split(',|/|\|', s)
        regions.append(list)

    for s in flatten_1d(regions):
        for match in re.finditer(regex, s):
            region_count += 1    
            
    return region_count

def flatten_2d(data):
    regions = []
    regions_flatten = []
    regions_count = []  

    for s in data['리전']:
        list = re.split(',|/|\|', s)
        regions.append(list)

    region_list = []
    status_list = []
    for r, s in zip(regions, data['진행상태']):
        for item in r:
            region_list.append(item)
            status_list.append(s)          

    data = pd.DataFrame(zip(region_list, status_list))
    data.columns = ['리전', '진행상태']
    
    return data    

def flatten_3d(data):
    regions = []
    regions_flatten = []
    regions_count = []  

    for s in data['리전']:
        list = re.split(',|/|\|', s)
        regions.append(list)

    region_list = []
    status_list = []
    month_list = []
    
    for r, m, s in zip(regions, data['월'], data['진행상태']):
        print('r,m,s : ', r,m,s)
        for item in r:
            print('item : ', item)
            region_list.append(item)
            status_list.append(s)
            month_list.append(m)

    data = pd.DataFrame(zip(region_list, month_list, status_list))
    data.columns = ['월', '합계']
    
    return data    

def counter_3d_vm(df_filtered, ym2):
    
    group_df = df_filtered.groupby(['년','월'])['count'].sum().reset_index()
    print(group_df)
    
    group_df['Date'] = pd.to_datetime(group_df['년'].astype(str) + group_df['월'].astype(str), format='%Y%m').dt.strftime('%Y%m')
    print(group_df)
    # created_group = group_df.groupby(['Date','count'])
    created_group = group_df.loc[:,['Date', 'count']]
    print(created_group, type(created_group))

    df_extract = created_group.loc[:,['Date']]
    print("df_extract", df_extract)

    df_index = df_extract['Date'].tolist()
    print("df_index",df_index)
    print(ym2)
    ym_index = df_index.index(ym2)
    print("ym_index",ym_index)

    # for i in df_index[ym_index:ym_index-12:-1]:
    created_group = created_group[(created_group['Date'] >= df_index[ym_index-12]) & (created_group['Date'] <= df_index[ym_index])]
    # data = counter_3d_test(created_group,ym)
    
    return created_group 

def counter_3d_db(df_filtered, ym2):
    
    # group_df = df_filtered.groupby(['년','월'])['count'].sum().reset_index()
    # print(group_df)
    # chart = getLineChart_new(data)
    df_filtered['Date'] = pd.to_datetime(df_filtered['년'].astype(str) + df_filtered['월'].astype(str), format='%Y%m').dt.strftime('%Y%m')
    print(df_filtered)
    # created_group = group_df.groupby(['Date','count'])
    created_group = df_filtered.loc[:,['Date', '유형', 'count']]
    print(created_group, type(created_group))

    df_extract = created_group.loc[:,['Date']]
    print("df_extract", df_extract)

    df_index = sorted(list(set(df_extract['Date'].tolist())))
    print("df_index",df_index)
    print(ym2)
    ym_index = df_index.index(ym2)
    print("ym_index",ym_index)

    # for i in df_index[ym_index:ym_index-12:-1]:
    created_group = created_group[(created_group['Date'] >= df_index[ym_index-12]) & (created_group['Date'] <= df_index[ym_index])]
    # data = counter_3d_test(created_group,ym)
    
    return created_group 

def counter_3d_regular(df_filtered, ym2):
    
    df_filtered['Date'] = pd.to_datetime(df_filtered['년'].astype(str) + df_filtered['월'].astype(str), format='%Y%m').dt.strftime('%Y%m')
    print(df_filtered)
    # created_group = group_df.groupby(['Date','count'])
    created_group = df_filtered.loc[:,['Date', '진행상태']]
    print(created_group, type(created_group))

    df_extract = created_group.loc[:,['Date']]
    print("df_extract", df_extract)

    df_index = sorted(list(set(df_extract['Date'].tolist())))
    print("df_index",df_index)
    print(ym2)
    ym_index = df_index.index(ym2)
    print("ym_index",ym_index)

    # for i in df_index[ym_index:ym_index-12:-1]:
    created_group = created_group[(created_group['Date'] >= df_index[ym_index-12]) & (created_group['Date'] <= df_index[ym_index])]
    # data = counter_3d_test(created_group,ym)
    
    return created_group 

def counter_3d_license(df_filtered, ym2):
    
    df_filtered['Date'] = pd.to_datetime(df_filtered['년'].astype(str) + df_filtered['월'].astype(str), format='%Y%m').dt.strftime('%Y%m')
    print(df_filtered)
    # created_group = group_df.groupby(['Date','count'])
    created_group = df_filtered.loc[:,['Date', '유형', '공급사']]
    print(created_group, type(created_group))

    df_extract = created_group.loc[:,['Date']]
    print("df_extract", df_extract)

    df_index = sorted(list(set(df_extract['Date'].tolist())))
    print("df_index",df_index)
    print(ym2)
    ym_index = df_index.index(ym2)
    print("ym_index",ym_index)

    # for i in df_index[ym_index:ym_index-12:-1]:
    created_group = created_group[(created_group['Date'] >= df_index[ym_index-12]) & (created_group['Date'] <= df_index[ym_index])]
    # data = counter_3d_test(created_group,ym)
    
    return created_group

def counter_3d(df, ym):
    
    # pivot = pd.pivot_table( df[['월','진행상태','년']], values='진행상태', index = ['년'], columns='월', aggfunc='count')

    ymList = []
    countList = []
    
    # 갯수가 0인 YYYYMM Counting을 위한 코드
    tempList = ['202201','202202','202203','202204','202205','202206','202207','202208','202209','202210','202211','202212',
               '202301', '202302','202303','202304','202305','202306','202307','202308','202309','202310','202311','202312',
               '202401','202402','202403','202404','202405','202406','202407','202408','202409','202410','202411','202412']
    
    realList = []
    
    ym_index = tempList.index(ym)
    
    print("ym_index",ym_index)
        
    for i in tempList[ym_index:ym_index-12:-1]:
        realList.append(i)
    
    print("realList", realList)
        
    # 현재 데이터가 존재하는 Date 모두 뽑기 (mList)
    # 현재 데이터가 존재하는 Date 뽑되, 중복 제거 (mList_dup)
    mList = df['Date'].tolist()
    mList_dup = list(set(df['Date'].tolist()))
    print("dup",mList_dup)
    print("최대값:",max(mList_dup))
    print("최솟값:",min(mList_dup))
    
    for i in realList:
        mon = i
        ymList.append(mon)
        print("YM",ymList)
        if mon in mList_dup:
            countList.append(mList.count(mon))
            print("CL",countList)
        else:
            countList.append(0)
        
    data = pd.DataFrame(zip(ymList,countList))
    data.columns = ['Date', '합계']
    
    print(data)
    
    return data 

def assign_date(row):
    year_int = int(row['년'])
    if year_int >= 2024:
        created_at_datetime = pd.to_datetime(row['created_at'])
        return created_at_datetime.strftime('%Y%m')
    else:
        return pd.to_datetime(f"{row['년']}{row['월'].zfill(2)}", format='%Y%m').strftime('%Y%m')
        # return pd.to_datetime(str(year_int) + row['월'].zfill(2), format='%Y%m').strftime('%Y%m')

def counter_3d_temp(df, ym):
    countDict = defaultdict(int)
    tempList = [
        '202201', '202202', '202203', '202204', '202205', '202206', '202207', '202208', '202209', '202210', '202211', '202212',
        '202301', '202302', '202303', '202304', '202305', '202306', '202307', '202308', '202309', '202310', '202311', '202312',
        '202401', '202402', '202403', '202404', '202405', '202406', '202407', '202408', '202409', '202410', '202411', '202412'
    ]
   
    # In-progress 상태에 대한 처리
    for r in df[df['진행상태'] == 'In-progress'].itertuples():
        created_at_datetime = pd.to_datetime(r.created_at)
        
        start_date = created_at_datetime.strftime('%Y%m')
        end_date = ym
        
        start_index = tempList.index(start_date)
        end_index = tempList.index(end_date) + 1
        for month in tempList[start_index:end_index]:  # 완료된 달은 제외
            countDict[month] += 1

    # Completed 상태에 대한 처리
    for r in df[df['진행상태'] == 'Completed'].itertuples():
        if r.completed_at is not None:
            created_at_datetime = pd.to_datetime(r.created_at)
            completed_at_datetime = pd.to_datetime(r.completed_at)
            
            start_date = created_at_datetime.strftime('%Y%m')
            completed_date = completed_at_datetime.strftime('%Y%m')
            
            start_index = tempList.index(start_date)
            end_index = tempList.index(completed_date) + 1
            
            for month in tempList[start_index:end_index]:
                countDict[month] += 1

    # 결과 데이터 프레임 생성
    current_index = tempList.index(ym)
    start_index = max(0, current_index - 11)
    realList = tempList[start_index:current_index + 1]
   
    data = pd.DataFrame({'Date': realList, '합계': [countDict[month] for month in realList]})
   
    return data

# def counter_3d_temp(df, ym):
    
#     # pivot = pd.pivot_table( df[['월','진행상태','년']], values='진행상태', index = ['년'], columns='월', aggfunc='count')

#     ymList = []
#     countList = []
    
#     # 갯수가 0인 YYYYMM Counting을 위한 코드
#     tempList = ['202201','202202','202203','202204','202205','202206','202207','202208','202209','202210','202211','202212',
#                '202301', '202302','202303','202304','202305','202306','202307','202308','202309','202310','202311','202312',
#                '202401','202402','202403','202404','202405','202406','202407','202408','202409','202410','202411','202412']
    
#     current_index = tempList.index(ym)
#     start_index = max(0, current_index - 11)
#     realList = tempList[start_index:current_index + 1]
    
#     print("current:", current_index)
#     print("start:", start_index)
#     print("real:", realList)
    
#     countDict = defaultdict(int)
    
#     for r in df[df['진행상태'] == 'In-progress'].itertuples():
#         start_month_index = max(tempList.index(r.Date), start_index)
#         end_month_index = min(tempList.index(ym), current_index)
#         for month in tempList[start_month_index:end_month_index+1]:
#             countDict[month] +=1
            
#     for r in df[df['진행상태'] == 'Completed'].itertuples():
#         print("temp:", tempList.index(r.Date))
#         if start_index <= tempList.index(r.Date) <= current_index:
#             countDict[r.Date] +=1
        
#     data = pd.DataFrame({'Date': realList, '합계': [countDict[month] for month in realList]})
#     # data.columns = ['Date', '합계']
    
#     print(data)
    
#     return data 

# def counter_3d_incident(df, ym):
    
#     # pivot = pd.pivot_table( df[['월','진행상태','년']], values='진행상태', index = ['년'], columns='월', aggfunc='count')

#     ymList = []
#     countList = []
    
#     # 갯수가 0인 YYYYMM Counting을 위한 코드
#     tempList = ['202201','202202','202203','202204','202205','202206','202207','202208','202209','202210','202211','202212',
#                '202301', '202302','202303','202304','202305','202306','202307','202308','202309','202310','202311','202312',
#                '202401','202402','202403','202404','202405','202406','202407','202408','202409','202410','202411','202412']
    
#     realList = []
    
#     ym_index = tempList.index(ym)
#     print("ym_index",ym_index)
        
#     for i in tempList[ym_index-1:ym_index-12:-1]:
#         realList.append(i)
    
#     print("realList", realList)
        
#     # 현재 데이터가 존재하는 Date 모두 뽑기 (mList)
#     # 현재 데이터가 존재하는 Date 뽑되, 중복 제거 (mList_dup)
#     mList = df['Date'].tolist()
#     mList_dup = list(set(df['Date'].tolist()))
#     print("dup",mList_dup)
    
#     print("최대값:",max(mList_dup))
#     print("최솟값:",min(mList_dup))
    
#     for i in realList:
#         mon = i
#         ymList.append(mon)
#         print("YM",ymList)
#         if mon in mList_dup:
#             countList.append(mList.count(mon))
#             print("CL",countList)
#         else:
#             countList.append(0)
        
#     data = pd.DataFrame(zip(ymList,countList))
#     data.columns = ['Date', '합계']
    
#     print(data)
    
#     return data 

def counter_3d_k8s(df, ym):
    
    # pivot = pd.pivot_table( df[['월','진행상태','년']], values='진행상태', index = ['년'], columns='월', aggfunc='count')

    ymList = []
    countList = []
    
    # 갯수가 0인 YYYYMM Counting을 위한 코드
    tempList = ['202201','202202','202203','202204','202205','202206','202207','202208','202209','202210','202211','202212',
               '202301', '202302','202303','202304','202305','202306','202307','202308','202309','202310','202311','202312',
               '202401','202402','202403','202404','202405','202406','202407','202408','202409','202410','202411','202412']
    
    realList = []
    
    ym_index = tempList.index(ym)
    print("ym_index",ym_index)
        
    for i in tempList[ym_index-1:ym_index-11:-1]:
        realList.append(i)
    
    print("realList", realList)
        
    # 현재 데이터가 존재하는 Date 모두 뽑기 (mList)
    # 현재 데이터가 존재하는 Date 뽑되, 중복 제거 (mList_dup)
    mList = df['Date'].tolist()
    mList_dup = list(set(df['Date'].tolist()))
    print("dup",mList_dup)
    
    print("최대값:",max(mList_dup))
    print("최솟값:",min(mList_dup))
    
    for i in realList:
        mon = i
        ymList.append(mon)
        print("YM",ymList)
        if mon in mList_dup:
            countList.append(mList.count(mon))
            print("CL",countList)
        else:
            countList.append(0)
        
    data = pd.DataFrame(zip(ymList,countList))
    data.columns = ['Date', '합계']
    
    print(data)
    
    return data 

# def counter_3d_backup(df):
    

#     ymList = []
#     countList_s = []
#     countList_f = []
#     # success = df[(df['Date']==item) & (df['성패']=='O')]
#     # sList = df['성패'].tolist()
#     # amount = df.loc[(df['년']==y) & (df['월']==month)]
#     # success = sList.count('O')
#     # fail = sList.count('X')
#     # success = df[(df['성패']=='O')].tolist()
#     # fail = df[(df['성패']=='X')].tolist()
#     # print("sfList", sList)
#     # print("success", success)
#     # print("fail", fail)
    
#     mList = df['Date'].tolist()
#     mList_dup = list(set(df['Date'].tolist()))
#     mList_dup.sort()
#     print("dup",mList_dup)

#     # df1 = df[(df['Date']==mList_dup) & (df['성패']=='O')]
#     # df2 = df[(df['Date']==mList_dup) & (df['성패']=='X')]
    
#     # for i in mList_dup:
#     # # for i in pd.date_range(Mindt, Maxdt, freq='M'):
#     #     mon = i
#     #     ymList.append(mon)
#     #     # print("YM",ymList)
#     #     if mon in ymList:
#     #         # countList.append(mList_to_int.count(mon)):
#     #         countList_s.append(sList.count('O'))
#     #         countList_f.append(sList.count('X'))
#     # for i,o in zip(mList_dup, df['성패']):

#     for i in mList_dup:
#         mon = i
#         ymList.append(mon)
#         # for item in ymList:
#         success = df[(df['Date']==mon) & (df['성패']=='O')]
#         fail = df[(df['Date']==mon) & (df['성패']=='X')]
#         countList_s.append(len(success))
#         countList_f.append(len(fail))
#             # countList_f.append(len(df.loc[df['성패']=='X']))
    
#     # for r, m, s in zip(regions, data['월'], data['진행상태']):
#     #     print('r,m,s : ', r,m,s)
#     #         for item in r:
#     #             print('item : ', item)
#     #             region_list.append(item)
#     #             status_list.append(s)
#     #             month_list.append(m)
    
#     print("CL_s",countList_s)
#     print("CL_f",countList_f)
            
#     data2 = pd.DataFrame(zip(ymList,countList_s, countList_f))
#     data2.columns = ['Date', '성공', '실패']
    
#     print(data2)
    
#     return data2


def getTables(df, regions, year, month):
    df['장애인지'] = (pd.to_datetime(df['발생인지시간'])-pd.to_datetime(df['장애발생시간'])).astype('timedelta64[m]')
    # df_filtered = df[df['리전'].apply(lambda x: True if re.search(regex, x) else False) & (df['테넌트']== 'PRD') & (df['진행상태']=='완료')]
    df_filtered = df[ df['리전'].isin(regions) & df['테넌트'].isin(['PRD'])]
    # print("df in func", df_filtered)
    
    # df_filtered
    df_filtered['장애인지'] = (pd.to_datetime(df_filtered['발생인지시간'])-pd.to_datetime(df_filtered['장애발생시간'])).astype('timedelta64[m]')
    df_filtered['발생인지시간'] = pd.to_datetime(df_filtered['발생인지시간'])
    
    # timeslot
    # timeslot = df_filtered[(df_filtered['년']==y) & (df_filtered['월']== month)]
    timeslot = df_filtered[ df_filtered['년'].isin([year]) & df_filtered['월'].isin([month]) ]
    timeslot  = timeslot[['발생인지시간', '장애인지', '리전']]
    timeslot.columns = ['일', '장애인지', '리전']
    
    timeslot['일'] = timeslot['일'].dt.day
    # timeslot['장애전파'] = timeslot['장애전파'].astype('timedelta64[m]')
    timeslot.sort_values(by=['일'], ascending=True, inplace=True)
    # print("end of timeslot", timeslot)
    # timeslot
    return df_filtered, timeslot

def getTables2(df, regions, year, month):
    df['장애전파'] = (pd.to_datetime(df['장애전파시간'])-pd.to_datetime(df['발생인지시간'])).astype('timedelta64[m]')
    # df_filtered = df[df['리전'].apply(lambda x: True if re.search(regex, x) else False) & (df['테넌트']== 'PRD') & (df['진행상태']=='완료')]
    df_filtered = df[ df['리전'].isin(regions) & df['테넌트'].isin(['PRD'])]
    
    # df_filtered
    df_filtered['장애전파'] = (pd.to_datetime(df_filtered['장애전파시간'])-pd.to_datetime(df_filtered['발생인지시간'])).astype('timedelta64[m]')
    df_filtered['장애전파시간'] = pd.to_datetime(df_filtered['장애전파시간'])
    
    # timeslot
    timeslot = df_filtered[ df_filtered['년'].isin([year]) & df_filtered['월'].isin([month]) ]
    timeslot  = timeslot[['장애전파시간', '장애전파', '리전']]
    timeslot.columns = ['일', '장애전파', '리전']
    
    timeslot['일'] = timeslot['일'].dt.day
    # timeslot['장애전파'] = timeslot['장애전파'].astype('timedelta64[m]')
    timeslot.sort_values(by=['일'], ascending=True, inplace=True)
    # timeslot
    return df_filtered, timeslot

def preprocess_df(df):
    def extract_region(val):
        if isinstance(val, str) and val.strip() != "":
            parts = val.split("-")
            return "-".join(parts[:3]) if len(parts) >= 3 else "Unknown"
        return "Unknown"

    def extract_tenant(val):
        if isinstance(val, str) and val.strip() != "":
            parts = val.split("-")
            return parts[3] if len(parts) >= 4 else "Unknown"
        return "Unknown"

    df['Region'] = df['availability_zone'].apply(extract_region)
    df['Tenant'] = df['availability_zone'].apply(extract_tenant)

    # Region 축약 이름 매핑
    region_map = {
        "EU-CENTRAL-1": "FR2",
        "EU-CENTRAL-2": "FR7",
        "Unknown": "Unknown"
    }
    df['Region'] = df['Region'].map(region_map).fillna("Other")
    
    return df

def preprocess_df_LB(df):
    # def extract_region(val):
    #     if isinstance(val, str) and val.strip() != "":
    #         parts = val.split("-")
    #         return "-".join(parts[:3]) if len(parts) >= 3 else "Unknown"
    #     return "Unknown"

    # def extract_tenant(val):
    #     if isinstance(val, str) and val.strip() != "":
    #         parts = val.split("-")
    #         return parts[3] if len(parts) >= 4 else "Unknown"
    #     return "Unknown"

    # df['Region'] = df['availability_zone'].apply(extract_region)
    # df['Tenant'] = df['availability_zone'].apply(extract_tenant)

    # Region 축약 이름 매핑
    region_map = {
        "FR2_Admin": "FR2",
        "FR2_PRD-A": "FR2",
        "FR2_PRD-B": "FR2",
        "FR2_PRD-C": "FR2",
        "FR2_PRD-D": "FR2",
        "FR2_STG-A": "FR2",
        "FR2_STG-B": "FR2",
        "FR2_STG-C": "FR2",
        "FR2_STG-D": "FR2",
        "FR7_Admin": "FR7",
        "FR7_PRD-A": "FR7",
        "FR7_PRD-B": "FR7",
        "FR7_PRD-C": "FR7",
        "FR7_PRD-D": "FR7",
        "FR7_STG-A": "FR7",
        "FR7_STG-B": "FR7",
        "FR7_STG-C": "FR7",
        "FR7_STG-D": "FR7",
    }
    df['Tenant'] = df['Tenant'].map(region_map).fillna("Other")
    
    return df    

def getPivotTable_new(df, group_by_col):
    # 비어있거나 유효한 값이 없으면 빈 pivot 반환
    if df.empty or df[group_by_col].dropna().empty:
        print(f"[경고] '{group_by_col}' 기준으로 생성할 수 있는 데이터가 없습니다.")
        return pd.DataFrame(columns=[group_by_col, '합계', '비중']), 0

    # 피벗 테이블 생성
    pivotTable = df.groupby(group_by_col).size().reset_index(name='합계')
    pivotTable.sort_values(by='합계', ascending=False, inplace=True)
    total = pivotTable['합계'].sum()
    pivotTable['비중'] = round((pivotTable['합계'] / total) * 100, 1)

    return pivotTable, total


def getPivotTable(df):
    if 'flavor' in df:
        # df_filtered = df.loc[(df['월']==month) & (df['년']==y) & (df['테넌트']== 'PRD') & (df['진행상태']=='완료')]
        pivotTable = pd.pivot_table(df[['availability_zone','진행상태']], index = ['리전'], aggfunc = 'count').rename_axis('리전').reset_index()
        pivotTable.columns = ['리전', '합계']
        pivotTable.sort_values(by=['합계'], ascending=False, inplace=True)
        pivotTable.reset_index(drop=True, inplace=True)
        total = pivotTable["합계"].sum()
        pivotTable['비중'] = round((pivotTable['합계'] / total) * 100, 1)
    elif '작업_Title' in df:
        # 
        # df_filtered = df.loc[(df['월']==month) & (df['년']==y) & (df['테넌트']== 'PRD')]
        pivotTable = pd.pivot_table(df[['리전','진행상태']], index = ['리전'], aggfunc = 'count').rename_axis('리전').reset_index()
        pivotTable.columns = ['리전', '합계']
        pivotTable.sort_values(by=['합계'], ascending=False, inplace=True)
        pivotTable.reset_index(drop=True, inplace=True)
        total = pivotTable["합계"].sum()
        pivotTable['비중'] = round((pivotTable['합계'] / total) * 100, 1) 
    elif '클러스터명' in df:
        # 자산관리 K8s
        # df_filtered = df.loc[(df['월']==month) & (df['년']==y) & (df['테넌트']== 'PRD')]
        pivotTable = pd.pivot_table(df[['리전', '클러스터명']], index = ['리전'], aggfunc = 'count').rename_axis('리전').reset_index()    
        pivotTable.columns = ['리전', '합계']
        pivotTable.sort_values(by=['합계'], ascending=False, inplace=True)
        pivotTable.reset_index(drop=True, inplace=True)
        total = pivotTable["합계"].sum()
        pivotTable['비중'] = round((pivotTable['합계'] / total) * 100, 1)

    elif '성패' in df:
        # 백업관리 DB
        # df_filtered = df.loc[(df['월']==month) & (df['년']==y) & (df['테넌트']== 'PRD')]
        pivotTable = pd.pivot_table(df[['리전', '성패']], index = ['리전'], aggfunc = 'count').rename_axis('리전').reset_index()       
        pivotTable.columns = ['리전', '합계']
        pivotTable.sort_values(by=['합계'], ascending=False, inplace=True)
        pivotTable.reset_index(drop=True, inplace=True)
        total = pivotTable["합계"].sum()
        pivotTable['비중'] = round((pivotTable['합계'] / total) * 100, 1)        
    elif 'count' in df:
        # 집계
        # df_filtered = df.loc[(df['월']==month) & (df['년']==y) & (df['테넌트']== 'PRD')]
        pivotTable = pd.pivot_table(df[['리전', 'count']], index = ['리전'], aggfunc = 'sum').rename_axis('리전').reset_index() 
        pivotTable["합계"] = pivotTable.sum(axis=1)
        pivotTable.sort_values(by=['합계'], ascending=False, inplace=True)
        total = pivotTable["합계"].sum()
        pivotTable['비중'] = round((pivotTable['합계'] / total) * 100, 1)       
    else:
        # 표준 데이터
        # df_filtered = df.loc[(df['월']==month) & (df['년']==y) & (df['테넌트']== 'PRD') & (df['진행상태']=='완료')]
        pivotTable = pd.pivot_table(df[['리전','진행상태']], index = ['리전'], aggfunc = 'count').rename_axis('리전').reset_index()
        pivotTable.columns = ['리전', '합계']
        pivotTable.sort_values(by=['합계'], ascending=False, inplace=True)
        pivotTable.reset_index(drop=True, inplace=True)
        total = pivotTable["합계"].sum()
        pivotTable['비중'] = round((pivotTable['합계'] / total) * 100, 1)

    return pivotTable, total

def getPivotTable_regular(df_filtered, month, y):    
    # 표준 데이터
    df_filtered = df.loc[(df['월']==month) & (df['년']==y) & (df['진행상태']=='Completed')]
    # print("df",df_filtered)
    pivotTable = pd.pivot_table(df_filtered[['리전','진행상태']], index = ['리전'], aggfunc = 'count').rename_axis('리전').reset_index()
    print("pivot", pivotTable)
    pivotTable.columns = ['리전', '합계']
    pivotTable.sort_values(by=['합계'], ascending=False, inplace=True)
    pivotTable.reset_index(drop=True, inplace=True)
    total = pivotTable["합계"].sum()
    pivotTable['비중'] = round((pivotTable['합계'] / total) * 100, 1)

    return pivotTable, total

def getPivotTable2(df):
    # 집계 데이터
    if 'count' in df:
        # df_filtered = df.loc[(df['월']==month) & (df['테넌트']== 'PRD') & (df['년']==y)]
        pivotTable = pd.pivot_table(df[['리전', '유형', 'count']], values = 'count', index = ["유형"], columns = ["리전"], aggfunc = 'sum')
        pivotTable["합계"] = pivotTable.sum(axis=1)
    else:
        pivotTable, total = None, None
        
    pivotTable.sort_values(by=['합계'], ascending=False, inplace=True)
    total = pivotTable["합계"].sum()
    pivotTable['비중'] = round((pivotTable['합계'] / total) * 100, 1)
    return pivotTable, total


def getPivotTable_security(df_filtered, month):
   
    # 표준 데이터
    # df_filtered = df.loc[(df['월']==month) & (df['테넌트']== 'PRD') ]
    # df_filtered = df.loc[(df['월']==month) & (df['테넌트']== 'PRD') & (df['진행상태']=='완료')]
    
    pivotTable = pd.pivot_table(df_filtered[['리전','진행상태']], index = ['리전'], aggfunc = 'count').rename_axis('리전').reset_index()
    pivotTable.columns = ['리전', '합계']
    pivotTable.sort_values(by=['합계'], ascending=False, inplace=True)
    pivotTable.reset_index(drop=True, inplace=True)
    total = pivotTable["합계"].sum()
    pivotTable['비중'] = round((pivotTable['합계'] / total) * 100, 1)

    return pivotTable, total

def getPivotTable_event(df_filtered, month, region_list):

    #pivotTable = pd.pivot_table(df_filtered[['리전','진행상태']], index = ['리전','진행상태'], aggfunc = 'count').rename_axis('리전').reset_index()
    pivotTable = pd.pivot_table(df_filtered[['진행상태','리전','년']], index = ['진행상태','리전'], aggfunc = 'count').rename_axis(['진행상태','리전']).reset_index()
    pivotTable.columns = ['진행상태','리전', '합계']
    
    pivot = pivotFlatten_2c(pivotTable, region_list)
    
    pivot.sort_values(by=['합계'], ascending=False, inplace=True)
    pivot.reset_index(drop=True, inplace=True)
    total = pivot["합계"].sum()
    pivot['비중'] = round((pivot['합계'] / total) * 100, 1)

    return df_filtered, pivot, total

def pivotFlatten_2c(pivotTable, region_list):
    regions = []
    counts = []
    statuses = []
    region_flatten = []
    status_flatten = []
    countByRegion = []
    completed_countByRegion = []
    incompleted_countByRegion = []

    for index, row in pivotTable.iterrows():
        list = re.split(',|/|\|', row['리전'])
        regions.append(list)
        counts.append(row['합계'])
        statuses.append(row['진행상태'])
    for (c, r, s) in zip(counts, regions, statuses):
        for j in r:
            region_flatten.append(j * c)
            status_flatten.append(s)
            
    for r in region_list:
        regex = r
        region_count = 0
        for s in region_flatten:
            for match in re.finditer(regex, s):
                region_count += 1
        countByRegion.append(region_count)
        
    for r in region_list:
        regex = r
        complete_count = 0
        incomplete_count = 0
        for rf, sf in zip(region_flatten, status_flatten):
            for match in re.finditer(regex, rf):
                for match in re.finditer("완료", sf):
                    complete_count += 1
                for match in re.finditer("진행중", sf):
                    incomplete_count += 1
        completed_countByRegion.append(complete_count)
        incompleted_countByRegion.append(incomplete_count)
        
    pivot = pd.DataFrame((zip(region_list, countByRegion, completed_countByRegion, incompleted_countByRegion )), columns=['리전', '합계', '완료', '미완료'])       
    
    return pivot       
    
    
def pivotFlatten(pivotTable, region_list):
    regions = []
    counts = []
    pivot_flatten = []
    countByRegion = []
    complete_countByRegion = []
    incomplete_countByRegion = []
    
    for index, row in pivotTable.iterrows():
        list = re.split(',|/|\|', row['리전'])
        regions.append(list)
        counts.append(row['합계'])

    for (c, r) in zip(counts, regions):
        for j in r:
            pivot_flatten.append(j * c)

    for r in region_list:
        regex = r
        region_count = 0
        for s in pivot_flatten:
            for match in re.finditer(regex, s):
                region_count += 1
        countByRegion.append(region_count)

    for r in region_list:
        regex = r
        complete_count = 0
        incomplete_count = 0
        for s in pivotTable['진행상태']:
            if s == '완료':
                complete_count += 1
            else:
                incomplete_count += 1
        complete_countByRegion.append(complete_count)
        incomplete_countByRegion.append(incomplete_count)
        
    pivot = pd.DataFrame((zip(region_list, countByRegion, complete_count, incomplete_count )), columns=['리전', '합계', '완료', '미완료'])
    return pivot    

def getPivotTable_capacity(df_filtered, month):
   
    # 표준 데이터
    # df_filtered = df.loc[(df['월']==month) & (df['테넌트']== 'PRD') ]
    # df_filtered = df.loc[(df['월']==month) & (df['테넌트']== 'PRD') & (df['진행상태']=='완료')]
    
    pivotTable = pd.pivot_table(df_filtered[['리전','카테고리']], index = ['리전'], aggfunc = 'count').rename_axis('리전').reset_index()
    pivotTable.columns = ['리전', '합계']
    pivotTable.sort_values(by=['합계'], ascending=False, inplace=True)
    pivotTable.reset_index(drop=True, inplace=True)
    total = pivotTable["합계"].sum()
    pivotTable['비중'] = round((pivotTable['합계'] / total) * 100, 1)

    return pivotTable, total

def flatten_4d(data):
    regions = []
    regions_flatten = []
    regions_count = []  

    for s in data['리전']:
        list = re.split(',|/|\|', s)
        regions.append(list)

    region_list = []
    status_list = []
    month_list = []
    
    for r, m, s in zip(regions, data['진행상태'], data['작업유형']):
        # print('r,m,s : ', r,m,s)
        for item in r:
            # print('item : ', item)
            region_list.append(item)
            status_list.append(s)
            month_list.append(m)

    data = pd.DataFrame(zip(region_list, month_list, status_list))
    data.columns = ['리전','진행상태', '작업유형']
    
    return data  

def flatten_5d(data):
    regions = []
    regions_flatten = []
    regions_count = []  

    for s in data['리전']:
        list = re.split(',|/|\|', s)
        regions.append(list)

    region_list = []
    status_list = []
    month_list = []
    
    for r, m, s in zip(regions, data['진행상태'], data['Work Type']):
        # print('r,m,s : ', r,m,s)
        for item in r:
            # print('item : ', item)
            region_list.append(item)
            status_list.append(s)
            month_list.append(m)

    data = pd.DataFrame(zip(region_list, month_list, status_list))
    data.columns = ['리전','진행상태', 'Work Type']
    
    return data    


# def getPivotTable_license(df, month):
#         df_filtered = df.loc[(df['월']==month) & (df['테넌트']== 'PRD')]
#         pivotTable = pd.pivot_table(df_filtered[['리전', '유형']], index = ['리전'], aggfunc = 'count').rename_axis('리전').reset_index()       
#         pivotTable.columns = ['리전', '합계']
#         pivotTable.sort_values(by=['합계'], ascending=False, inplace=True)
#         pivotTable.reset_index(drop=True, inplace=True)
#         total = pivotTable["합계"].sum()
#         pivotTable['비중'] = round((pivotTable['합계'] / total) * 100, 1)    

def getPivotTable_license(df_filtered, month, region_list):

    pivotTable = pd.pivot_table(df_filtered[['리전','년','진행상태','유형']], index = ['리전','유형'], aggfunc = 'count').rename_axis(['유형','리전']).reset_index()
    pivotTable.columns = ['리전','진행상태', '유형', '합계']
    
    pivot = pivotFlatten_2c(pivotTable, region_list)
    # pivot = pivotTable
    
    pivot.sort_values(by=['합계'], ascending=False, inplace=True)
    pivot.reset_index(drop=True, inplace=True)
    total = pivot["합계"].sum()
    pivot['비중'] = round((pivot['합계'] / total) * 100, 1)

    return df_filtered, pivot, total        

def getPivotTable_event_db_license(df_filtered, month, region_list):

    pivotTable = pd.pivot_table(df_filtered[['리전','년', '유형']], index = ['리전','유형'], aggfunc = 'count').rename_axis(['유형','리전']).reset_index()
    pivotTable.columns = ['리전', '유형', '합계']
    
    # pivot = pivotFlatten_2c(pivotTable, region_list)
    # pivot = flatten_d_db_license(pivotTable)
    
    pivot = pivotTable
    
    pivot.sort_values(by=['합계'], ascending=False, inplace=True)
    pivot.reset_index(drop=True, inplace=True)
    total = pivot["합계"].sum()
    pivot['비중'] = round((pivot['합계'] / total) * 100, 1)

    return df_filtered, pivot, total

def getPivotTable_event_db_license_2(df_filtered, month, region_list):

    pivotTable = pd.pivot_table(df_filtered[['리전','년']], index = ['리전'], aggfunc = 'count').rename_axis(['리전']).reset_index()
    pivotTable.columns = ['리전', '합계']
    
    # pivot = pivotFlatten_2c(pivotTable, region_list)
    # pivot = flatten_d_db_license(pivotTable)
    
    pivot = pivotTable
    
    pivot.sort_values(by=['합계'], ascending=False, inplace=True)
    pivot.reset_index(drop=True, inplace=True)
    total = pivot["합계"].sum()
    pivot['비중'] = round((pivot['합계'] / total) * 100, 1)

    return df_filtered, pivot, total
# def flatten_d_db_license(data):
#     regions = []
#     regions_flatten = []
#     regions_count = []  

#     for s in data['리전']:
#         list = re.split(',|/|\|', s)
#         regions.append(list)

#     region_list = []
#     status_list = []
#     month_list = []
    
#     # 공급사 = MCCS, Tiebro, mongo 등
#     # 유형 = 공식/임시 
    
#     for r, m, s in zip(regions, data['공급사'], data['유형']):
#         # print('r,m,s : ', r,m,s)
#         for item in r:
#             # print('item : ', item)
#             region_list.append(item)
#             status_list.append(s)
#             month_list.append(m)

#     data = pd.DataFrame(zip(region_list, month_list, status_list))
#     data.columns = ['리전','라이선스', '유형']
    
#     return data    

def flatten_d_db_license(data):
    # regions = []
    # regions_flatten = []
    # regions_count = []  

    # for s in data['리전']:
    #     list = re.split(',|/|\|', s)
    #     regions.append(list)

    region_list = []
    status_list = []
    
    # 공급사 = MCCS, Tiebro, mongo 등
    # 유형 = 공식/임시 
    
    for r, s in zip(data['리전'], data['유형']):
        # print('r,m,s : ', r,m,s)
        for item in r:
            # print('item : ', item)
            region_list.append(item)
            status_list.append(s)

    data = pd.DataFrame(zip(region_list, status_list))
    data.columns = ['리전', '유형']
    
    return data  