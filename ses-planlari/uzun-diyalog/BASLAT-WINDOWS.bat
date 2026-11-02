@echo off
chcp 65001 >nul
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
 py -3 SESLENDIR.py
) else (
 python SESLENDIR.py
)
if errorlevel 1 (
 echo Python 3.9 veya daha yeni bir surum gerekiyor.
 pause
)
