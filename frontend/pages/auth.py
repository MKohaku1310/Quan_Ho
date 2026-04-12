from nicegui import app, ui
import theme
import components
from api import api_client
import asyncio
import re

def auth_required(func):
    """Decorator to protect routes that require authentication."""
    async def wrapper(*args, **kwargs):
        if not app.storage.user.get('is_authenticated'):
            ui.notify('Vui lòng đăng nhập để truy cập trang này', type='warning')
            ui.navigate.to('/dang-nhap')
            return
        return await func(*args, **kwargs)
    return wrapper

def admin_required(func):
    """Decorator to protect routes that require admin privileges."""
    async def wrapper(*args, **kwargs):
        if not app.storage.user.get('is_authenticated'):
            ui.notify('Vui lòng đăng nhập', type='warning')
            ui.navigate.to('/dang-nhap')
            return
        if app.storage.user.get('role') != 'admin':
            ui.notify('Bạn không có quyền truy cập trang này', type='negative')
            ui.navigate.to('/')
            return
        return await func(*args, **kwargs)
    return wrapper

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

@ui.page('/ho-so')
@auth_required
async def profile_page():
    user_data = await api_client.get_me()
    if not user_data:
        app.storage.user.clear()
        ui.navigate.to('/dang-nhap')
        return

    is_admin = app.storage.user.get('role') == 'admin'

    with theme.frame():
        with ui.element('section').classes('pt-12 pb-24 bg-background min-h-screen'):
            with theme.container().classes('max-w-6xl'):
                # Profile Header / Breadcrumb
                with ui.row().classes('w-full justify-between items-end mb-8 px-4'):
                    with ui.column().classes('gap-1'):
                        ui.label('TÀI KHOẢN').classes('text-[10px] font-black tracking-[0.3em] text-primary opacity-80 uppercase')
                        ui.label('Hồ sơ cá nhân').classes('text-4xl font-display font-bold text-foreground tracking-tight')
                    
                    if is_admin:
                        ui.button('BẢNG QUẢN TRỊ', icon='admin_panel_settings', on_click=lambda: ui.navigate.to('/admin')).props('unelevated rounded-xl color=secondary').classes('px-6 py-2 shadow-lg font-bold')

                with ui.row().classes('w-full gap-8 flex-col lg:flex-row'):
                    # LEFT COLUMN: Identity Card
                    with ui.column().classes('w-full lg:w-80 gap-6 shrink-0'):
                        with ui.card().classes('w-full p-8 rounded-[2rem] shadow-xl border border-border bg-card text-center items-center overflow-hidden relative'):
                            # Background Glow
                            ui.element('div').classes('absolute -top-24 -right-24 w-48 h-48 bg-primary/10 rounded-full blur-3xl')
                            
                            # Avatar Section
                            with ui.element('div').classes('relative group z-10'):
                                seed = user_data.get('email')
                                avatar_url = f'https://api.dicebear.com/7.x/bottts-neutral/svg?seed={seed}&backgroundColor=b21e1e'
                                ui.image(user_data.get('avatar_url') or avatar_url).classes('w-40 h-40 rounded-[2.5rem] border-4 border-background shadow-inner bg-muted object-cover')
                                with ui.element('div').classes('absolute bottom-2 right-2 h-10 w-10 bg-primary text-white rounded-2xl flex items-center justify-center shadow-lg border-2 border-white cursor-pointer hover:scale-110 transition-transform'):
                                    ui.icon('edit', size='1.2rem')

                            ui.label(user_data.get('name')).classes('font-display text-3xl font-bold mt-8 tracking-tight')
                            ui.label(user_data.get('email')).classes('text-sm text-muted-foreground -mt-1 font-medium')
                            
                            # Role Badge
                            bg_color = 'bg-secondary/10 text-secondary' if is_admin else 'bg-primary/5 text-primary'
                            with ui.element('div').classes(f'mt-4 px-5 py-1.5 {bg_color} text-[10px] font-black uppercase rounded-full border border-current/10 shadow-sm'):
                                ui.label('QUẢN TRỊ VIÊN' if is_admin else 'THÀNH VIÊN')
                            
                            ui.separator().classes('my-8 opacity-40')
                            
                            with ui.column().classes('w-full gap-2.5'):
                                def logout_action():
                                    app.storage.user.clear()
                                    ui.notify('Đã đăng xuất', type='info')
                                    ui.navigate.to('/')

                                ui.button('Thông tin cá nhân', icon='person').props('flat rounded size=md').classes('w-full justify-start font-bold text-foreground/80 lowercase tracking-wide')
                                ui.button('Bảo mật', icon='security').props('flat rounded size=md').classes('w-full justify-start font-bold text-foreground/80 lowercase tracking-wide')
                                ui.button('Đăng xuất', icon='logout', on_click=logout_action).props('flat rounded size=md').classes('w-full justify-start font-bold text-negative mt-4 hover:bg-negative/5')

                    # RIGHT COLUMN: Content Tabs
                    with ui.column().classes('flex-1 min-w-0'):
                        with ui.card().classes('w-full p-8 sm:p-12 rounded-[2rem] shadow-xl border border-border bg-card flex flex-col gap-10'):
                            # PERSONAL INFO SECTION
                            with ui.column().classes('w-full gap-6'):
                                with ui.row().classes('w-full items-center gap-3 mb-2'):
                                    ui.icon('edit', size='2rem').classes('text-primary opacity-20')
                                    ui.label('Chỉnh sửa hồ sơ').classes('text-2xl font-bold tracking-tight')
                                
                                with ui.row().classes('grid grid-cols-1 md:grid-cols-2 gap-8 w-full'):
                                    edit_name = ui.input('Họ và tên', value=user_data.get('name')).classes('w-full').props('outlined rounded-xl bg-background')
                                    edit_phone = ui.input('Số điện thoại', value=user_data.get('phone')).classes('w-full').props('outlined rounded-xl bg-background')
                                
                                edit_bio = ui.textarea('Lời tựa / Giới thiệu', value=user_data.get('bio')).classes('w-full').props('outlined rounded-xl bg-background auto-grow')
                                
                                async def save_profile():
                                    save_btn.props('loading')
                                    ok = await api_client.update_profile({'name': edit_name.value, 'phone': edit_phone.value, 'bio': edit_bio.value})
                                    save_btn.props(remove='loading')
                                    if ok:
                                        ui.notify('Cập nhật thành công!', type='positive')
                                    else:
                                        ui.notify('Cập nhật thất bại', type='negative')
                                        
                                with ui.row().classes('w-full justify-end mt-4'):
                                    save_btn = ui.button('Lưu thay đổi', on_click=save_profile).classes('px-10 py-3 rounded-2xl font-black text-lg shadow-xl shadow-primary/20').props('unelevated color="primary"')

                            ui.separator().classes('opacity-30')

                            # SECURITY SECTION (Quick access)
                            with ui.column().classes('w-full gap-6'):
                                with ui.row().classes('w-full items-center gap-3 mb-2'):
                                    ui.icon('shield', size='2rem').classes('text-primary opacity-20')
                                    ui.label('Bảo mật tài khoản').classes('text-2xl font-bold tracking-tight')
                                
                                with ui.row().classes('grid grid-cols-1 md:grid-cols-2 gap-8 w-full items-end'):
                                    new_p = ui.input('Đổi mật khẩu mới').props('outlined rounded-xl type=password bg-background').classes('w-full')
                                    pass_btn = ui.button('Cập nhật mật khẩu', on_click=lambda: ui.notify('Tính năng đổi mật khẩu đang được xử lý')).classes('w-full py-4 rounded-xl font-bold border-2 border-primary/20 text-primary hover:bg-primary/5 transition-colors').props('flat')
