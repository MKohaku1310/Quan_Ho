@echo off
echo Dang kiem tra moi truong...

:: Neu chua co venv thi tu dong tao va cai dat
if not exist venv (
    echo Dang tao moi truong ao (venv)...
    python -m venv venv
    call venv\Scripts\activate
    echo Dang cai dat cac thu vien can thiet...
    pip install -r requirements.txt
)

echo Dang khoi dong ung dung Quan Ho Bac Ninh...
start cmd /c "call venv\Scripts\activate && cd backend && python -m uvicorn app.main:app --port 8000"
start cmd /c "call venv\Scripts\activate && cd frontend && python main.py"

echo.
echo He thong dang chay tai: http://localhost:8080
echo Tai lieu API: http://localhost:8000/docs
pause
