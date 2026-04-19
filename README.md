# Hệ thống thông tin Quan Họ Bắc Ninh

Đây là dự án quản lý và giới thiệu di sản văn hóa phi vật thể Quan họ Bắc Ninh. Ứng dụng được xây dựng với giao diện hiện đại, hỗ trợ tra cứu làn điệu, nghệ nhân, làng nghề và trợ lý ảo chatbot.

## Các thành phần chính
- Backend: FastAPI (Python)
- Frontend: NiceGUI (Python)
- Cơ sở dữ liệu: SQLite (Đã có sẵn dữ liệu đi kèm)

## Hướng dẫn cài đặt và khởi chạy (Dành cho máy mới)

1. Yêu cầu: Máy tính cần cài đặt sẵn Python (phiên bản 3.10 trở lên).

2. Cách chạy nhanh nhất:
   - Bạn chỉ cần nhấp đúp chuột vào file `run.bat`.
   - File này sẽ tự động kiểm tra, nếu máy bạn chưa có môi trường ảo (venv), nó sẽ tự động tạo và tải các thư viện cần thiết (mất khoảng 1-2 phút cho lần đầu tiên).

3. Cách chạy thủ công (Nếu không muốn dùng file .bat):
   - Mở cửa sổ lệnh (Terminal/CMD) tại thư mục dự án.
   - Tạo môi trường ảo: `python -m venv venv`
   - Kích hoạt môi trường: `venv\Scripts\activate`
   - Cài đặt thư viện: `pip install -r requirements.txt`
   - Chạy backend: `cd backend && python -m uvicorn app.main:app --port 8000`
   - Chạy frontend: `cd frontend && python main.py`

## Thông tin truy cập
- Địa chỉ trang web: http://localhost:8080
- Trang quản trị: http://localhost:8080/admin
- Tài liệu API: http://localhost:8000/docs

## Tài khoản Admin mặc định
- Email: admin@example.com
- Mật khẩu: admin123

Lưu ý: Để sử dụng tính năng Chatbot AI, bạn cần điền GEMINI_API_KEY vào file .env trong thư mục backend (sao chép từ .env.example).
