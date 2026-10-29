@echo off
chcp 65001 >nul
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 -m venv .ses-ortami
) else (
  python -m venv .ses-ortami
)
if errorlevel 1 goto hata
.ses-ortami\Scripts\python.exe -m pip install edge-tts==7.3.1
if errorlevel 1 goto hata
.ses-ortami\Scripts\python.exe URET.py
if errorlevel 1 goto hata
echo.
echo yeni-kadin-sesleri.zip dosyasini sohbete yukleyebilirsiniz.
pause
exit /b 0
:hata
echo.
echo Islem tamamlanamadi. Python 3.9 veya daha yeni bir surum ve internet baglantisi gerekiyor.
echo Yukaridaki hata mesajini bizimle paylasabilirsiniz.
pause
exit /b 1
