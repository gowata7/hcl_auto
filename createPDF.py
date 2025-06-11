from io import BytesIO
# from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2 import PdfWriter, PdfReader
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
        "EU": {
            "sentence_h1": [
                'EU Hcloud Storage 일일 사용량',
            ],
            "sentence_h2": [
                '',
            ],
            "sentence_h3": [
                'https://hubble-euce.platform.hcloud.io/grafana/d/dongheon-euce/netapp-euce-summary?from=now-3h&orgId=41&to=now&viewPanel=2',
            ]
        },
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


    
    if region == 'EU':
        common_filenames = [
            "01_%s_Hcloud_Storage_*.png",
    ]
        
    # elif region == 'EU':
    #     common_filenames = [
    #     '01_%s_lb(a10)_*.png',
    #     '02_%s_fw_1_*.png',
    #     '03_%s_total_1_*.png',
    #     '04_%s_host_1_*.png',
    #     '05_%s_vm_1_*.png',
    #     '06_%s_database_1_*.png',
    #     '07_%s_mongo_*.png',
    #     '08_%s_netapp_info_*.png',
    #     '09_%s_storage_1_*.png',
    #     '10_%s_cluster_info_1_*.png',
    #     '11_%s_cluster_info_2_*.png',
    #     '12_%s_cluster_info_3_*.png',
    #     '13_%s_cluster_info_4_*.png'
    # ]


       
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

    pdf = PdfWriter()

    inch = 72
                    
    for i, file in enumerate(filelist_recently):  # for each slide
        # Using ReportLab Canvas to insert image into PDF
        
        imgTemp = BytesIO()
        imgDoc = canvas.Canvas(imgTemp, pagesize=(11 * inch, 8.5 * inch))
        fontname = 'C:\\Windows\\Fonts\\Malgun.ttf'
        pdfmetrics.registerFont(TTFont("Malgun", fontname))

        # Draw image on Canvas and save PDF in buffer
        print(file)
        Words = file.split(".")[0].split("\\")
        Title = Words[1]
        imgDoc.setFont('Malgun', 14)
        imgDoc.drawString(20, 580, Title)
        imgDoc.setFont('Malgun', 12)
        imgDoc.drawString(20, 560, sentence_h1[i])
        imgDoc.drawString(20, 540, sentence_h2[i])
        imgDoc.drawString(20, 520, sentence_h3[i])
        imgDoc.drawImage(file, 0, 0, width=780, height=590, preserveAspectRatio=True, mask='auto')
        imgDoc.save()
        
        # PyPDF2의 PdfWriter를 사용하여 페이지 추가
        page = PdfReader(BytesIO(imgTemp.getvalue())).pages[0]
        pdf.add_page(page)
                    
    # 파일 저장
    filename = f"{region}_Storage_in_detail_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    filename = os.path.join(pdf_path, filename)
    with open(filename, "wb") as output_pdf:
        pdf.write(output_pdf)

    print("--리포트저장성공--")