@echo off
call C:\work\jinhong\jinhongenv\Scripts\activate.bat

timeout /t 10

(start python EUcapture.py) | pause

(start python pdf_mail_process.py "EU")  | pause

timeout /t 300

call kill_ChromeD.bat