@echo off
title Quan Ho Bac Ninh - Launcher
echo ==========================================
echo    QUAN HO BAC NINH - KHOI DONG NHANH
echo ==========================================
echo.

:: Check for venv
if not exist venv (
    echo [LOI] Khong tim thay thu muc venv. 
    echo Hay chay lenh: python -m venv venv
    pause
    exit /b 1
)

:: Check for existing processes on ports 8000 and 8080
echo [+] Dang kiem tra cac cong ket noi...
netstat -ano | findstr :8000 > nul
if %errorlevel% equ 0 (
    echo [CANH BAO] Cong 8000 dang bi chiem. Dang co gang giai phong...
    for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do taskkill /f /pid %%a > nul 2>&1
)

netstat -ano | findstr :8080 > nul
if %errorlevel% equ 0 (
    echo [CANH BAO] Cong 8080 dang bi chiem. Dang co gang giai phong...
    for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8080') do taskkill /f /pid %%a > nul 2>&1
)

:: Start Backend
echo [+] Dang bat Backend...
:: Using /k instead of /c to keep the window open if an error occurs
start "Quan Ho - Backend" cmd /k "call venv\Scripts\activate && cd backend && python -m uvicorn app.main:app --port 8000"

:: Start Frontend
echo [+] Dang bat Frontend...
start "Quan Ho - Frontend" cmd /k "call venv\Scripts\activate && cd frontend && python main.py"

echo.
echo ==========================================
echo   UNG DUNG DANG CHAY TAI:
echo   - Frontend: http://localhost:8080
echo   - Backend API: http://localhost:8000/docs
echo.
echo   [Luu y] Neu cua so CMD bi loi, vui long 
echo   chup anh hoac copy loi do gui cho toi.
echo ==========================================
echo.
pause
