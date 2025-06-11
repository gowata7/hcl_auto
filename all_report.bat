@echo off
call C:\Beomjun\venv\Scripts\activate.bat

rasdial KR2 spark tmvkzm1!
rasdial EU2-FR2 spark tmvkzm1!

timeout /t 10

(start python vm_lb_1.py) | pause
(start python volume_2.py) | pause
(start python capture_3.py) | pause
(start python proxmox_4.py) | pause

timeout /t 100

(start python pdf_mail_process.py "EU")  | pause

timeout /t 10

cd /d C:\Beomjun\db
(start python vm_inject.py) | pause

@REM # rasdial "KR2-ADMIN" /DISCONNECT

@REM # timeout /t 300

@REM # call kill_ChromeD.bat