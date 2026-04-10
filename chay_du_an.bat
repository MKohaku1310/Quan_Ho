@echo off
setlocal
title Quan Ho Bac Ninh - Project Launcher

:: ANSI Colors (Nếu CMD hỗ trợ)
set "ESC="
set "GREEN=%ESC%[92m"
set "GOLD=%ESC%[93m"
set "CYAN=%ESC%[36m"
set "RED=%ESC%[91m"
set "RESET=%ESC%[0m"

cls
echo %GOLD%======================================================%RESET%
echo %GOLD%    HE THONG QUAN HO BAC NINH - REBUILT FRONTEND    %RESET%
echo %GOLD%======================================================%RESET%
echo.

:: 1. Kiểm tra Python
echo %CYAN%[1/3] Kiem tra moi truong Python...%RESET%
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo %RED%[LOI] Khong tim thay Python. Vui long cai dat Python va add vao PATH.%RESET%
    pause
    exit /b 1
)
echo %GREEN%--- OK: Python da san sang.%RESET%
echo.

:: 2. Khởi động Backend
echo %CYAN%[2/3] Dang khoi dong Backend (FastAPI - Port 8000)...%RESET%
start "Quan Ho - Backend" cmd /k "cd backend && title Backend - FastAPI && echo Dang chay Backend... && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

:: Đợi 3 giây cho backend ổn định
timeout /t 3 /nobreak >nul

:: 3. Khởi động Frontend
echo %CYAN%[3/3] Dang khoi dong Frontend (NiceGUI - Port 8080)...%RESET%
start "Quan Ho - Frontend" cmd /k "cd frontend_py && title Frontend - NiceGUI && echo Dang chay Frontend NiceGUI... && python main.py"

echo.
echo %GREEN%======================================================%RESET%
echo %GREEN%    KHOI DONG THANH CONG!%RESET%
echo %GREEN%======================================================%RESET%
echo.
echo %GOLD%  - UI:      http://localhost:8080%RESET%
echo %GOLD%  - API:     http://localhost:8000/api/health%RESET%
echo %GOLD%  - Swagger: http://localhost:8000/docs%RESET%
echo.
echo %CYAN%Luu y:%RESET%
echo   - Neu gap loi "ModuleNotFoundError", hay chay:
echo     %GOLD%pip install -r backend/requirements.txt%RESET%
echo     %GOLD%pip install nicegui requests httpx%RESET%
echo.
echo %CYAN%Nhan phim bat ky de ket thuc trinh khoi dong...%RESET%
pause >nul
