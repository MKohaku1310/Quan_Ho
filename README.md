# He thong thong tin Quan Ho Bac Ninh

Day la du an quan ly va gioi thieu di san van hoa phi vat the Quan ho Bac Ninh. Ung dung duoc xay dung voi giao dien hien dai, ho tro tra cuu lan dieu, nghe nhan, lang nghe va chatbot ho tro.

## Cac thanh phan chinh
- Backend: FastAPI (Python)
- Frontend: NiceGUI (Python)
- Database: SQLite (Da co san du lieu)

## Huong dan cai dat va chay (Cho may moi)

1. Yeu cau: May can cai san Python (phien ban 3.10 tro len).

2. Cach chay nhanh nhat:
   - Ban chi can click dup vao file `run.bat`.
   - File nay se tu dong kiem tra, neu may ban chua co moi truong ao (venv), no se tu tao vao tu tai cac thu vien can thiet (mat khoang 1-2 phut cho lan dau).

3. Cach chay thu cong (Neu khong muon dung file .bat):
   - Mo terminal tai thu muc du an.
   - Tao venv: `python -m venv venv`
   - Kich hoat venv: `venv\Scripts\activate`
   - Cai thu vien: `pip install -r requirements.txt`
   - Chay backend: `cd backend && python -m uvicorn app.main:app --port 8000`
   - Chay frontend: `cd frontend && python main.py`

## Thong tin truy cap
- Dia chi web: http://localhost:8080
- Trang quan tri: http://localhost:8080/admin
- Tai lieu API: http://localhost:8000/docs

## Tai khoan Admin mac dinh
- Email: admin@example.com
- Mat khau: admin123

Luu y: De su dung tinh nang Chatbot AI, ban can dien GEMINI_API_KEY vao file .env trong thu muc backend (copy tu .env.example).
