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

@ui.page('/dang-ky')
def register_page():
    with theme.frame():
        with ui.element('section').classes('py-20 md:py-32 bg-background w-full flex justify-center px-4'):
            with ui.card().classes('w-full max-w-md p-8 sm:p-10 rounded-3xl shadow-elevated border border-border bg-card'):
                with ui.column().classes('items-center w-full gap-2 mb-8'):
                    ui.element('div').classes('h-16 w-16 rounded-2xl bg-primary/10 flex items-center justify-center text-primary mb-2').add(ui.icon('person_add', size='2.5rem'))
                    ui.label('Khởi tạo hành trình').classes('font-display text-3xl font-bold text-center')
                    ui.label('Tham gia cộng đồng yêu dân ca Quan họ').classes('text-muted-foreground text-sm text-center')

                with ui.column().classes('gap-5 w-full'):
                    # Fields with realtime validation
                    name = ui.input('Họ và tên').classes('w-full').props('outlined rounded-lg')
                    
                    email = ui.input('Email').classes('w-full').props('outlined rounded-lg type=email')
                    email_error = ui.label('').classes('text-[11px] text-negative -mt-4 ml-1 opacity-0 transition-opacity')
                    
                    password = ui.input('Mật khẩu').classes('w-full').props('outlined rounded-lg type=password')
                    pass_strength = ui.label('').classes('text-[11px] -mt-4 ml-1 opacity-0 transition-opacity')
                    
                    confirm_pass = ui.input('Xác nhận mật khẩu').classes('w-full').props('outlined rounded-lg type=password')
                    confirm_error = ui.label('').classes('text-[11px] text-negative -mt-4 ml-1 opacity-0 transition-opacity')

                    # Validation Logic
                    def validate_email(e):
                        if not e: email_error.classes('opacity-0'); return
                        is_valid = re.match(r"[^@]+@[^@]+\.[^@]+", e)
                        email_error.text = "" if is_valid else "Email không đúng định dạng"
                        email_error.classes(replace=('opacity-100' if not is_valid else 'opacity-0'))

                    def validate_pass(p):
                        if not p: pass_strength.classes('opacity-0'); return
                        score = 0
                        if len(p) >= 8: score += 1
                        if any(c.isupper() for c in p): score += 1
                        if any(c.isdigit() for c in p): score += 1
                        
                        msgs = ["Yếu", "Trung bình", "Mạnh"]
                        colors = ["text-negative", "text-warning", "text-positive"]
                        idx = min(score, 2)
                        pass_strength.text = f"Độ mạnh: {msgs[idx]}"
                        pass_strength.classes(replace=f'opacity-100 {colors[idx]}')

                    def validate_confirm(cp):
                        if not cp: confirm_error.classes('opacity-0'); return
                        is_match = cp == password.value
                        confirm_error.text = "" if is_match else "Mật khẩu không khớp"
                        confirm_error.classes(replace=('opacity-100' if not is_match else 'opacity-0'))

                    email.on('update:model-value', lambda e: validate_email(e))
                    password.on('update:model-value', lambda p: validate_pass(p))
                    confirm_pass.on('update:model-value', lambda cp: validate_confirm(cp))

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
                            
                    reg_btn = ui.button('Đăng ký tài khoản', on_click=handle_register).props('unelevated rounded-lg').classes('w-full bg-primary text-white font-bold py-3.5 mt-2 shadow-lg shadow-primary/20 hover:scale-[1.02] transition-transform')
                    
                    with ui.row().classes('w-full justify-center gap-1.5 mt-4 text-sm'):
                        ui.label('Bạn đã có tài khoản?').classes('text-muted-foreground')
                        ui.link('Đăng nhập tại đây', '/dang-nhap').classes('text-primary font-bold hover:underline')

@ui.page('/dang-nhap')
def login_page():
    # If already logged in, go home
    if app.storage.user.get('is_authenticated'):
        ui.navigate.to('/')
        return

    with theme.frame():
        with ui.element('section').classes('py-20 md:py-32 bg-background w-full flex justify-center px-4'):
            with ui.card().classes('w-full max-w-md p-8 sm:p-10 rounded-3xl shadow-elevated border border-border bg-card'):
                with ui.column().classes('items-center w-full gap-2 mb-8'):
                    ui.element('div').classes('h-16 w-16 rounded-2xl bg-primary/10 flex items-center justify-center text-primary mb-2').add(ui.icon('login', size='2.5rem'))
                    ui.label('Chào mừng trở lại').classes('font-display text-3xl font-bold text-center')
                    ui.label('Đăng nhập để tiếp tục khám phá Kinh Bắc').classes('text-muted-foreground text-sm text-center')

                with ui.column().classes('gap-5 w-full'):
                    email = ui.input('Email').classes('w-full').props('outlined rounded-lg type=email icon=alternate_email')
                    password = ui.input('Mật khẩu').classes('w-full').props('outlined rounded-lg type=password icon=lock')
                    
                    with ui.row().classes('w-full justify-between items-center -mt-2'):
                        ui.checkbox('Ghi nhớ tôi').classes('text-xs text-muted-foreground opacity-70')
                        ui.link('Quên mật khẩu?', '#').classes('text-xs text-primary hover:underline')

                    async def handle_login():
                        if not email.value or not password.value:
                            ui.notify('Nhập email và mật khẩu', type='warning')
                            return
                        
                        login_btn.props('loading')
                        success = await api_client.login(email.value, password.value)
                        login_btn.props(remove='loading')
                        
                        if success:
                            ui.notify('Đăng nhập thành công', type='positive', position='top')
                            ui.navigate.to('/ho-so')
                        else:
                            ui.notify('Email hoặc mật khẩu không đúng', type='negative')
                            
                    login_btn = ui.button('Đăng nhập', on_click=handle_login).props('unelevated rounded-lg').classes('w-full bg-primary text-white font-bold py-3.5 mt-2 shadow-lg shadow-primary/20 hover:scale-[1.02] transition-transform')
                    
                    with ui.row().classes('w-full justify-center gap-1.5 mt-4 text-sm'):
                        ui.label('Thành viên mới?').classes('text-muted-foreground')
                        ui.link('Đăng ký ngay', '/dang-ky').classes('text-primary font-bold hover:underline')

@ui.page('/ho-so')
@auth_required
async def profile_page():
    # Fetch refresh profile info
    user_data = await api_client.get_me()
    if not user_data:
        app.storage.user.clear()
        ui.navigate.to('/dang-nhap')
        return

    with theme.frame():
        with ui.element('section').classes('py-12 md:py-20 bg-background min-h-screen'):
            with theme.container().classes('max-w-6xl'):
                with ui.row().classes('w-full gap-8 flex-col lg:flex-row'):
                    
                    # Sidebar Column
                    with ui.column().classes('w-full lg:w-80 gap-6 shrink-0'):
                        with ui.card().classes('w-full p-8 rounded-3xl shadow-sm border border-border bg-card text-center items-center'):
                            # Avatar Section
                            with ui.element('div').classes('relative group'):
                                avatar = ui.image(user_data.get('avatar_url') or 'https://api.dicebear.com/7.x/avataaars/svg?seed=' + user_data.get('name')).classes('w-32 h-32 rounded-full border-4 border-primary/20 bg-muted object-cover shadow-inner transition-all group-hover:brightness-75')
                                with ui.element('label').classes('absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 cursor-pointer transition-opacity'):
                                    ui.icon('upload', size='2rem').classes('text-white')
                                    # Simulation of upload
                                    ui.upload(on_upload=lambda e: ui.notify('Đã tải ảnh lên thành công (Simulation)')).classes('hidden')

                            ui.label(user_data.get('name')).classes('font-display text-2xl font-bold mt-6 tracking-tight')
                            ui.label(user_data.get('email')).classes('text-sm text-muted-foreground -mt-1')
                            
                            ui.element('div').classes('mt-4 px-3 py-1 bg-primary/10 text-primary text-[10px] font-bold uppercase rounded-full').add(ui.label(user_data.get('role', 'Member')))
                            
                            ui.separator().classes('my-6 opacity-50')
                            
                            with ui.column().classes('w-full gap-3'):
                                ui.button('Cập nhật ảnh', icon='photo_camera', on_click=lambda: ui.notify('Tính năng đang hoàn thiện')).props('flat dense').classes('text-sm text-foreground/70 w-full justify-start')
                                ui.button('Cài đặt tài khoản', icon='settings').props('flat dense').classes('text-sm text-foreground/70 w-full justify-start')
                                ui.button('Đăng xuất', icon='logout', on_click=lambda: (app.storage.user.clear(), ui.navigate.to('/'))).props('flat dense').classes('text-sm text-negative w-full justify-start mt-4 font-bold')

                    # Content Column
                    with ui.column().classes('flex-1 min-w-0'):
                        with ui.tabs().classes('w-full border-b border-border bg-card/30 rounded-t-3xl') as tabs:
                            info_tab = ui.tab('Thông tin cá nhân', icon='person').classes('font-bold tracking-wide py-4')
                            activity_tab = ui.tab('Hoạt động của tôi', icon='history').classes('font-bold tracking-wide py-4')
                            security_tab = ui.tab('Bảo mật', icon='security').classes('font-bold tracking-wide py-4')

                        with ui.tab_panels(tabs, value=info_tab).classes('w-full bg-card rounded-b-3xl border-x border-b border-border shadow-sm p-6 md:p-10'):
                            # PERSONAL INFO TAB
                            with ui.tab_panel(info_tab).classes('p-0 gap-8'):
                                ui.label('Hồ sơ công khai').classes('text-xl font-bold mb-4 opacity-70')
                                with ui.column().classes('w-full gap-6'):
                                    with ui.row().classes('grid grid-cols-1 md:grid-cols-2 gap-6 w-full'):
                                        edit_name = ui.input('Họ và tên', value=user_data.get('name')).classes('w-full').props('outlined rounded-lg')
                                        edit_phone = ui.input('Số điện thoại', value=user_data.get('phone')).classes('w-full').props('outlined rounded-lg')
                                    
                                    edit_bio = ui.textarea('Lời tựa / Giới thiệu', value=user_data.get('bio')).classes('w-full').props('outlined rounded-lg auto-grow')
                                    
                                    async def save_profile():
                                        save_btn.props('loading')
                                        ok = await api_client.update_profile({'name': edit_name.value, 'phone': edit_phone.value, 'bio': edit_bio.value})
                                        save_btn.props(remove='loading')
                                        if ok:
                                            ui.notify('Đã cập nhật thông tin thành công', type='positive')
                                        else:
                                            ui.notify('Cập nhật thất bại', type='negative')
                                            
                                    save_btn = ui.button('Lưu thay đổi', on_click=save_profile).classes('px-8 py-2.5 rounded-xl font-bold').props('unelevated color="primary"')

                            # ACTIVITIES TAB
                            with ui.tab_panel(activity_tab).classes('p-0'):
                                activities = await api_client.get_activities()
                                if not activities:
                                    # Add some mock for demo if empty
                                    activities = [
                                        {'type': 'history', 'title': 'Đã nghe: "Khách đến chơi nhà"', 'date': '2026-04-11T15:30:00'},
                                        {'type': 'favorite', 'title': 'Đã thích bài: "Người ơi người ở đừng về"', 'date': '2026-04-10T10:15:00'},
                                        {'type': 'event', 'title': 'Đã đăng ký: Hội Lim 2026', 'date': '2026-04-09T09:00:00'},
                                    ]

                                if not activities:
                                    components.empty_state('Bạn chưa có hoạt động nào.')
                                else:
                                    with ui.column().classes('w-full gap-4'):
                                        for act in activities:
                                            with ui.row().classes('w-full items-center p-4 rounded-2xl hover:bg-muted/50 transition-colors border border-transparent hover:border-border'):
                                                icon_map = {'history': 'history', 'favorite': 'favorite', 'event': 'how_to_reg'}
                                                color_map = {'history': 'primary', 'favorite': 'negative', 'event': 'warning'}
                                                
                                                ui.element('div').classes(f'h-10 w-10 rounded-full bg-{color_map[act["type"]]}/10 text-{color_map[act["type"]]} flex items-center justify-center shrink-0').add(ui.icon(icon_map[act['type']], size='1.25rem'))
                                                with ui.column().classes('flex-1 gap-0 ml-4'):
                                                    ui.label(act['title']).classes('font-bold text-foreground text-sm')
                                                    dt = act['date'][:16].replace('T', ' ')
                                                    ui.label(dt).classes('text-[10px] text-muted-foreground')
                                                ui.icon('chevron_right', size='1rem').classes('text-muted-foreground opacity-30')

                            # SECURITY TAB
                            with ui.tab_panel(security_tab).classes('p-0 gap-8'):
                                ui.label('Đổi mật khẩu').classes('text-xl font-bold mb-4 opacity-70')
                                with ui.column().classes('w-full max-w-sm gap-4'):
                                    old_p = ui.input('Mật khẩu cũ').props('outlined rounded-lg type=password').classes('w-full')
                                    new_p = ui.input('Mật khẩu mới').props('outlined rounded-lg type=password').classes('w-full')
                                    confirm_p = ui.input('Xác nhận mật khẩu mới').props('outlined rounded-lg type=password').classes('w-full')
                                    
                                    async def handle_change_pass():
                                        if new_p.value != confirm_p.value:
                                            ui.notify('Mật khẩu xác nhận không khớp', type='warning')
                                            return
                                        
                                        pass_btn.props('loading')
                                        ok = await api_client.change_password(old_p.value, new_p.value)
                                        pass_btn.props(remove='loading')
                                        if ok:
                                            ui.notify('Đã đổi mật khẩu thành công', type='positive')
                                            old_p.value = new_p.value = confirm_p.value = ""
                                        else:
                                            ui.notify('Mật khẩu cũ không đúng hoặc có lỗi', type='negative')

                                    pass_btn = ui.button('Cập nhật mật khẩu', on_click=handle_change_pass).classes('w-full py-2.5 rounded-xl font-bold').props('unelevated color="primary"')
