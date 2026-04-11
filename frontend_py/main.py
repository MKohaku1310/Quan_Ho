from nicegui import app, ui
import os

# Import pages to register routes
from pages import home, introduction, songs, artists, villages, news, chatbot, auth

# ---------------------------------------------------------------------------
# Serve static files
# ---------------------------------------------------------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
app.add_static_files('/static', os.path.join(current_dir, 'static'))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ in {'__main__', '__mp_main__'}:
    ui.run(
        title='Quan Họ Bắc Ninh - Di sản văn hóa',
        storage_secret='quanho_secret',
        port=8080,
        favicon='static/favicon.png'
    )