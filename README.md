# 🌸 Hệ thống Thông tin Quan Họ Bắc Ninh 🌸

![Quan Ho Heritage](https://images.unsplash.com/photo-1599908608021-b5d929aa054e?auto=format&fit=crop&q=80&w=1200)

Chào mừng bạn đến với hệ thống bảo tồn và giới thiệu **Dân ca Quan họ Bắc Ninh** — Di sản Văn hóa Phi vật thể đại diện của Nhân loại (UNESCO 2009). Đây là một nền tảng hiện đại được thiết kế với phong cách **"Studio Aesthetic"**, kết hợp giữa nét truyền thống Kinh Bắc và trải nghiệm người dùng cao cấp.

---

## 🌟 Tính năng nổi bật

- **Trải nghiệm Premium:** Giao diện Glassmorphism mượt mà, đậm chất văn hóa.
- **Thư viện Làn điệu:** Tra cứu hàng trăm bài hát Quan họ cổ và mới.
- **Danh nhân & Địa danh:** Khám phá 49 làng Quan họ gốc và các nghệ nhân tiêu biểu.
- **Trợ lý Ảo (Chatbot):** Tương tác cùng "Liền Anh/Liền Chị" ảo để tìm hiểu về di sản.
- **Hệ thống Quản trị:** Quản lý nội dung, sự kiện và tài khoản dễ dàng.

---

## 🛠️ Hướng dẫn cài đặt & Khởi chạy (100% Chạy được)

Dự án này được thiết kế để có thể chạy ngay lập tức sau khi tải về. Hãy làm theo các bước sau:

### 1. Yêu cầu hệ thống
- **Python 3.10+** (Khuyến nghị 3.11)
- Windows OS (Để chạy file `.bat`)

### 2. Thiết lập môi trường
Mở terminal (CMD/PowerShell) tại thư mục gốc và chạy:
```bash
# Tạo môi trường ảo
python -m venv venv

# Kích hoạt và cài đặt thư viện
call venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Cấu hình AI (Tùy chọn cho Chatbot)
Sao chép file `.env.example` trong thư mục `backend` thành `.env` và điền **GEMINI_API_KEY** của bạn để kích hoạt Chatbot AI.

### 4. Khởi chạy hệ thống
Bạn chỉ cần nhấp đúp vào file:
👉 **`run.bat`**

Hệ thống sẽ tự động khởi động cả Backend (FastAPI) và Frontend (NiceGUI).
- **Trang chủ:** `http://localhost:8080`
- **API Docs:** `http://localhost:8000/docs`

---

## 📂 Cấu trúc thư mục

```text
Quan_Ho/
├── backend/            # API Server (FastAPI + SQLAlchemy)
│   ├── app/            # Logic xử lý chính
│   └── quan_ho.db      # Cơ sở dữ liệu đã pre-seeded
├── frontend/           # Giao diện người dùng (NiceGUI)
│   ├── components/     # Các thành phần giao diện Studio
│   └── pages/          # Các trang nội dung
├── run.bat             # File khởi chạy nhanh
└── requirements.txt    # Danh sách thư viện
```

---

## 👤 Tài khoản thử nghiệm (Admin)
- **Email:** `admin@example.com`
- **Mật khẩu:** `admin123`

---

## 📝 Giấy phép & Bản quyền
Dự án được phát triển nhằm mục đích giáo dục và bảo tồn văn hóa. 
**© 2024 Quan Họ Bắc Ninh Heritage.**
