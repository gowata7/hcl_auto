import shutil
from datetime import datetime, timedelta
import pandas as pd
import warnings
import os
warnings.filterwarnings('ignore')

from chart_portal import *
from table_portal import *
from docx.text.run import *
from docx.enum.text import WD_ALIGN_PARAGRAPH

# DRM 방지(default.docx)
def findfile(name, path):
    for dirpath, dirname, filename in os.walk(path):
        if name in filename:
            return os.path.join(dirpath, name)

file_path=os.path.abspath("")
srcpath = findfile("default.docx.org", file_path)
dir, file = os.path.split(srcpath)
shutil.copy2(srcpath, dir+"\default.docx")

from document_portal import *

# Document 기본 폰트
style = document.styles['Normal']
# style.font.name = '맑은고딕'
style.font.name = 'Calibri'
style.font.size = Pt(12)
# style._element.rPr.rFonts.set(qn('w:eastAsia'), '맑은고딕')
style._element.rPr.rFonts.set(qn('w:eastAsia'), 'Calibri')

# Chart 기본 폰트
alt.themes.register('맑은고딕', hanfont)
alt.themes.enable('맑은고딕')