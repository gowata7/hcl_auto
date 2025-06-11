@echo off
setlocal

:: 날짜 형식 YYYYMMDD 생성
for /f %%a in ('powershell -Command "Get-Date -Format yyyyMMdd"') do set TODAY=%%a

:: 가상환경 활성화
call C:\Beomjun\venv\Scripts\activate.bat

:: 로그 파일 경로 설정
set LOGFILE=C:\Beomjun\log\%TODAY%.log

echo [%TIME%] === 작업 시작 === >> %LOGFILE%

rasdial KR2 spark tmvkzm1!
rasdial EU2-FR2 spark tmvkzm1!

timeout /t 10

:: 각각의 스크립트를 백그라운드에서 병렬 실행
start "" cmd /c "python vm_lb_1.py >> %LOGFILE% 2>&1"
start "" cmd /c "python volume_2.py >> %LOGFILE% 2>&1"
start "" cmd /c "python capture_3.py >> %LOGFILE% 2>&1"
start "" cmd /c "python proxmox_4.py >> %LOGFILE% 2>&1"

:: 모두 실행된 후 멈춤
timeout /t 10
start "" cmd /c "python pdf_mail_process.py EU >> %LOGFILE% 2>&1"
pause

@REM timeout /t 100

@REM # rasdial "KR2-ADMIN" /DISCONNECT

@REM # timeout /t 300

@REM # call kill_ChromeD.bat