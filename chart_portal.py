
import pandas as pd
from pandas import Series, DataFrame
# from pandas_ods_reader import read_ods
from datetime import datetime, timedelta

import altair as alt
import pandas as pd
import re  

def hanfont():
    font = "맑은고딕"
    
    return {
        "config" : {
             "axis": {
                  "fontSize": 12,                
                  "font": font,
                  "anchor": "start", # equivalent of left-aligned.
                  "fontColor": "#000000"
             }
        }
    }

def getStackedHBarChart(source):
    bar = alt.Chart(source).mark_bar().encode(
        x=alt.X('count(리전):Q', stack='zero', title=''),         
        y=alt.Y('진행상태:O', sort='ascending'),  
        # order=alt.Order("count(리전):Q", sort='descending'),
        color=alt.Color('리전:N') #, legend=None)   
    )
    
    text1 = alt.Chart(source).mark_text(dx=-20, dy=0, color='black').encode(
        x=alt.X('count(리전):Q', stack='zero', sort='ascending'),        
        y=alt.Y('진행상태:N', sort='ascending'),        
        detail=alt.Color("리전:N"),
        text = alt.Text('count(리전):Q', format='d') #, sort='descending')
    )
    
    text2 = alt.Chart(source).mark_text(dx=10, dy=-3, color='black').encode(
        x=alt.X('count(리전):Q', stack='zero', title=''),         
        y=alt.Y('진행상태:N'),        
        # order=alt.Order("count(리전):Q", sort='descending'),
        # color=alt.Color('리전:N'), # legend=None)   
        text = alt.Text('count(리전):Q', format='d')
        # text = alt.Text('sum(count):Q', format='d')        
    ) 
    
    chart = (bar + text1 + text2).properties(width=360, height=360)
    return chart

def getStackedHBarChart1(source):
    bar = alt.Chart(source).mark_bar().encode(
        x=alt.X('sum(count):Q', stack='zero', title=''),
        y=alt.Y('월:N'),
        color=alt.Color("유형:N") #, legend=None)   
    )
    line = alt.Chart(source).mark_line(color="red").encode(
        x=alt.X('sum(count):Q', title=''),
        y=alt.Y('월:N', title='월별 추세')
    )
    text1 = alt.Chart(source).mark_text(dx=0, dy=3, color='black').encode(
        x=alt.X('sum(count):Q', stack='zero'),
        y=alt.Y('월:N'),
        detail=alt.Color("유형:N"),
        text = alt.Text('sum(count):Q', format='d')
    )
    text2 = line.mark_text(dx=20, dy=0, color='red').encode(
        x=alt.X('sum(count):Q'),
        y=alt.Y('월:N'),
        text = alt.Text('sum(count):Q', format='d')
    )    
    chart = (bar + line + text1 + text2).properties(width=360, height=360)
    return chart


# def getStackedVBarChart1(source):
#     bar = alt.Chart(source).mark_bar().encode(
#         x=alt.X('월:N', stack='zero', title=''),
#         y=alt.Y('sum(count):Q'),
#         color=alt.Color("유형:N") #, legend=None)   
#     )
#     line = alt.Chart(source).mark_line(color="red").encode(
#         x=alt.X('월:N', title=''),
#         y=alt.Y('sum(count):Q', title='월별 추세')
#     )
#     text1 = alt.Chart(source).mark_text(dx=-20, dy=0, color='black').encode(
#         x=alt.X('월:N'),        
#         y=alt.Y('sum(count):Q', stack='zero'),     
#         detail=alt.Color("유형:N"),
#         text = alt.Text('sum(count):Q', format='d')
#     )
#     text2 = line.mark_text(dx=0, dy=-15, color='red').encode(
#         x=alt.X('월:N'),        
#         y=alt.Y('sum(count):Q'),
#         text = alt.Text('sum(count):Q', format='d')
#     )        
#     chart = (bar + line + text1 + text2).properties(width=360, height=360)
#     return chart    

def getStackedVBarChart1(source):
    bar = alt.Chart(source).mark_bar().encode(
        x=alt.X('Date:N', stack='zero', title=''),
        y=alt.Y('sum(count):Q'),
        color=alt.Color("유형:N") #, legend=None)   
    )
    line = alt.Chart(source).mark_line(color="red").encode(
        x=alt.X('Date:N', title=''),
        y=alt.Y('sum(count):Q', title='월별 추세')
    )
    text1 = alt.Chart(source).mark_text(dx=-20, dy=0, color='black').encode(
        x=alt.X('Date:N'),        
        y=alt.Y('sum(count):Q', stack='zero'),     
        detail=alt.Color("유형:N"),
        text = alt.Text('sum(count):Q', format='d')
    )
    text2 = line.mark_text(dx=0, dy=-15, color='red').encode(
        x=alt.X('Date:N'),        
        y=alt.Y('sum(count):Q'),
        text = alt.Text('sum(count):Q', format='d')
    )        
    chart = (bar + line + text1 + text2).properties(width=360, height=360)
    return chart    


    
def getBarChart1(source):
    bar = alt.Chart(source).mark_bar().encode(
        x=alt.X('리전'),
        y=alt.Y('count()', title=''),
        color=alt.Color("리전:N", legend=None)
    )
    text = bar.mark_text(
        align='center', # align='left',
        baseline='middle',
        dx=7  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
        text='count():Q'
    )

    chart = (bar + text).properties(width=360, height=360)
    return chart

def getBarChart1s(source, month):
    
    bar = alt.Chart(source).mark_bar().encode(
        x=alt.X('유형:N'),
        y=alt.Y('sum(count)', title=''),
        color=alt.Color("유형:N", legend=None)
    )
    text = bar.mark_text(
        align='center', # align='left',
        baseline='middle',
        dx=7  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
        text='sum(count):Q'
    )

    chart = (bar + text).properties(width=360, height=360)
    return chart

def getBarChart2(source, month):
    bar = alt.Chart(source).mark_bar().encode(
        x=alt.X('월'),
        y=alt.Y('count()', title=''),
        color=alt.Color("성패:N", legend=None)
    )
    text = bar.mark_text(
        align='center', # align='left',
        baseline='middle',
        dx=7  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
        text='count():Q'
    )

    chart = (bar + text).properties(width=360, height=360)
    return chart


def getBarChart2s(source, month):
    
    bar = alt.Chart(source).mark_bar().encode(
        x=alt.X('월:N'),
        y=alt.Y('sum(count)', title=''),
        color=alt.Color("유형:N", legend=None)
    )
    text = bar.mark_text(
        align='left', # align='center',
        baseline='top', # baseline='middle',
        dx=7  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
        text='sum(count):Q'
    )

    chart = (bar + text).properties(width=360, height=360)
    return chart

def getBarChart3s(source, month):
    
    bar = alt.Chart(source).mark_bar().encode(
        x=alt.X('유형:N'),
        y=alt.Y('sum(count)', title=''),
        color=alt.Color("유형:N", legend=None)
    )
    text = bar.mark_text(
        align='center', # align='left',
        baseline='middle',
        dx=7  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
        text='sum(count):Q'
    )

    chart = (bar + text).properties(width=360, height=360)
    return chart

def getPieChart_region(source):
    base = alt.Chart(source).encode(
        theta=alt.Theta("합계:Q", stack=True), 
        color=alt.Color("Region:N"),
        order=alt.Order("합계:Q", sort='descending')
    )

    pie = base.mark_arc(outerRadius=130)

    text = pie.mark_text(
        size=12,
        radius=180,        
        color='black'
    ).encode(
        text="label:N"
    ).transform_calculate(
        label = alt.datum.Region + ": " + alt.datum.합계   + ", " + alt.datum.비중 +"%"
    )

    chart = (pie + text).properties(width=360, height=360)
    return chart

def getPieChart_tenant(source):
    base = alt.Chart(source).encode(
        theta=alt.Theta("합계:Q", stack=True), 
        color=alt.Color("Tenant:N"),
        order=alt.Order("합계:Q", sort='descending')
    )

    pie = base.mark_arc(outerRadius=130)

    text = pie.mark_text(
        size=12,
        radius=180,        
        color='black'
    ).encode(
        text="label:N"
    ).transform_calculate(
        label = alt.datum.Tenant + ": " + alt.datum.합계   + ", " + alt.datum.비중 +"%"
    )

    chart = (pie+text).properties(width=360, height=360)
    return chart

def getPieChart2(source):
    base = alt.Chart(source).encode(
        theta=alt.Theta("합계:Q", stack=True), 
        color=alt.Color("DBMS유형:N", legend=None),
        order=alt.Order("합계:Q", sort='descending')
    )

    pie = base.mark_arc(outerRadius=120)

    text = pie.mark_text(
        size=12,
        radius=160,        
        color='black'
    ).encode(
        text="label:N"
    ).transform_calculate(
        label = alt.datum.DBMS유형 + ": " + alt.datum.합계   + ", " + alt.datum.비중 +"%"
    )

    chart = (pie).properties(width=360, height=360)
    return chart


def getLineChart_new(df):
    source = df
    # mList = df['Date'].tolist()
    # mList_to_int = [int(i) for i in mList]
    # mList_to_str = str(mList_to_int)
    # print(mList_to_str)
    # start = datetime.strptime(min(mList_to_str), '%Y%m')
    # end = datetime.strptime(max(mList_to_str), '%Y%m')
    # mList_to_date = [datetime.strptime('%Y%m') for date in pd.date_range(start, periods=(end-start).months+1)]
    # print(mList_to_date)
    
    # Min = str(min(mList_to_int))
    # Max = str(max(mList_to_int))
    # print(type(Min), type(Max))
    # print(Min, Max)
    # Mind = datetime.strptime(Min, '%Y%m')
    # Maxd = datetime.strptime(Max, '%Y%m')
    
    point = alt.Chart(source).mark_point().encode(
        # x=alt.X('Date', scale=alt.Scale(padding=15), title='월별 추세'),
        # x=alt.X('Date', scale=alt.Scale(domain=[202205, 202212]), title='월별 추세'),
        # x=alt.X('Date:T', axis=alt.Axis(format="%Y-%m"), scale=alt.Scale(padding=15), title='월별 추세')
        # x=alt.X('Date:N', scale=alt.Scale(domain=[Min,Max], padding=15), title='월별 추세'),
        # x=alt.X('year(Date):O', axis=alt.Axis(format="%Y-%y, %M-%m"), scale=alt.Scale(padding=15), title='월별 추세'),
        x=alt.X('Date:O', scale=alt.Scale(padding=15), title='월별 추세'),
        y=alt.Y('합계', title='발생 건수')
    )

    line = alt.Chart(source).mark_line(color="red").encode(
        # x=alt.X('yearmonth(Date):O', title='월별 추세'),
        x=alt.X('Date:O', title='월별 추세'),
        y=alt.Y('합계', title='')
    )

    text = point.mark_text(
        size=12,
        align='center',
        baseline='line-top',
        color='black',
        dy=-20,
        fontSize=12,
    ).encode(
        text = '합계:Q'
    )

    chart = (point + line + text).properties(width=360, height=200)
    return chart

def getLineChart_capacity(df):
    source = df
    # mList = df['Date'].tolist()
    # mList_to_int = [int(i) for i in mList]
    # mList_to_str = str(mList_to_int)
    # print(mList_to_str)
    # start = datetime.strptime(min(mList_to_str), '%Y%m')
    # end = datetime.strptime(max(mList_to_str), '%Y%m')
    # mList_to_date = [datetime.strptime('%Y%m') for date in pd.date_range(start, periods=(end-start).months+1)]
    # print(mList_to_date)
    
    # Min = str(min(mList_to_int))
    # Max = str(max(mList_to_int))
    # print(type(Min), type(Max))
    # print(Min, Max)
    # Mind = datetime.strptime(Min, '%Y%m')
    # Maxd = datetime.strptime(Max, '%Y%m')
    
    point = alt.Chart(source).mark_point().encode(
        # x=alt.X('Date', scale=alt.Scale(padding=15), title='월별 추세'),
        # x=alt.X('Date', scale=alt.Scale(domain=[202205, 202212]), title='월별 추세'),
        # x=alt.X('Date:T', axis=alt.Axis(format="%Y-%m"), scale=alt.Scale(padding=15), title='월별 추세')
        # x=alt.X('Date:N', scale=alt.Scale(domain=[Min,Max], padding=15), title='월별 추세'),
        # x=alt.X('year(Date):O', axis=alt.Axis(format="%Y-%y, %M-%m"), scale=alt.Scale(padding=15), title='월별 추세'),
        x=alt.X('Date:N', scale=alt.Scale(padding=15), title='월별 추세'),
        y=alt.Y('count()', title='발생 건수'),
        color=alt.Color("진행상태:N", legend=alt.Legend(title="진행상태"), sort=['완료'])
    )

    line = alt.Chart(source).mark_line(color="red").encode(
        # x=alt.X('yearmonth(Date):O', title='월별 추세'),
        x=alt.X('Date:N', title='월별 추세'),
        y=alt.Y('count(Date)', title='')
    )

    text = line.mark_text(
        size=12,
        align='center',
        baseline='line-top',
        color='black',
        dy=-30,
        fontSize=12,
    ).encode(
        text = 'count(Date):Q'
    )
    text2 = point.mark_text(
        size=12,
        align='center',
        baseline='line-top',
        color='black',
        dy=-20,
        fontSize=12,
    ).encode(
        text = 'count(진행상태):Q'
    )
    
    chart = (point + line + text + text2).properties(width=360, height=280)
    return chart

def getLineChart_regular(df):
    source = df
    # mList = df['Date'].tolist()
    # mList_to_int = [int(i) for i in mList]
    # mList_to_str = str(mList_to_int)
    # print(mList_to_str)
    # start = datetime.strptime(min(mList_to_str), '%Y%m')
    # end = datetime.strptime(max(mList_to_str), '%Y%m')
    # mList_to_date = [datetime.strptime('%Y%m') for date in pd.date_range(start, periods=(end-start).months+1)]
    # print(mList_to_date)
    
    # Min = str(min(mList_to_int))
    # Max = str(max(mList_to_int))
    # print(type(Min), type(Max))
    # print(Min, Max)
    # Mind = datetime.strptime(Min, '%Y%m')
    # Maxd = datetime.strptime(Max, '%Y%m')
    
    point = alt.Chart(source).mark_point().encode(
        x=alt.X('Date:N', scale=alt.Scale(padding=15), title='월별 추세'),
        y=alt.Y('count()', title='발생 건수'),
        # color=alt.Color('진행상태:N', legend=alt.Legend(title="진행상태", sort=alt.EncodingSortField('count()', op='mean', order='descending')))
        color=alt.Color('진행상태:N', legend=alt.Legend(title="진행상태"), sort=['완료'])
    )

    line = alt.Chart(source).mark_line(color="red").encode(
        x=alt.X('Date:N', title='월별 추세'),
        y=alt.Y('count(Date)', title='')
    )

    text = line.mark_text(
        size=12,
        align='center',
        baseline='line-top',
        color='black',
        dy=-20,
        fontSize=12,
    ).encode(
        text = 'count(Date):Q'
    )
    text2 = point.mark_text(
        size=12,
        align='center',
        baseline='line-top',
        color='black',
        dy=-20,
        fontSize=12,
    ).encode(
        text = 'count(진행상태):Q'
    )

    chart = (point + line + text + text2).properties(width=360, height=200)
    return chart

def getLineChart_complete(df):
    source = df
    # mList = df['Date'].tolist()
    # mList_to_int = [int(i) for i in mList]
    # mList_to_str = str(mList_to_int)
    # print(mList_to_str)
    # start = datetime.strptime(min(mList_to_str), '%Y%m')
    # end = datetime.strptime(max(mList_to_str), '%Y%m')
    # mList_to_date = [datetime.strptime('%Y%m') for date in pd.date_range(start, periods=(end-start).months+1)]
    # print(mList_to_date)
    
    # Min = str(min(mList_to_int))
    # Max = str(max(mList_to_int))
    # print(type(Min), type(Max))
    # print(Min, Max)
    # Mind = datetime.strptime(Min, '%Y%m')
    # Maxd = datetime.strptime(Max, '%Y%m')
    
    point = alt.Chart(source).mark_point().encode(
        # x=alt.X('Date', scale=alt.Scale(padding=15), title='월별 추세'),
        # x=alt.X('Date', scale=alt.Scale(domain=[202205, 202212]), title='월별 추세'),
        # x=alt.X('Date:T', axis=alt.Axis(format="%Y-%m"), scale=alt.Scale(padding=15), title='월별 추세')
        # x=alt.X('Date:N', scale=alt.Scale(domain=[Min,Max], padding=15), title='월별 추세'),
        # x=alt.X('year(Date):O', axis=alt.Axis(format="%Y-%y, %M-%m"), scale=alt.Scale(padding=15), title='월별 추세'),
        x=alt.X('Date:O', scale=alt.Scale(padding=15), title='월별 추세'),
        y=alt.Y('count(Date)', title='발생 건수')
    )

    line = alt.Chart(source).mark_line(color="red").encode(
        # x=alt.X('yearmonth(Date):O', title='월별 추세'),
        x=alt.X('Date:O', title='월별 추세'),
        y=alt.Y('count(Date)', title='')
    )

    text = point.mark_text(
        size=12,
        align='center',
        baseline='line-top',
        color='black',
        dy=-20,
        fontSize=12,
    ).encode(
        text = 'count(Date):Q'
    )

    chart = (point + line + text).properties(width=360, height=200)
    return chart

def getLineChart(df):
    source = df
    point = alt.Chart(source).mark_point().encode(
        x=alt.X('월', scale=alt.Scale(padding=15), title='월별 추세'),
        y=alt.Y('합계', title='발생 건수')
    )

    line = alt.Chart(source).mark_line(color="red").encode(
        x=alt.X('월', title='월별 추세'),
        y=alt.Y('합계', title='')
    )

    text = point.mark_text(
        size=12,
        align='center',
        baseline='line-top',
        color='black',
        dy=-20,
        fontSize=12,
    ).encode(
        text = '합계:Q'
    )

    chart = (point + line + text).properties(width=360, height=200)
    return chart


def getLineChart2(df):
    source = df
    point = alt.Chart(source).mark_point().encode(
        x=alt.X('Date:N', scale=alt.Scale(padding=15), title='월별 추세'),
        y=alt.Y('count()', title='발생 건수')
    )

    line = alt.Chart(source).mark_line(color="red").encode(
        x=alt.X('Date:N', title='월별 추세'),
        y=alt.Y('count()', title='')
    )

    text = point.mark_text(
        size=12,
        align='center',
        baseline='line-top',
        color='black',
        dy=-20,
        fontSize=12,
    ).encode(
        text = 'count(성패):Q'
    )

    chart = (point + line + text).properties(width=360, height=200)
    return chart

def getLineChart2s(df):
    source = df    
    point = alt.Chart(source).mark_point().encode(
        x=alt.X('Date:N', scale=alt.Scale(padding=15), title='월별 추세'),
        y=alt.Y('count:Q', title='수량'),
        # text=alt.Text("성패:N")
    )

    line = alt.Chart(source).mark_line(color="red").encode(
        x=alt.X('Date:N', title='월별 추세'),
        y=alt.Y('count:Q', title='')
    )

    text = point.mark_text(
        size=12,
        align='center',
        baseline='line-top',
        color='black',
        dy=-20,
        fontSize=12,
    ).encode(
        text = 'count:Q'
    )

    chart = (point + line + text).properties(width=360, height=200)
    return chart

def getLineChart3(df, df2):
    source = df
    source2 = df2
    
    point = alt.Chart(source).mark_point().encode(
        x=alt.X('Date:N', scale=alt.Scale(padding=15), title='월별 추세'),
        y=alt.Y('count()', title='발생 건수'),
        color=alt.Color('성패:N', legend=alt.Legend(title="성패 및 비표준설치"))
    )
    
    point2 = alt.Chart(source2).mark_point().encode(
        x=alt.X('Date:N', scale=alt.Scale(padding=15), title='월별 추세'),
        y=alt.Y('count()'),
        color=alt.Color('비고:N')
    )
    
    line = alt.Chart(source).mark_line(color="red").encode(
        x=alt.X('Date:N', title='월별 추세'),
        y=alt.Y('count(Date)', title='발생 건수')
    )

    text = point.mark_text(
        size=12,
        align='center',
        baseline='line-top',
        color='black',
        dy=-20,
        fontSize=12,
    ).encode(
        text = 'count(성패):Q'
    )
    
    text2 = line.mark_text(
        size=12,
        align='center',
        baseline='line-top',
        color='black',
        dy=-20,
        fontSize=12,
    ).encode(
        text = 'count(Date):Q'       
    )
    
    text3 = point2.mark_text(
        size=12,
        align='center',
        baseline='line-top',
        color='black',
        dy=4,
        fontSize=12,
    ).encode(
        text = 'count(비고):Q'       
    )

    chart = (point + point2 + line + text + text2 + text3).properties(width=360, height=250)
    return chart


# def getLineChart3(df, df2, month):
#     source = df
#     source2 = df2
    
#     point = alt.Chart(source2).mark_point().encode(
#         x=alt.X('Date:N', scale=alt.Scale(padding=15), title='월별 추세'),
#         y=alt.Y('성공', title='발생 건수'),
#         # color=alt.Color('성공:N')
#     )

#     point2 = alt.Chart(source2).mark_point().encode(
#         x=alt.X('Date:N', scale=alt.Scale(padding=15), title='월별 추세'),
#         y=alt.Y('실패', title='발생 건수'),
#         # color=alt.Color('실패:N')
#     )    
    
#     line = alt.Chart(source).mark_line(color="red").encode(
#         x=alt.X('Date:N', title='월별 추세'),
#         y=alt.Y('합계', title='발생 건수')
#     )

#     text = point.mark_text(
#         size=12,
#         align='center',
#         baseline='line-top',
#         color='black',
#         dy=-20,
#         fontSize=12,
#     ).encode(
#         text = '성공:Q'
#     )
    
#     text2 = point2.mark_text(
#         size=12,
#         align='center',
#         baseline='line-top',
#         color='black',
#         dy=-20,
#         fontSize=12,
#     ).encode(
#         text = '실패:Q'       
#     )
    
#     text3 = line.mark_text(
#         size=12,
#         align='center',
#         baseline='line-top',
#         color='black',
#         dy=-20,
#         fontSize=12,
#     ).encode(
#         text = '합계:Q'       
#     )

#     chart = (point + point2 + line + text + text2 + text3).properties(width=360, height=200)
#     return chart


def getScatterChart(timeslot, month):
    
    # Brush for selection
    brush = alt.selection(type='interval')

    # Scatter Plot
    source = timeslot
    points = alt.Chart(source).mark_point().encode(
        x=alt.X('일:Q', scale=alt.Scale(padding=15), title='장애 발생 일'),
        y=alt.Y('장애인지:Q', title='장애인지 소요시간(분)'),
        color=alt.Color('리전:N')
    ).add_selection(brush)

    points

    # Base chart for data tables
    ranked_text = alt.Chart(source).mark_text(align='right').encode(
        y=alt.Y('row_number:O',axis=None)
    ).transform_filter(
        brush
    )
    
    #.transform_window(
    #    row_number='row_number()'
    #).transform_filter(
    #    'datum.row_number < 15'
    #)

    
    #chart = points + ranked_text
    chart = (points).properties(width=360, height=200)

    return chart

def getBarChart4s(source, month):
    
    bar = alt.Chart(source).mark_bar().encode(
        x=alt.X('라이선스 종류:N', title=['유형별 라이선스 수']),
        y=alt.Y('count(라이선스 종류)', title=''),
        color=alt.Color("유형:N", legend=None)
    )
    text = bar.mark_text(
        align='left', # align='center',
        baseline='top', # baseline='middle',
        dx=7  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
        text='count(라이선스 종류):Q'
    )
    text2 = bar.mark_text(
        size=12,
        align='center',
        baseline='line-top',
        color='black',
        dy=-20,
        fontSize=12,
    ).encode(
        text = 'count(라이선스 종류):Q'
    )	

    chart = (bar + text + text2).properties(width=360, height=360)
    return chart



def getLineChart4s(df, month):
    source = df    
    point = alt.Chart(source).mark_point().encode(
        x=alt.X('월', scale=alt.Scale(padding=15), title='월별 추세'),
        y=alt.Y('count(라이선스 종류)', title='수량'),
        text=alt.Text("라이선스 종류:N")
    )

    line = alt.Chart(source).mark_line(color="red").encode(
        x=alt.X('월', title='월별 추세'),
        y=alt.Y('count(라이선스 종류)', title='')
    )

    text = point.mark_text(
        size=12,
        align='center',
        baseline='line-top',
        color='black',
        dy=-20,
        fontSize=12,
    ).encode(
        text = 'count(라이선스 종류):Q'
    )

    chart = (point + line + text).properties(width=360, height=200)
    return chart

def get_1_4_HBarChart(source):
    bar = alt.Chart(source).mark_bar().encode(
        x=alt.X('count(작업유형):Q', stack='zero', title=''),         
        # y=alt.Y('진행상태:O', sort='ascending'),  
        y=alt.Y('작업유형:O', sort='ascending'),  
        # order=alt.Order("count(리전):Q", sort='descending'),
        color=alt.Color('작업유형:N') #, legend=None)   
    )
    
    # text1 = alt.Chart(source).mark_text(dx=-20, dy=0, color='black').encode(
    text1 = alt.Chart(source).mark_text(dx=0, dy=0, color='black').encode(
        x=alt.X('count(작업유형):Q', stack='zero', sort='ascending'),        
        # y=alt.Y('진행상태:N', sort='ascending'),        
        y=alt.Y('작업유형:N', sort='ascending'),        
        detail=alt.Color("작업유형:N"),
        text = alt.Text('count(작업유형):Q', format='d') #, sort='descending')
    )
    
    # text2 = alt.Chart(source).mark_text(dx=10, dy=-3, color='black').encode(
    text2 = alt.Chart(source).mark_text(dx=10, dy=-3, color='black').encode(
        x=alt.X('count(작업유형):Q', stack='zero', title=''),         
        # y=alt.Y('진행상태:N'),        
        y=alt.Y('작업유형:N'),        
        # order=alt.Order("count(리전):Q", sort='descending'),
        # color=alt.Color('리전:N'), # legend=None)   
        text = alt.Text('count(작업유형):Q', format='d')
        # text = alt.Text('sum(count):Q', format='d')        
    ) 
    
    # chart = (bar + text1 + text2).properties(width=360, height=360)
    chart = (bar + text2).properties(width=360, height=360)
    return chart

def get_1_5_HBarChart(source):
    bar = alt.Chart(source).mark_bar().encode(
        x=alt.X('count(Work Type):Q', stack='zero', title=''),         
        # y=alt.Y('진행상태:O', sort='ascending'),  
        y=alt.Y('Work Type:O', sort='ascending'),  
        # order=alt.Order("count(리전):Q", sort='descending'),
        color=alt.Color('Work Type:N') #, legend=None)   
    )
    
    # text1 = alt.Chart(source).mark_text(dx=-20, dy=0, color='black').encode(
    text1 = alt.Chart(source).mark_text(dx=0, dy=0, color='black').encode(
        x=alt.X('count(Work Type):Q', stack='zero', sort='ascending'),        
        # y=alt.Y('진행상태:N', sort='ascending'),        
        y=alt.Y('Work Type:N', sort='ascending'),        
        detail=alt.Color("Work Type:N"),
        text = alt.Text('count(Work Type):Q', format='d') #, sort='descending')
    )
    
    # text2 = alt.Chart(source).mark_text(dx=10, dy=-3, color='black').encode(
    text2 = alt.Chart(source).mark_text(dx=10, dy=-3, color='black').encode(
        x=alt.X('count(Work Type):Q', stack='zero', title=''),         
        # y=alt.Y('진행상태:N'),        
        y=alt.Y('Work Type:N'),        
        # order=alt.Order("count(리전):Q", sort='descending'),
        # color=alt.Color('리전:N'), # legend=None)   
        text = alt.Text('count(Work Type):Q', format='d')
        # text = alt.Text('sum(count):Q', format='d')        
    ) 
    
    # chart = (bar + text1 + text2).properties(width=360, height=360)
    chart = (bar + text2).properties(width=360, height=360)
    return chart



def get_1_5_StackedHBarChart(source):
    bar = alt.Chart(source).mark_bar().encode(
        x=alt.X('count(리전):Q', stack='zero', title=''),         
        y=alt.Y('Work Type:O', sort='ascending'),  
        # order=alt.Order("count(리전):Q", sort='descending'),
        color=alt.Color('리전:N') #, legend=None)   
    )
    
    text1 = alt.Chart(source).mark_text(dx=-20, dy=0, color='black').encode(
        x=alt.X('count(리전):Q', stack='zero', sort='ascending'),        
        y=alt.Y('Work Type:N', sort='ascending'),        
        detail=alt.Color("리전:N"),
        text = alt.Text('count(리전):Q', format='d') #, sort='descending')
    )
    
    text2 = alt.Chart(source).mark_text(dx=10, dy=-3, color='black').encode(
        x=alt.X('count(리전):Q', stack='zero', title=''),         
        y=alt.Y('Work Type:N'),        
        # order=alt.Order("count(리전):Q", sort='descending'),
        # color=alt.Color('리전:N'), # legend=None)   
        text = alt.Text('count(리전):Q', format='d')
        # text = alt.Text('sum(count):Q', format='d')        
    ) 
    
    chart = (bar + text1 + text2).properties(width=360, height=360)
    return chart




def get_1_11_HBarChart(source):
    bar = alt.Chart(source).mark_bar().encode(
        x=alt.X('count(라이선스 종류):Q', stack='zero', title=''),         
        # y=alt.Y('진행상태:O', sort='ascending'),  
        y=alt.Y('라이선스 종류:O', sort='ascending'),  
        # order=alt.Order("count(리전):Q", sort='descending'),
        color=alt.Color('라이선스 종류:N') #, legend=None)   
    )
    
    # text1 = alt.Chart(source).mark_text(dx=-20, dy=0, color='black').encode(
    text1 = alt.Chart(source).mark_text(dx=0, dy=0, color='black').encode(
        x=alt.X('count(라이선스 종류):Q', stack='zero', sort='ascending'),        
        # y=alt.Y('진행상태:N', sort='ascending'),        
        y=alt.Y('라이선스 종류:N', sort='ascending'),        
        detail=alt.Color("라이선스 종류:N"),
        text = alt.Text('count(라이선스 종류):Q', format='d') #, sort='descending')
    )
    
    # text2 = alt.Chart(source).mark_text(dx=10, dy=-3, color='black').encode(
    text2 = alt.Chart(source).mark_text(dx=10, dy=-3, color='black').encode(
        x=alt.X('count(라이선스 종류):Q', stack='zero', title=''),         
        # y=alt.Y('진행상태:N'),        
        y=alt.Y('라이선스 종류:N'),        
        # order=alt.Order("count(리전):Q", sort='descending'),
        # color=alt.Color('리전:N'), # legend=None)   
        text = alt.Text('count(라이선스 종류):Q', format='d')
        # text = alt.Text('sum(count):Q', format='d')        
    ) 
    
    # chart = (bar + text1 + text2).properties(width=360, height=360)
    chart = (bar + text2).properties(width=360, height=360)
    return chart



def getStacked_1_11_VBarChart1(source):
    bar = alt.Chart(source).mark_bar().encode(
        x=alt.X('Date:N', stack='zero', title=''),
        # y=alt.Y('sum(count):Q'),
        # y=alt.Y('count(Date):Q'),
        y=alt.Y('count(Date):Q'),
        color=alt.Color("유형:N", sort='descending') #sort='descending') #, legend=None)   
    )
    line = alt.Chart(source).mark_line(color="red").encode(
        x=alt.X('Date:N', title=''),
        y=alt.Y('count(Date):Q', title='월별 추세'),
        # y=alt.Y('count(Date):Q', title='월별 추세')
        # y=alt.Y('sum(count):Q', title='월별 추세')
    )
    text1 = alt.Chart(source).mark_text(dx=-20, dy=0, color='black').encode(
        x=alt.X('Date:N'),        
        y=alt.Y('count(Date):Q', stack='zero'),
        # y=alt.Y('sum(count):Q', stack='zero'),     
        # y=alt.Y('count(Date):Q', stack='zero'),     
        detail=alt.Color("유형:N"),
        # text = alt.Text('sum(count):Q', format='d')
        # text = alt.Text('count(Date):Q', format='d')
        text = alt.Text('count(Date):Q', format='d')
    )
    text2 = line.mark_text(dx=0, dy=-15, color='red').encode(
        x=alt.X('Date:N'),
        y=alt.Y('count(Date):Q'),
        # y=alt.Y('sum(count):Q'),
        # y=alt.Y('count(Date):Q'),
        # text = alt.Text('sum(count):Q', format='d')
        text = alt.Text('count(Date):Q', format='d')
    )        
    chart = (bar + line + text1 + text2).properties(width=360, height=360)
    # chart = (bar + line +  text2).properties(width=360, height=360)
    return chart    


def getStacked_1_11_VBarChart2(source):
    bar = alt.Chart(source).mark_bar().encode(
        x=alt.X('Date:N', stack='zero', title=''),
        y=alt.Y('count(Date):Q'),
        # y=alt.Y('sum(count):Q'),
        # y=alt.Y('count(Date):Q'),
        color=alt.Color("공급사:N") #, legend=None)   
    )
    line = alt.Chart(source).mark_line(color="red").encode(
        x=alt.X('Date:N', title=''),
        y=alt.Y('count(Date):Q', title='월별 추세')
        # y=alt.Y('count(Date):Q', title='월별 추세')
        # y=alt.Y('sum(count):Q', title='월별 추세')
    )
    text1 = alt.Chart(source).mark_text(dx=-20, dy=0, color='black').encode(
        x=alt.X('Date:N'),        
        y=alt.Y('count(Date):Q', stack='zero'),
        # y=alt.Y('sum(count):Q', stack='zero'),     
        # y=alt.Y('count(Date):Q', stack='zero'),     
        detail=alt.Color("공급사:N"),
        text = alt.Text('count(Date):Q', format='d')
        # text = alt.Text('sum(count):Q', format='d')
        # text = alt.Text('count(Date):Q', format='d')
    )
    text2 = line.mark_text(dx=0, dy=-15, color='red').encode(
        x=alt.X('Date:N'),        
        y=alt.Y('count(Date):Q'),
        # y=alt.Y('sum(count):Q'),
        # y=alt.Y('count(Date):Q'),
        # text = alt.Text('sum(count):Q', format='d')
        # text = alt.Text('count(Date):Q', format='d')
        text = alt.Text('count(Date):Q', format='d')
    )        
    chart = (bar + line + text1 + text2).properties(width=360, height=360)
    # chart = (bar + line +  text2).properties(width=360, height=360)
    return chart   


def getScatterChart2(timeslot, month):
    
    # Brush for selection
    brush = alt.selection(type='interval')

    # Scatter Plot
    source = timeslot
    points = alt.Chart(source).mark_point().encode(
        x=alt.X('일:Q', scale=alt.Scale(padding=15), title='장애 발생 일'),
        y=alt.Y('장애전파:Q', title='장애전파 소요시간(분)'),
        color=alt.Color('리전:N')
    ).add_selection(brush)

    points

    # Base chart for data tables
    ranked_text = alt.Chart(source).mark_text(align='right').encode(
        y=alt.Y('row_number:O',axis=None)
    ).transform_filter(
        brush
    )
    
    #.transform_window(
    #    row_number='row_number()'
    #).transform_filter(
    #    'datum.row_number < 15'
    #)

    
    #chart = points + ranked_text
    chart = (points).properties(width=360, height=200)

    return chart

