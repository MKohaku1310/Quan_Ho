from nicegui import app, ui
import os

# Import các trang để đăng ký route
from pages import (
    home, introduction, songs, artists, villages, news, chatbot, 
    auth, profile
)
from pages.admin import (
    hub, editor, accounts, melodies, artists as admin_artists, 
    news as admin_news, villages as admin_villages, 
    comments, registrations
)

# ---------------------------------------------------------------------------
# Phục vụ file tĩnh
# ---------------------------------------------------------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
app.add_static_files('/static', os.path.join(current_dir, 'static'))

# ---------------------------------------------------------------------------
# Trạng thái ban đầu
# ---------------------------------------------------------------------------
@app.on_connect
def init_user_state():
    if 'language' not in app.storage.user:
        app.storage.user['language'] = 'vi'

# ---------------------------------------------------------------------------
# Xử lý lỗi
# ---------------------------------------------------------------------------
@app.on_exception
def handle_exception(e):
    # Ghi log lỗi nhưng ngăn server bị crash hoặc hiển thị lỗi 500 thô
    print(f"FRONTEND ERROR: {e}")
    # Bạn cũng có thể dùng ui.notify ở đây nếu context cho phép
    # ui.notify('Đã xảy ra lỗi, vui lòng kiểm tra kết nối server.', type='negative')

# ---------------------------------------------------------------------------
# Điểm khởi chạy
# ---------------------------------------------------------------------------
if __name__ in {'__main__', '__mp_main__'}:
    ui.run(
        title='Quan Họ Bắc Ninh - Di sản văn hóa',
        storage_secret='quanho_secret',
        port=8080,
        favicon=os.path.join(current_dir, 'static', 'common', 'favicon.png'),
        reload=True,
        uvicorn_reload_dirs=current_dir, # Theo dõi frontend_py đệ quy
        uvicorn_logging_level='info'
    )