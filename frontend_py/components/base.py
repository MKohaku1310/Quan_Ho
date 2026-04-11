from nicegui import ui, app
import theme
from api import api_client

def navbar():
    # Detect current path for active state
    current_path = ui.context.client.page.path if hasattr(ui.context, 'client') and hasattr(ui.context.client, 'page') else '/'
    
    # Glassmorphism navbar
    with ui.header().classes('qh-navbar fixed top-0 left-0 right-0 z-[100] w-full transition-all duration-300').style(
        'background: rgba(255, 248, 240, 0.75); '
        'backdrop-filter: blur(16px) saturate(180%); '
        '-webkit-backdrop-filter: blur(16px) saturate(180%); '
        'border-bottom: 0.5px solid rgba(180, 120, 60, 0.1); '
        'box-shadow: 0 4px 30px rgba(0, 0, 0, 0.05);'
    ).props('elevated=false'):
        with theme.container().classes('flex h-14 items-center px-4'):
            # 1. Left: Logo
            with ui.element('div').classes('flex-1 flex justify-start items-center'):
                with ui.link(target='/').classes('flex items-center gap-2 no-underline transition-opacity hover:opacity-80 shrink-0'):
                    ui.image('/static/lotus-ornament.png').classes('h-7 w-7')
                    with ui.row().classes('gap-1 items-baseline'):
                        ui.label('Quan Họ').classes('font-display text-lg font-bold text-primary whitespace-nowrap')
                        ui.label('Bắc Ninh').classes('font-display text-lg font-bold text-[#d4af37] whitespace-nowrap')

            # 2. Center: Nav Items
            with ui.element('div').classes('max-lg:hidden flex items-center justify-center gap-1 whitespace-nowrap px-4'):
                nav_items = [
                    ('/', 'home', 'Trang chủ'),
                    ('/gioi-thieu', 'intro', 'Giới thiệu'),
                    ('/bai-hat', 'songs', 'Bài hát'),
                    ('/nghe-nhan', 'artists', 'Nghệ nhân'),
                    ('/lang-quan-ho', 'villages', 'Làng Quan họ'),
                    ('/tin-tuc', 'news', 'Tin tức'),
                ]
                for path, key, label in nav_items:
                    is_active = (current_path == path)
                    ui.link(label, target=path).classes(
                        f'rounded-md px-3 py-1.5 text-sm font-medium transition-colors hover:bg-primary/10 hover:text-primary no-underline '
                        f'{"text-primary font-bold bg-primary/5" if is_active else "text-muted-foreground"}'
                    )

            # 3. Right: Actions
            with ui.element('div').classes('flex-1 flex justify-end items-center gap-3'):
                ui.button(icon='search', on_click=lambda: ui.navigate.to('/bai-hat')).props('flat round size=sm').classes('text-muted-foreground hover:text-primary')
                ui.label('VI').classes('flex h-8 w-8 items-center justify-center rounded-md text-xs font-bold text-muted-foreground transition-colors border border-border/50 max-sm:hidden')
                
                with ui.element('div').classes('max-sm:hidden flex items-center gap-1'):
                    if app.storage.user.get('is_authenticated'):
                        ui.button('Hồ sơ', icon='account_circle', on_click=lambda: ui.navigate.to('/ho-so')).props('flat rounded size=sm').classes('text-muted-foreground font-medium px-3')
                        ui.button(icon='logout', on_click=lambda: (api_client.logout(), ui.navigate.to('/'))).props('flat round size=sm').classes('text-destructive hover:bg-destructive/10')
                    else:
                        ui.button('Đăng nhập', on_click=lambda: ui.navigate.to('/dang-nhap')).props('flat rounded size=sm').classes('text-muted-foreground font-medium px-3')
                        ui.button('Đăng ký', on_click=lambda: ui.navigate.to('/dang-ky')).props('unelevated rounded size=sm').classes('bg-primary text-white font-semibold px-4 shadow-sm')
                
                mobile_btn = ui.button(icon='menu').props('flat round').classes('lg:hidden text-muted-foreground')
                
                with ui.dialog() as drawer:
                    with ui.card().classes('w-72 h-full p-0 overflow-hidden'):
                        with ui.column().classes('p-4 gap-1'):
                            with ui.row().classes('justify-between items-center mb-6 px-2'):
                                ui.label('Menu').classes('font-bold text-lg')
                                ui.button(icon='close', on_click=drawer.close).props('flat round size=sm')
                            for path, key, label in nav_items:
                                is_active = (current_path == path)
                                ui.link(label, target=path).classes(f'w-full px-4 py-3 rounded-md no-underline {"bg-muted text-primary font-bold" if is_active else "text-muted-foreground hover:bg-muted/50"}')
                            ui.element('div').classes('mt-4 border-t border-border pt-4 px-2 space-y-2')
                            if app.storage.user.get('is_authenticated'):
                                ui.button('Hồ sơ cá nhân', icon='account_circle', on_click=lambda: ui.navigate.to('/ho-so')).props('flat rounded size=md').classes('w-full text-muted-foreground justify-start')
                            else:
                                ui.button('Đăng nhập', icon='login', on_click=lambda: ui.navigate.to('/dang-nhap')).props('flat rounded size=md').classes('w-full text-muted-foreground justify-start')
                mobile_btn.on_click(drawer.open)

def footer():
    with ui.element('footer').classes('w-full border-t border-border bg-card mt-auto shrink-0'):
        with ui.element('div').classes('mx-auto max-w-7xl px-4 py-12'):
            with ui.element('div').classes('grid grid-cols-1 gap-12 md:grid-cols-4'):
                # Column 1: Brand
                with ui.column().classes('gap-4'):
                    with ui.row().classes('items-center gap-2'):
                        ui.image('/static/lotus-ornament.png').classes('h-8 w-8')
                        ui.label('Quan Họ Bắc Ninh').classes('font-display text-lg font-bold text-primary')
                    ui.label(
                        'Bảo tồn và phát huy giá trị di sản văn hóa phi vật thể '
                        'Quan họ Bắc Ninh — Di sản UNESCO 2009.'
                    ).classes('text-sm text-muted-foreground leading-relaxed')

                # Column 2: Explore
                with ui.column().classes('gap-3'):
                    ui.label('KHÁM PHÁ').classes('font-display text-sm font-semibold text-foreground mb-1')
                    for label, path in [
                        ('Giới thiệu',   '/gioi-thieu'),
                        ('Bài hát',      '/bai-hat'),
                        ('Nghệ nhân',    '/nghe-nhan'),
                        ('Làng Quan họ', '/lang-quan-ho'),
                    ]:
                        ui.link(label, target=path).classes('text-sm text-muted-foreground hover:text-primary no-underline transition-colors')

                # Column 3: Contact
                with ui.column().classes('gap-3'):
                    ui.label('LIÊN HỆ').classes('font-display text-sm font-semibold text-foreground mb-1')
                    ui.label('Sở Văn hóa, Thể thao và Du lịch tỉnh Bắc Ninh').classes('text-sm text-muted-foreground')
                    ui.label('Email: quanho@bacninh.gov.vn').classes('text-sm text-muted-foreground')

                # Column 4: Social Media
                with ui.column().classes('gap-3'):
                    ui.label('KẾT NỐI').classes('font-display text-sm font-semibold text-foreground mb-1')
                    with ui.row().classes('gap-3'):
                        with ui.element('a').classes(
                            'flex h-10 w-10 items-center justify-center rounded-full bg-primary/10 '
                            'text-primary hover:bg-primary hover:text-white transition-all cursor-pointer'
                        ).props('href="https://facebook.com" target="_blank"'):
                            ui.html('<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>')
                        with ui.element('a').classes(
                            'flex h-10 w-10 items-center justify-center rounded-full bg-primary/10 '
                            'text-primary hover:bg-primary hover:text-white transition-all cursor-pointer'
                        ).props('href="https://youtube.com" target="_blank"'):
                            ui.html('<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>')
                    ui.label('Theo dõi chúng tôi trên mạng xã hội').classes('text-xs text-muted-foreground')

            # Bottom Bar
            ui.element('div').classes('mt-12 border-t border-border pt-8')
            with ui.row().classes('w-full justify-between items-center gap-4 flex-wrap'):
                with ui.row().classes('items-center gap-2'):
                    ui.label('© 2024 Quan Họ Bắc Ninh.').classes('text-xs font-bold text-foreground')
                    ui.label('Trân quý và bảo tồn di sản thế giới.').classes('text-xs text-muted-foreground')
                
                with ui.row().classes('gap-4'):
                    for link_label in ['Điều khoản', 'Bảo mật', 'Liên hệ']:
                        ui.link(link_label, '#').classes('text-[10px] uppercase tracking-widest font-bold text-muted-foreground hover:text-primary no-underline transition-colors')

def section_title(title, subtitle=None):
    with ui.column().classes('mb-8 text-center w-full items-center gap-2'):
        ui.image('/static/lotus-ornament.png').classes('mx-auto mb-2 h-10 w-10 opacity-70')
        ui.label(title).classes('font-display text-3xl font-bold text-foreground md:text-4xl')
        if subtitle:
            ui.label(subtitle).classes('mx-auto max-w-2xl text-muted-foreground text-sm')

def filter_pills(options, active_option, on_change):
    with ui.row().classes('gap-3 mb-12'):
        for opt in options:
            is_active = opt == active_option
            ui.button(opt, on_click=lambda o=opt: on_change(o)).props('unelevated rounded-full' if is_active else 'outline rounded-full').classes(
                f'px-6 py-2 text-sm font-bold transition-all '
                f'{"bg-primary text-white shadow-md" if is_active else "text-muted-foreground border-border hover:border-primary hover:text-primary"}'
            )

def empty_state(message, icon='search_off'):
    with ui.column().classes('items-center justify-center py-32 w-full opacity-60 gap-4'):
        ui.icon(icon, size='64px').classes('text-muted-foreground/30')
        ui.label(message).classes('text-xl italic font-light tracking-wide')

def page_header(title, subtitle):
    # Account for fixed navbar height (56px)
    with ui.element('section').classes('bg-card/30 pt-32 pb-20 border-b border-border w-full flex justify-center').style('padding-top: 120px;'):
        with theme.container().classes('text-center'):
            ui.image('/static/lotus-ornament.png').classes('mb-6 h-12 w-12 mx-auto')
            ui.label(title).classes('font-display text-5xl font-black text-foreground mb-4 tracking-tight')
            ui.label(subtitle).classes('max-w-2xl mx-auto text-lg text-muted-foreground font-light leading-relaxed')
