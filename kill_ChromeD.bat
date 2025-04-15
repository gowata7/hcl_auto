@echo off
SETLOCAL enabledelayedexpansion
SET count=1
for /f "tokens=2 delims= " %%a IN ('tasklist ^| findstr chromedriver.exe') do (    
    set var!count!= %%a;
    set /a count=!count!+1;
    echo !count!
    taskkill /F /PID %%a
)
SET count=1
for /f "tokens=2 delims= " %%a IN ('tasklist ^| findstr python.exe') do (    
    set var!count!= %%a;
    set /a count=!count!+1;
    echo !count!
    taskkill /F /PID %%a
)
SET count=1
for /f "tokens=2 delims= " %%a IN ('tasklist ^| findstr chrome.exe') do (    
    set var!count!= %%a;
    set /a count=!count!+1;
    echo !count!
    taskkill /F /PID %%a
)
