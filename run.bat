@echo off
title Quan Ho Bac Ninh
echo Dang khoi dong...

:: Start Backend
start cmd /k "cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

:: Wait for backend
timeout /t 3 /nobreak >nul

:: Start Frontend
start cmd /k "cd frontend_py && python main.py"

echo Bat dau thanh cong.
echo UI: http://localhost:8080
echo API: http://localhost:8000/docs
pause
