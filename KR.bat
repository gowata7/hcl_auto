@echo off
call C:\work\jinhong\jinhongenv\Scripts\activate.bat

rasdial KR2-ADMIN spark tmvkzm1!

timeout /t 10

(start python KRcapture.py) | pause

(start python KRJENcapture.py) | pause

(start python pdf_mail_process.py "KR")  | pause

timeout /t 10

rasdial "KR2-ADMIN" /DISCONNECT

timeout /t 300

call kill_ChromeD.bat