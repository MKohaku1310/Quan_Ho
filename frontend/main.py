from nicegui import app, ui
import os

# Import pages to register routes
from pages import home, introduction, songs, artists, villages, news, chatbot, auth, admin, admin_editor

# ---------------------------------------------------------------------------
# Serve static files
# ---------------------------------------------------------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
app.add_static_files('/static', os.path.join(current_dir, 'static'))


# ---------------------------------------------------------------------------
# Initial state
# ---------------------------------------------------------------------------
@app.on_connect
def init_user_state():
    if 'language' not in app.storage.user:
        app.storage.user['language'] = 'vi'

# ---------------------------------------------------------------------------
# Error Handling
# ---------------------------------------------------------------------------
@app.on_exception
def handle_exception(e):
    # Log error but prevent the server from crashing or showing a raw 500 error
    print(f"FRONTEND ERROR: {e}")
    # You could also use ui.notify here if the context allows
    # ui.notify('Đã xảy ra lỗi, vui lòng kiểm tra kết nối server.', type='negative')

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ in {'__main__', '__mp_main__'}:
    ui.run(
        title='Quan Họ Bắc Ninh - Di sản văn hóa',
        storage_secret='quanho_secret',
        port=8080,
        favicon=os.path.join(current_dir, 'static', 'common', 'favicon.png'),
        reload=True,
        uvicorn_reload_dirs=current_dir, # Watch frontend_py recursively
        uvicorn_logging_level='info'
    )