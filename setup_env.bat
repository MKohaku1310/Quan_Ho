@echo off
title Quan Ho Bac Ninh - Environment Setup
echo ======================================================
echo    QUAN HO BAC NINH - CAI DAT MOI TRUONG
echo ======================================================
echo.

echo [1/2] Dang kiem tra Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo LOI: Python chua duoc cai dat hoac chua duoc them vao PATH.
    echo Vui long cai dat Python tai https://www.python.org/
    pause
    exit /b
)

echo [2/2] Dang cai dat cac thu vien can thiet...
echo Lenh: pip install -r requirements.txt
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo LOI: Co loi xay ra trong qua trinh cai dat thu vien.
    echo Kiem tra ket noi mang va thu lai.
) else (
    echo.
    echo ======================================================
    echo    CAI DAT THANH CONG!
    echo    Bay gio ban co the chay ung dung bang 'run.bat'.
    echo ======================================================
)

echo.
pause
