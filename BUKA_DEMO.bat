@echo off
setlocal
cd /d "%~dp0"
title CCTV VISION SIMAPRES WONOGIRI - DEMO SIMULASI
set "PY=%~dp0.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=%USERPROFILE%\Folder Baru\Downloads\CCTV_Vision_Wonogiri_Prototipe_Simapres_2026\CCTV_Vision_Wonogiri\.venv\Scripts\python.exe"
if not exist "%PY%" set "PY=%~dp0.venv\Scripts\python.exe"
if not exist "%PY%" (
  set "PY=%~dp0.venv\Scripts\python.exe"
  echo Python environment lama tidak ditemukan; menyiapkan lingkungan baru...
  py -3.11 -m venv "%~dp0.venv"
  if errorlevel 1 goto error
)
if not exist "%PY%" goto error
"%PY%" -c "import streamlit, cv2, numpy" >nul 2>&1
if errorlevel 1 (
  echo Memasang modul ringan. Diperlukan internet hanya saat instalasi pertama...
  "%PY%" -m pip install -r "%~dp0requirements.txt"
  if errorlevel 1 goto error
)
echo.
echo Aplikasi simulasi akan dibuka di http://localhost:8502
echo Biarkan terminal ini terbuka selama aplikasi digunakan.
echo.
"%PY%" -m streamlit run "%~dp0app.py" --server.port 8502 --server.address 127.0.0.1 --server.headless false
if errorlevel 1 goto error
exit /b 0
:error
echo.
echo Terjadi kegagalan. Kirim foto isi terminal ini kepada ChatGPT.
pause
exit /b 1
