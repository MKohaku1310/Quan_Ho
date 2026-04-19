@echo off
if not exist venv (
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)

start cmd /c "call venv\Scripts\activate && cd backend && python -m uvicorn app.main:app --port 8000"
start cmd /c "call venv\Scripts\activate && cd frontend && python main.py"

echo He thong dang chay tai: http://localhost:8080
pause
