from nicegui import app, ui
import theme
import components
from api import api_client
import asyncio

@ui.page('/dang-ky')
def register_page():
    with theme.frame():
        with ui.element('section').classes('py-24 bg-background w-full flex justify-center'):
            with ui.card().classes('w-full max-w-md p-8 rounded-2xl shadow-elevated border border-border bg-card'):
                ui.label('Tạo tài khoản').classes('font-display text-3xl font-bold text-center mb-6')
                with ui.column().classes('gap-4 w-full'):
                    name = ui.input('Họ và tên').classes('w-full').props('outlined')
                    email = ui.input('Email').classes('w-full').props('outlined type=email')
                    password = ui.input('Mật khẩu').classes('w-full').props('outlined type=password')
                    
                    async def handle_register():
                        if not all([name.value, email.value, password.value]):
                            ui.notify('Vui lòng điền đầy đủ thông tin', type='warning')
                            return
                        if await api_client.register(name.value, email.value, password.value):
                            ui.notify('Đăng ký thành công!', type='positive')
                            ui.navigate.to('/dang-nhap')
                        else:
                            ui.notify('Đăng ký thất bại', type='negative')
                            
                    ui.button('Đăng ký', on_click=handle_register).props('unelevated rounded-lg').classes('w-full bg-primary text-white font-bold py-3 mt-2')
                    ui.link('Đã có tài khoản? Đăng nhập ngay', '/dang-nhap').classes('text-sm text-center w-full text-muted-foreground')

@ui.page('/dang-nhap')
def login_page():
    with theme.frame():
        with ui.element('section').classes('py-24 bg-background w-full flex justify-center'):
            with ui.card().classes('w-full max-w-md p-8 rounded-2xl shadow-elevated border border-border bg-card'):
                ui.label('Đăng nhập').classes('font-display text-3xl font-bold text-center mb-6')
                with ui.column().classes('gap-4 w-full'):
                    email = ui.input('Email').classes('w-full').props('outlined type=email')
                    password = ui.input('Mật khẩu').classes('w-full').props('outlined type=password')
                    
                    async def handle_login():
                        if await api_client.login(email.value, password.value):
                            ui.notify('Chào mừng bạn quay lại!', type='positive')
                            ui.navigate.to('/')
                        else:
                            ui.notify('Sai thông tin đăng nhập', type='negative')
                            
                    ui.button('Đăng nhập', on_click=handle_login).props('unelevated rounded-lg').classes('w-full bg-primary text-white font-bold py-3 mt-2')
                    ui.link('Chưa có tài khoản? Đăng ký ngay', '/dang-ky').classes('text-sm text-center w-full text-muted-foreground')

@ui.page('/ho-so')
def profile_page():
    if not app.storage.user.get('is_authenticated'):
        ui.navigate.to('/dang-nhap')
        return
        
    with theme.frame():
        with ui.element('section').classes('py-16 bg-background w-full'):
            with theme.container().classes('max-w-4xl'):
                ui.label('Hồ sơ cá nhân').classes('font-display text-3xl font-bold text-foreground mb-8')
                with ui.row().classes('gap-8 w-full flex-col md:flex-row'):
                    with ui.column().classes('w-full md:w-1/3 gap-4'):
                        with ui.card().classes('w-full p-6 text-center items-center'):
                            ui.image('/static/chatbot-avatar.png').classes('w-24 h-24 rounded-full border-4 border-muted mx-auto')
                            role = app.storage.user.get('role', 'user')
                            ui.label(app.storage.user.get('name', 'Người dùng')).classes('font-display text-xl font-bold mt-4')
                            ui.label(f'Vai trò: {role.upper()}').classes('text-xs font-bold text-primary')
                            ui.button('Đăng xuất', icon='logout', on_click=lambda: (app.storage.user.clear(), ui.navigate.to('/'))).props('flat').classes('text-destructive w-full mt-4')
                    with ui.column().classes('w-full md:w-2/3'):
                        with ui.card().classes('w-full p-6'):
                            ui.label('Thông tin tài khoản').classes('font-bold mb-4 border-b pb-2')
                            ui.label(f"Email: {app.storage.user.get('email', 'N/A')}")
                            ui.label(f"ID: {app.storage.user.get('id', 'N/A')}")
