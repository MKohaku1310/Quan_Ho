from nicegui import ui, app
import theme
from api import api_client
from translation import t, toggle_language

def navbar():
    # Detect current path for active state
    current_path = ui.context.client.page.path if hasattr(ui.context, 'client') and hasattr(ui.context.client, 'page') else '/'
    
    # Navigation items for both desktop and mobile
    nav_items = [
        ('/', 'home', t('home')),
        ('/gioi-thieu', 'intro', t('intro')),
        ('/bai-hat', 'songs', t('songs')),
        ('/nghe-nhan', 'artists', t('artists')),
        ('/lang-quan-ho', 'villages', t('villages')),
        ('/tin-tuc', 'news', t('news')),
    ]

    # Glassmorphism navbar (Styled in theme.py via .qh-navbar)
    with ui.header().classes('qh-navbar w-full').props('elevated=false'):
        with theme.container().classes('flex h-14 items-center px-4'):
            # 1. Left: Logo
            with ui.element('div').classes('flex-1 flex justify-start items-center'):
                with ui.link(target='/').classes('flex items-center gap-2 no-underline transition-opacity hover:opacity-80 shrink-0'):
                    ui.image('/static/common/lotus-ornament.png').classes('h-7 w-7')
                    with ui.row().classes('gap-1 items-baseline'):
                        ui.label('Quan Họ').classes('font-display text-lg font-bold text-primary whitespace-nowrap')
                        ui.label('Bắc Ninh').classes('font-display text-lg font-bold text-[#d4af37] whitespace-nowrap')

            # 2. Center: Nav Items (Desktop)
            # Using style('display: flex') to bypass Tailwind md: breakpoint issues in NiceGUI
            with ui.element('div').classes('items-center justify-center gap-1 whitespace-nowrap px-2').style('display: flex !important;'):
                for path, key, label in nav_items:
                    is_active = (current_path == path)
                    ui.link(label, target=path).classes(
                        f'rounded-lg px-4 py-2 text-sm font-bold transition-all hover:bg-primary/10 hover:text-primary no-underline '
                        f'{"text-primary bg-primary/5 shadow-sm" if is_active else "text-muted-foreground"}'
                    )

            # 3. Right: Actions
            with ui.element('div').classes('flex-1 flex justify-end items-center gap-1 sm:gap-2 flex-nowrap').style('display: flex !important;'):
                # Language Toggle
                lang_label = t('language_toggle')
                ui.button(lang_label, on_click=lambda: (toggle_language(), ui.navigate.reload())).props('flat rounded size=md').classes('text-muted-foreground font-bold border border-border/50 px-2 min-w-0 h-9 shrink-0')

                # Auth buttons - Integrated into one row for consistent alignment
                if app.storage.user.get('is_authenticated'):
                    if app.storage.user.get('role') == 'admin':
                        ui.button('ADMIN', icon='dashboard', on_click=lambda: ui.navigate.to('/admin')).props('flat rounded size=md').classes('text-secondary font-black px-3 h-10 border border-secondary/20 hover:bg-secondary/10 shrink-0')
                    
                    ui.button(t('profile'), icon='account_circle', on_click=lambda: ui.navigate.to('/ho-so')).props('flat rounded size=md').classes('text-muted-foreground font-medium px-3 h-10 hover:bg-muted shrink-0')
                    ui.button(icon='logout', on_click=api_client.logout).props('flat round size=md').classes('text-destructive hover:bg-destructive/10 h-10 w-10 flex-shrink-0')
                else:
                    ui.button(t('login'), on_click=lambda: ui.navigate.to('/dang-nhap')).props('flat rounded size=md').classes('text-muted-foreground font-medium px-4 h-10 transition-all hover:bg-muted shrink-0')
                    ui.button(t('register'), on_click=lambda: ui.navigate.to('/dang-ky')).props('unelevated rounded size=md').classes('bg-primary text-white font-semibold px-6 h-10 shadow-md hover:brightness-110 shrink-0')
                
                # Mobile Menu Button (Visible on < md)
                mobile_btn = ui.button(icon='menu', on_click=lambda: drawer.open()).props('flat round size=md').classes('md:hidden text-primary bg-primary/5 ml-1 shrink-0')
                
                with ui.dialog() as drawer:
                    with ui.card().classes('w-screen max-w-[320px] h-full p-0 overflow-hidden flex flex-col bg-background'):
                        # Drawer Header
                        with ui.element('div').classes('p-6 bg-primary text-white flex flex-col gap-4'):
                            with ui.row().classes('justify-between items-center'):
                                ui.label('DANH MỤC').classes('font-black tracking-[0.2em] text-sm opacity-80')
                                ui.button(icon='close', on_click=drawer.close).props('flat round color=white size=md')
                            
                            if app.storage.user.get('is_authenticated'):
                                with ui.row().classes('items-center gap-3 mt-4'):
                                    ui.avatar('account_circle', color='white', text_color='primary').classes('shadow-lg')
                                    with ui.column().classes('gap-0'):
                                        ui.label(app.storage.user.get('user_name', 'Người dùng')).classes('font-bold leading-tight')
                                        ui.label('Thành viên Quan họ').classes('text-[10px] opacity-70 uppercase font-black')
                            else:
                                ui.label('Chào mừng bạn!').classes('text-xl font-display font-bold')

                        # Drawer Links
                        with ui.scroll_area().classes('flex-1'):
                            with ui.column().classes('p-6 gap-2 w-full'):
                                for path, key, label in nav_items:
                                    is_active = (current_path == path)
                                    with ui.link(target=path).classes('w-full no-underline').on('click', drawer.close):
                                        with ui.element('div').classes(
                                            f'w-full px-4 py-4 rounded-xl flex items-center gap-4 transition-all '
                                            f'{"bg-primary/10 text-primary border-l-4 border-primary shadow-sm" if is_active else "text-muted-foreground hover:bg-muted/50"}'
                                        ):
                                            icon_map = {
                                                'home': 'home', 'intro': 'info', 'songs': 'music_note', 
                                                'artists': 'groups', 'villages': 'map', 'news': 'article'
                                            }
                                            ui.icon(icon_map.get(key, 'circle'), size='24px')
                                            ui.label(label).classes('font-bold text-base')

                                # Auth section for Mobile
                                ui.separator().classes('my-4 opacity-50')
                                if app.storage.user.get('is_authenticated'):
                                    with ui.link(target='/ho-so').classes('w-full no-underline').on('click', drawer.close):
                                        with ui.element('div').classes('w-full px-4 py-4 rounded-xl flex items-center gap-4 text-muted-foreground hover:bg-muted/50'):
                                            ui.icon('settings', size='24px')
                                            ui.label('Quản lý tài khoản').classes('font-bold')
                                    ui.button(t('logout'), icon='logout', on_click=api_client.logout).props('flat rounded size=lg').classes('w-full text-destructive mt-4 font-bold')
                                else:
                                    with ui.column().classes('w-full gap-3 mt-2'):
                                        ui.button(t('login'), icon='login', on_click=lambda: (ui.navigate.to('/dang-nhap'), drawer.close())).props('outline rounded size=lg').classes('w-full text-primary font-bold h-14')
                                        ui.button(t('register'), icon='person_add', on_click=lambda: (ui.navigate.to('/dang-ky'), drawer.close())).props('unelevated rounded size=lg').classes('w-full bg-primary text-white font-bold h-14 shadow-md')

                pass # mobile_btn handles open

def footer():
    with ui.element('footer').classes('w-full border-t border-border bg-card mt-auto shrink-0'):
        with ui.element('div').classes('mx-auto max-w-7xl px-4 py-12'):
            with ui.element('div').classes('grid grid-cols-1 gap-12 md:grid-cols-4'):
                # Column 1: Brand
                with ui.column().classes('gap-4'):
                    with ui.row().classes('items-center gap-2'):
                        ui.image('/static/common/lotus-ornament.png').classes('h-8 w-8')
                        ui.label('Quan Họ Bắc Ninh').classes('font-display text-lg font-bold text-primary')
                    ui.label(t('footer_brand_desc')).classes('text-sm text-muted-foreground leading-relaxed')

                # Column 2: Explore
                with ui.column().classes('gap-3'):
                    ui.label(t('footer_explore')).classes('font-display text-sm font-semibold text-foreground mb-1')
                    for key, path in [
                        ('intro',   '/gioi-thieu'),
                        ('songs',      '/bai-hat'),
                        ('artists',    '/nghe-nhan'),
                        ('villages', '/lang-quan-ho'),
                    ]:
                        ui.link(t(key), target=path).classes('text-sm text-muted-foreground hover:text-primary no-underline transition-colors')

                # Column 3: Contact
                with ui.column().classes('gap-3'):
                    ui.label(t('footer_contact')).classes('font-display text-sm font-semibold text-foreground mb-1')
                    ui.label('Sở Văn hóa, Thể thao và Du lịch tỉnh Bắc Ninh').classes('text-sm text-muted-foreground')
                    ui.label('Email: quanho@bacninh.gov.vn').classes('text-sm text-muted-foreground')

                # Column 4: Social Media
                with ui.column().classes('gap-3'):
                    ui.label(t('footer_connect')).classes('font-display text-sm font-semibold text-foreground mb-1')
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
        ui.image('/static/common/lotus-ornament.png').classes('mx-auto mb-2 h-10 w-10 opacity-70')
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
    # Account for fixed navbar height (56px) - Reduced for compact look
    with ui.element('section').classes('bg-card/30 pt-16 pb-8 border-b border-border w-full flex justify-center').style('padding-top: 80px;'):
        with theme.container().classes('text-center'):
            ui.image('/static/common/lotus-ornament.png').classes('mb-6 h-12 w-12 mx-auto')
            ui.label(title).classes('font-display text-5xl font-black text-foreground mb-4 tracking-tight')
            ui.label(subtitle).classes('max-w-2xl mx-auto text-lg text-muted-foreground font-light leading-relaxed')
