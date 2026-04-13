from nicegui import app, ui
import theme
import components
from api import api_client
import asyncio
import re

# Decorators are no longer used on page functions due to FastAPI signature conflicts.
# Auth checks are performed inside page functions directly.

@ui.page('/dang-ky')
def register_page():
    if app.storage.user.get('is_authenticated'):
        ui.navigate.to('/')
        return

    with theme.frame():
        with ui.element('section').classes('py-20 md:py-32 bg-background w-full flex justify-center px-4 overflow-hidden relative'):
            # Background Decorative Elements
            ui.element('div').classes('absolute top-0 right-0 w-96 h-96 bg-primary/5 rounded-full blur-3xl -mr-48 -mt-48')
            ui.element('div').classes('absolute bottom-0 left-0 w-96 h-96 bg-secondary/5 rounded-full blur-3xl -ml-48 -mb-48')
            
            with ui.card().classes('w-full max-w-md p-0 rounded-[2.5rem] shadow-2xl border border-border bg-card/80 backdrop-blur-xl overflow-hidden'):
                with ui.row().classes('w-full g-0'):
                    # Form Side
                    with ui.column().classes('w-full p-6 sm:p-10 gap-5'):
                        with ui.column().classes('items-center w-full gap-1 mb-2'):
                            with ui.element('div').classes('h-16 w-16 rounded-3xl bg-primary/10 flex items-center justify-center text-primary mb-1 shadow-inner'):
                                ui.icon('person_add', size='2.5rem')
                            ui.label('Khởi tạo hành trình').classes('font-display text-3xl font-bold text-center tracking-tight capitalize')
                            ui.label('Tham gia cộng đồng yêu dân ca Quan họ').classes('text-muted-foreground text-sm text-center max-w-[280px]')

                        with ui.column().classes('gap-4 w-full'):
                            name = ui.input('Họ và tên').classes('w-full').props('outlined rounded-xl bg-background shadow-sm')
                            email = ui.input('Email').classes('w-full').props('outlined rounded-xl type=email bg-background shadow-sm')
                            password = ui.input('Mật khẩu').classes('w-full').props('outlined rounded-xl type=password bg-background shadow-sm')
                            confirm_pass = ui.input('Xác nhận mật khẩu').classes('w-full').props('outlined rounded-xl type=password bg-background shadow-sm')

                            async def handle_register():
                                if not all([name.value, email.value, password.value]):
                                    ui.notify('Vui lòng điền đủ thông tin', type='warning')
                                    return
                                if password.value != confirm_pass.value:
                                    ui.notify('Mật khẩu chưa khớp', type='warning')
                                    return
                                
                                reg_btn.props('loading')
                                success = await api_client.register(name.value, email.value, password.value)
                                reg_btn.props(remove='loading')
                                
                                if success:
                                    ui.notify('Đăng ký thành công! Hãy đăng nhập.', type='positive', position='top')
                                    ui.navigate.to('/dang-nhap')
                                else:
                                    ui.notify('Email đã tồn tại hoặc lỗi hệ thống', type='negative')
                                    
                            reg_btn = ui.button('Tạo tài khoản ngay', on_click=handle_register).props('unelevated rounded-xl').classes('w-full bg-primary text-white font-black py-3 mt-4 shadow-xl shadow-primary/20 hover:scale-[1.02] transition-transform text-base uppercase tracking-wider')
                            
                            with ui.row().classes('w-full justify-center gap-1.5 mt-4 text-sm'):
                                ui.label('Bạn đã có tài khoản?').classes('text-muted-foreground')
                                ui.link('Đăng nhập tại đây', '/dang-nhap').classes('text-primary font-bold hover:underline')

@ui.page('/dang-nhap')
def login_page():
    if app.storage.user.get('is_authenticated'):
        ui.navigate.to('/')
        return

    with theme.frame():
        with ui.element('section').classes('py-20 md:py-32 bg-background w-full flex justify-center px-4 overflow-hidden relative'):
            # Decorative
            ui.element('div').classes('absolute top-1/2 left-0 w-80 h-80 bg-primary/5 rounded-full blur-3xl -ml-40')
            
            with ui.card().classes('w-full max-w-md p-0 rounded-[2.5rem] shadow-2xl border border-border bg-card/80 backdrop-blur-xl overflow-hidden'):
                with ui.column().classes('w-full p-6 sm:p-10 gap-6'):
                    with ui.column().classes('items-center w-full gap-1'):
                        with ui.element('div').classes('h-16 w-16 rounded-3xl bg-primary/10 flex items-center justify-center text-primary mb-1 shadow-inner'):
                            ui.icon('login', size='2.5rem')
                        ui.label('Chào mừng trở lại').classes('font-display text-3xl font-bold text-center tracking-tight')
                        ui.label('Tiếp tục khám phá tinh hoa Kinh Bắc').classes('text-muted-foreground text-sm text-center')

                    with ui.column().classes('gap-5 w-full'):
                        email = ui.input('Email').classes('w-full').props('outlined rounded-xl bg-background shadow-sm icon=alternate_email')
                        password = ui.input('Mật khẩu').classes('w-full').props('outlined rounded-xl type=password bg-background shadow-sm icon=lock')
                        
                        with ui.row().classes('w-full justify-between items-center -mt-2'):
                            ui.checkbox('Ghi nhớ đăng nhập').classes('text-sm text-muted-foreground opacity-80')
                            ui.link('Quên mật khẩu?', '#').classes('text-sm text-primary hover:underline font-medium')

                        async def handle_login():
                            if not email.value or not password.value:
                                ui.notify('Nhập email và mật khẩu', type='warning')
                                return
                            
                            login_btn.props('loading')
                            success = await api_client.login(email.value, password.value)
                            login_btn.props(remove='loading')
                            
                            if success:
                                ui.notify(f"Chào mừng {app.storage.user.get('user_name')}!", type='positive', position='top')
                                ui.navigate.to('/')
                            else:
                                ui.notify('Sai email hoặc mật khẩu', type='negative')
                                
                        login_btn = ui.button('Đăng nhập', on_click=handle_login).props('unelevated rounded-xl').classes('w-full bg-primary text-white font-black py-3 shadow-xl shadow-primary/20 hover:scale-[1.02] transition-transform text-base uppercase tracking-wider')
                        
                        with ui.row().classes('w-full justify-center gap-1.5 mt-2 text-sm'):
                            ui.label('Chưa có tài khoản?').classes('text-muted-foreground')
                            ui.link('Đăng ký miễn phí', '/dang-ky').classes('text-primary font-bold hover:underline')


