@echo off
echo [+] Dang khoi dong he thong Quan Ho Bac Ninh...
start cmd /c "call venv\Scripts\activate && cd backend && python -m uvicorn app.main:app --port 8000"
start cmd /c "call venv\Scripts\activate && cd frontend && python main.py"
echo [OK] Ung dung dang chay tai http://localhost:8080
pause
