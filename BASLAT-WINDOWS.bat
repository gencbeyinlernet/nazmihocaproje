@echo off
cd /d "%~dp0"
where py >nul 2>&1
if %errorlevel% equ 0 (
    py -3 "%~dp0BASLAT.py"
    goto :end
)
where python >nul 2>&1
if %errorlevel% equ 0 (
    python "%~dp0BASLAT.py"
    goto :end
)
echo Python 3 bulunamadi. Python kurulumundan sonra bu dosyayi yeniden acin.
:end
pause
