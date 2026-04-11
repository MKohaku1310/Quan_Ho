@echo off
title Quan Ho Bac Ninh - System Launcher
setlocal enabledelayedexpansion

echo ======================================================
echo    QUAN HO BAC NINH - HE THONG KHOI DONG
echo ======================================================

echo.
echo [1/3] Dang don dẹp cac tien trinh cu...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
    taskkill /f /pid %%a >nul 2>&1
)
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8080') do (
    taskkill /f /pid %%a >nul 2>&1
)
timeout /t 1 /nobreak >nul

echo [2/3] Dang khoi dong Backend (FastAPI)...
:: Check if .env exists, if not warn
if not exist "backend\.env" (
    echo WARNING: backend\.env khong ton tai. Su dung cau hinh mac dinh.
)
start "Quan Ho - Backend" cmd /k "cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

echo [3/3] Dang khoi dong Frontend (NiceGUI)...
timeout /t 3 /nobreak >nul
start "Quan Ho - Frontend" cmd /k "cd frontend_py && python main.py"

echo.
echo ======================================================
echo    HE THONG DA BAT DAU THANH CONG!
echo ======================================================
echo.
echo  - UI:  http://localhost:8080
echo  - API: http://localhost:8000/docs
echo.
echo  Neu bi loi 500, hay chay file 'debug_connectivity.py'
echo  hoac kiem tra cua so Backend de xem chi tiet loi.
echo.
echo ======================================================
pause

