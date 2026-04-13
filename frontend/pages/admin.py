from nicegui import app, ui
import theme
import components
from api import api_client



@ui.page('/admin')
async def admin_page():
    print(f"DEBUG ADMIN_PAGE: app.storage.user keys: {list(app.storage.user.keys())}")
    print(f"DEBUG ADMIN_PAGE: role: {app.storage.user.get('role')}, auth: {app.storage.user.get('is_authenticated')}")
    
    if not app.storage.user.get('is_authenticated') or app.storage.user.get('role') != 'admin':
        print("DEBUG ADMIN_PAGE: Redirecting due to missing auth/role")
        ui.navigate.to('/dang-nhap')
        return

    print("DEBUG ADMIN_PAGE: Fetching users...")
    users = await api_client.get_users()
    print(f"DEBUG ADMIN_PAGE: Received {len(users)} users")
    
    with theme.frame():
        with ui.element('section').classes('pt-12 pb-24 bg-background min-h-screen'):
            with theme.container():
                # Admin Header
                with ui.row().classes('w-full justify-between items-center mb-10 px-4'):
                    with ui.column().classes('gap-1'):
                        ui.label('QUẢN TRỊ HỆ THỐNG').classes('text-[10px] font-black tracking-[0.3em] text-primary opacity-80 uppercase')
                        ui.label('Bảng điều khiển').classes('text-5xl font-display font-bold text-foreground tracking-tight')
                    
                    with ui.row().classes('gap-4'):
                        ui.button('Làm mới', icon='refresh', on_click=ui.navigate.reload).props('outline rounded-xl').classes('px-6 font-bold')
                        ui.button('Về trang chủ', icon='home', on_click=lambda: ui.navigate.to('/')).props('unelevated rounded-xl color=primary').classes('px-6 font-black')

                # Stats Row (Quick Overview)
                with ui.row().classes('w-full grid grid-cols-1 md:grid-cols-4 gap-6 mb-12'):
                    stats = [
                        ('Tổng người dùng', len(users), 'group', 'bg-blue-500/10 text-blue-600'),
                        ('Làn điệu', '45', 'music_note', 'bg-primary/10 text-primary'),
                        ('Nghệ nhân', '12', 'person', 'bg-secondary/10 text-secondary'),
                        ('Lượt truy cập', '1.2k', 'trending_up', 'bg-green-500/10 text-green-600'),
                    ]
                    for label, val, icon, color_classes in stats:
                        with ui.card().classes('rounded-[2rem] p-6 flex flex-col items-center justify-center gap-2 border border-border shadow-sm hover:shadow-md transition-shadow'):
                            with ui.element('div').classes(f'h-12 w-12 rounded-2xl {color_classes} flex items-center justify-center'):
                                ui.icon(icon, size='1.5rem')
                            ui.label(str(val)).classes('text-3xl font-black tracking-tight')
                            ui.label(label).classes('text-[10px] font-bold text-muted-foreground uppercase tracking-widest')

                # Main Tables Section
                with ui.column().classes('w-full gap-8'):
                    # USER MANAGEMENT TABLE
                    with ui.card().classes('w-full p-8 rounded-[2.5rem] shadow-xl border border-border bg-card overflow-hidden'):
                        with ui.row().classes('w-full justify-between items-center mb-8'):
                            with ui.row().classes('items-center gap-4'):
                                with ui.element('div').classes('h-12 w-12 rounded-2xl bg-primary/10 text-primary flex items-center justify-center'):
                                    ui.icon('manage_accounts', size='1.8rem')
                                ui.label('Quản lý người dùng').classes('text-2xl font-bold tracking-tight')
                            
                            ui.input('Tìm kiếm người dùng...').props('outlined dense rounded-xl bg-background').classes('w-64')

                        async def handle_delete(user_id):
                            if user_id == app.storage.user.get('user_id'):
                                ui.notify('Bạn không thể tự xóa tài khoản của chính mình', type='warning')
                                return
                            
                            with ui.dialog() as dialog, ui.card().classes('p-8 rounded-3xl items-center text-center'):
                                ui.icon('warning', size='4rem', color='negative').classes('mb-4')
                                ui.label('Xác nhận xóa tài khoản?').classes('text-2xl font-bold mb-2')
                                ui.label('Hành động này không thể hoàn tác. Mọi dữ liệu của người dùng này sẽ bị mất.').classes('text-muted-foreground mb-6')
                                with ui.row().classes('gap-4'):
                                    ui.button('Đóng', on_click=dialog.close).props('flat')
                                    async def confirm():
                                        ok = await api_client.delete_user(user_id)
                                        if ok:
                                            ui.notify('Đã xóa người dùng thành công', type='positive')
                                            ui.navigate.reload()
                                        else:
                                            ui.notify('Lỗi khi xóa người dùng', type='negative')
                                    ui.button('XÓA VĨNH VIỄN', on_click=confirm).props('unelevated color=negative').classes('rounded-xl px-6')
                            dialog.open()

                        # HTML Table for more control / premium look
                        with ui.element('div').classes('w-full overflow-x-auto ring-1 ring-border rounded-2xl'):
                            with ui.element('table').classes('w-full text-left'):
                                with ui.element('thead').classes('bg-muted/50'):
                                    with ui.element('tr'):
                                        headers = ['ID', 'Người dùng', 'Email', 'Vai trò', 'Ngày tham gia', 'Thao tác']
                                        for h in headers:
                                            with ui.element('th').classes('px-6 py-4 text-[10px] font-black uppercase tracking-widest text-muted-foreground'):
                                                ui.label(h)
                                
                                with ui.element('tbody').classes('divide-y divide-border'):
                                    if not users:
                                        with ui.element('tr'):
                                            with ui.element('td').props('colspan=6').classes('px-6 py-12 text-center text-muted-foreground'):
                                                ui.label('Không có dữ liệu')
                                    else:
                                        for u in users:
                                            with ui.element('tr').classes('hover:bg-muted/20 transition-colors group'):
                                                # ID
                                                with ui.element('td').classes('px-6 py-4 font-body text-xs text-muted-foreground opacity-60'):
                                                    ui.label(f"#{u['id']}")
                                                
                                                # User info
                                                with ui.element('td').classes('px-6 py-4'):
                                                    with ui.row().classes('items-center gap-3'):
                                                        ui.avatar(f'https://api.dicebear.com/7.x/bottts-neutral/svg?seed={u["email"]}').classes('w-10 h-10 rounded-xl shadow-sm')
                                                        ui.label(u['name']).classes('font-bold text-sm')
                                                
                                                # Email
                                                with ui.element('td').classes('px-6 py-4 text-sm font-medium opacity-80'):
                                                    ui.label(u['email'])
                                                
                                                # Role Badge
                                                with ui.element('td').classes('px-6 py-4'):
                                                    is_u_admin = u['role'] == 'admin'
                                                    role_color = 'bg-secondary/10 text-secondary border-secondary/20' if is_u_admin else 'bg-primary/10 text-primary border-primary/20'
                                                    with ui.element('div').classes(f'px-3 py-1 text-[9px] font-black uppercase rounded-lg border {role_color} w-fit'):
                                                        ui.label(u['role'])

                                                # Joined Date
                                                with ui.element('td').classes('px-6 py-4 text-xs text-muted-foreground'):
                                                    ui.label(u['created_at'][:10])

                                                # Actions
                                                with ui.element('td').classes('px-6 py-4 text-right'):
                                                    with ui.row().classes('gap-2 items-center'):
                                                        ui.button(icon='edit', color='grey').props('flat round size=sm').classes('opacity-20 hover:opacity-100 transition-opacity')
                                                        ui.button(icon='delete', on_click=lambda u_id=u['id']: handle_delete(u_id)).props('flat round size=sm color=negative').classes('opacity-20 hover:opacity-100 transition-opacity')

                    # QUICK LINKS SECTION
                    with ui.row().classes('w-full grid grid-cols-1 md:grid-cols-3 gap-6'):
                        manage_items = [
                            ('Quản lý Làn điệu', 'music_note', '/bai-hat', 'bg-primary'),
                            ('Quản lý Nghệ nhân', 'groups', '/nghe-nhan', 'bg-secondary'),
                            ('Quản lý Tin tức', 'article', '/tin-tuc', 'bg-jade'),
                        ]
                        for title, icon, path, color in manage_items:
                            with ui.card().classes('rounded-[2rem] p-8 flex flex-col items-start gap-4 border border-border shadow-sm hover:scale-[1.02] transition-transform cursor-pointer').on('click', lambda p=path: ui.navigate.to(p)):
                                with ui.element('div').classes(f'h-14 w-14 rounded-2xl {color} text-white flex items-center justify-center shadow-lg'):
                                    ui.icon(icon, size='2rem')
                                ui.label(title).classes('text-xl font-bold tracking-tight')
                                ui.label('Chỉnh sửa, thêm bớt nội dung hệ thống.').classes('text-sm text-muted-foreground')
                                ui.button('Đi tới', icon='arrow_forward').props('flat rounded size=sm').classes('p-0 font-black')
