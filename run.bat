@echo off
setlocal
echo ========================================================
echo [+] DANG KHOI DONG HE THONG QUAN HO BAC NINH...
echo ========================================================

:: Kiem tra moi truong venv
if not exist venv (
    echo [!] Khong tim thay thu muc venv. Dang tao moi...
    python -m venv venv
    call venv\Scripts\activate
    echo [+] Dang cai dat thu vien...
    pip install -r requirements.txt
)

:: Khoi dong Backend
echo [+] Dang khoi dong Backend (FastAPI)...
start "QH_BACKEND" cmd /c "call venv\Scripts\activate && cd backend && python -m uvicorn app.main:app --port 8000 --reload"

:: Doi Backend san sang
timeout /t 3 /nobreak > nul

:: Khoi dong Frontend
echo [+] Dang khoi dong Frontend (NiceGUI)...
start "QH_FRONTEND" cmd /c "call venv\Scripts\activate && cd frontend && python main.py"

echo.
echo ========================================================
echo [OK] UNG DUNG DANG CHAY TAI: http://localhost:8080
echo [OK] API DOCS TAI: http://localhost:8000/docs
echo ========================================================
echo.
pause
