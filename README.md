# Quan Họ Bắc Ninh - Digital Heritage Platform

Nền tảng kỹ thuật số giúp bảo tồn và phát huy giá trị văn hóa Dân ca Quan họ Bắc Ninh.

## Tính năng chính
- Khám phá 49 làng Quan họ gốc.
- Thư viện bài hát với lời ca và thông tin nghệ nhân.
- Tin tức và sự kiện mới nhất về văn hóa Quan họ.
- Hệ thống quản lý người dùng và cộng đồng.

## Công nghệ sử dụng
- **Backend**: FastAPI, SQLAlchemy, MySQL, Pydantic v2.
- **Frontend**: React (Vite), Tailwind CSS, Shadcn UI, TanStack Query.

## Hướng dẫn cài đặt

### Backend
1. Cài đặt Python 3.10+.
2. Tạo môi trường ảo: `python -m venv venv`.
3. Cài đặt thư viện: `pip install -r requirements.txt`.
4. Cấu hình `.env` với `DATABASE_URL`.
5. Chạy seed dữ liệu: `python seed.py`.
6. Khởi chạy: `uvicorn app.main:app --reload`.

### Frontend
1. Cài đặt Node.js.
2. Cài đặt dependencies: `npm install`.
3. Khởi chạy: `npm run dev`.
