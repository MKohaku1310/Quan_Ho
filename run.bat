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

:: Start Backend
echo [+] Dang bat Backend...
start "Quan Ho - Backend" cmd /c "call venv\Scripts\activate && cd backend && python -m uvicorn app.main:app --port 8000"

:: Start Frontend
echo [+] Dang bat Frontend...
start "Quan Ho - Frontend" cmd /c "call venv\Scripts\activate && cd frontend && python main.py"

echo.
echo ==========================================
echo   UNG DUNG DANG CHAY TAI:
echo   - Frontend: http://localhost:8080
echo   - Backend API: http://localhost:8000/docs
echo ==========================================
echo.
pause
