@echo off
echo Dang khoi dong ung dung Quan Ho Bac Ninh...
start cmd /c "call venv\Scripts\activate && cd backend && python -m uvicorn app.main:app --port 8000"
start cmd /c "call venv\Scripts\activate && cd frontend && python main.py"
echo Truy cap http://localhost:8080 de su dung.
pause
