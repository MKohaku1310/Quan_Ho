from nicegui import ui, app
import theme
from api import api_client
from translation import t, toggle_language

def navbar():
    # Xac dinh duong dan hien tai
    current_path = ui.context.client.page.path if hasattr(ui.context, 'client') and hasattr(ui.context.client, 'page') else '/'
    
    # Danh sach menu
    nav_items = [
        ('/', 'home', t('home')),
        ('/gioi-thieu', 'intro', t('intro')),
        ('/bai-hat', 'songs', t('songs')),
        ('/nghe-nhan', 'artists', t('artists')),
        ('/lang-quan-ho', 'villages', t('villages')),
        ('/tin-tuc', 'news', t('news')),
    ]

    # Thanh dieu huong
    with ui.header().classes('qh-navbar w-full').props('elevated=false'):
        with theme.container().classes('flex h-14 items-center px-4'):
            # Logo
            with ui.element('div').classes('flex-1 flex justify-start items-center'):
                with ui.link(target='/').classes('flex items-center gap-2 no-underline transition-opacity hover:opacity-80 shrink-0'):
                    ui.image('/static/common/lotus-ornament.png').classes('h-7 w-7')
                    with ui.row().classes('gap-1 items-baseline'):
                        ui.label('Quan Họ').classes('font-display text-lg font-bold text-primary whitespace-nowrap')
                        ui.label('Bắc Ninh').classes('font-display text-lg font-bold text-[#d4af37] whitespace-nowrap')

            # Menu cho may tinh
            with ui.element('div').classes('flex max-md:hidden items-center justify-center gap-1 whitespace-nowrap px-2'):
                for path, key, label in nav_items:
                    is_active = (current_path == path)
                    ui.link(label, target=path).classes(
                        f'rounded-lg px-4 py-2 text-sm font-bold transition-all hover:bg-primary/10 hover:text-primary no-underline '
                        f'{"text-primary bg-primary/5 shadow-sm" if is_active else "text-muted-foreground"}'
                    )

            # Cac nut chuc nang
            with ui.element('div').classes('flex-1 flex justify-end items-center gap-1 sm:gap-2 flex-nowrap'):
                # Nut chuyen ngon ngu
                lang_label = t('language_toggle')
                ui.button(lang_label, on_click=lambda: (toggle_language(), ui.navigate.reload())).props('flat rounded size=md').classes('text-muted-foreground font-bold border border-border/50 px-2 min-w-0 h-9 shrink-0')

                # Nut dang nhap / dang ky
                with ui.element('div').classes('flex max-md:hidden items-center gap-2'):
                    if app.storage.user.get('is_authenticated'):
                        if app.storage.user.get('role') == 'admin':
                            ui.button('ADMIN', icon='dashboard', on_click=lambda: ui.navigate.to('/admin')).props('flat rounded size=md').classes('text-secondary font-black px-3 h-10 border border-secondary/20 hover:bg-secondary/10 shrink-0')
                        
                        ui.button(t('profile'), icon='account_circle', on_click=lambda: ui.navigate.to('/ho-so')).props('flat rounded size=md').classes('text-muted-foreground font-medium px-3 h-10 hover:bg-muted shrink-0')
                        ui.button(icon='logout', on_click=api_client.logout).props('flat round size=md').classes('text-destructive hover:bg-destructive/10 h-10 w-10 flex-shrink-0')
                    else:
                        ui.button(t('login'), on_click=lambda: ui.navigate.to('/dang-nhap')).props('flat rounded size=md').classes('text-muted-foreground font-medium px-4 h-10 transition-all hover:bg-muted shrink-0')
                        ui.button(t('register'), on_click=lambda: ui.navigate.to('/dang-ky')).props('unelevated rounded size=md').classes('bg-primary text-white font-semibold px-6 h-10 shadow-md hover:brightness-110 shrink-0')
                
                # Menu cho dien thoai
                mobile_btn = ui.button(icon='menu', on_click=lambda: drawer.open()).props('flat round size=md').classes('md:hidden text-primary bg-primary/5 ml-1 shrink-0')
                
                with ui.dialog() as drawer:
                    with ui.card().classes('w-screen max-w-[320px] h-full p-0 overflow-hidden flex flex-col bg-background'):
                        with ui.element('div').classes('p-6 bg-primary text-white flex flex-col gap-4'):
                            with ui.row().classes('justify-between items-center'):
                                ui.label(t('drawer_category')).classes('font-black tracking-[0.2em] text-sm opacity-80')
                                ui.button(icon='close', on_click=drawer.close).props('flat round color=white size=sm')
                            
                            if app.storage.user.get('is_authenticated'):
                                with ui.row().classes('items-center gap-3 mt-4'):
                                    ui.avatar('account_circle', color='white', text_color='primary').classes('shadow-lg')
                                    with ui.column().classes('gap-0'):
                                        ui.label(app.storage.user.get('user_name', t('anonymous'))).classes('font-bold leading-tight')
                                        ui.label(t('drawer_member')).classes('text-[10px] opacity-70 uppercase font-black')
                            else:
                                ui.label(t('drawer_guest')).classes('text-xl font-display font-bold')

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

                                ui.separator().classes('my-4 opacity-50')
                                if app.storage.user.get('is_authenticated'):
                                    with ui.link(target='/ho-so').classes('w-full no-underline').on('click', drawer.close):
                                        with ui.element('div').classes('w-full px-4 py-4 rounded-xl flex items-center gap-4 text-muted-foreground hover:bg-muted/50'):
                                            ui.icon('settings', size='24px')
                                            ui.label(t('drawer_manage_account')).classes('font-bold')
                                    ui.button(t('logout'), icon='logout', on_click=api_client.logout).props('flat rounded size=lg').classes('w-full text-destructive mt-4 font-bold')
                                else:
                                    with ui.column().classes('w-full gap-3 mt-2'):
                                        ui.button(t('login'), icon='login', on_click=lambda: (ui.navigate.to('/dang-nhap'), drawer.close())).props('outline rounded size=lg').classes('w-full text-primary font-bold h-14')
                                        ui.button(t('register'), icon='person_add', on_click=lambda: (ui.navigate.to('/dang-ky'), drawer.close())).props('unelevated rounded size=lg').classes('w-full bg-primary text-white font-bold h-14 shadow-md')


def footer():
    # Phan chan trang
    with ui.element('footer').classes('w-full bg-[#2d1a12] text-[#f5f5f0]/70 mt-auto shrink-0 relative overflow-hidden'):
        ui.element('div').classes('w-full h-[2px] bg-gradient-to-r from-transparent via-[#d68e33] to-transparent opacity-60')
        with ui.element('div').classes('absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 h-12 w-12 bg-[#2d1a12] rounded-full flex items-center justify-center border border-[#d68e33]/30 shadow-xl z-10'):
            ui.image('/static/common/lotus-ornament.png').classes('h-6 w-6 animate-spin-slow opacity-80')

        with ui.element('div').classes('mx-auto max-w-7xl px-6 py-20 relative z-0'):
            ui.image('/static/common/lotus-pattern.png').classes('absolute -right-20 -bottom-20 w-80 opacity-[0.04] pointer-events-none brightness-0 invert')

            with ui.element('div').classes('grid grid-cols-1 gap-y-12 gap-x-8 lg:grid-cols-12'):
                # Thong tin thuong hieu
                with ui.column().classes('lg:col-span-4 gap-6'):
                    with ui.row().classes('items-center gap-4'):
                        ui.image('/static/common/lotus-ornament.png').classes('h-12 w-12 brightness-0 invert opacity-90')
                        with ui.column().classes('gap-0'):
                            ui.label(t('hero_quan_ho') + ' ' + t('hero_bac_ninh')).classes('font-display text-3xl font-black text-[#f5f5f0] tracking-tight')
                            ui.label(t('heritage_kinh_bac')).classes('text-[10px] font-black tracking-[0.4em] text-[#d68e33]')
                    
                    ui.label(t('footer_brand_desc')).classes('text-sm leading-relaxed opacity-70 max-w-sm text-[#f5f5f0] font-light italic')
                    
                    with ui.row().classes('items-center gap-3 bg-white/5 p-4 rounded-2xl border border-white/5 mt-2 shadow-inner'):
                        ui.icon('verified', color='secondary', size='28px')
                        with ui.column().classes('gap-0'):
                            ui.label('UNESCO 2009').classes('text-xs font-black text-white tracking-wider')
                            ui.label(t('unesco_badge')).classes('text-[9px] opacity-60 uppercase tracking-[0.2em] font-bold')

                # Kham pha
                with ui.column().classes('lg:col-span-2 gap-8'):
                    ui.label(t('footer_explore')).classes('font-display text-[10px] font-black text-[#d68e33] tracking-[0.4em] uppercase opacity-80')
                    with ui.column().classes('gap-4'):
                        for key, path in [
                            ('home',       '/'),
                            ('intro',   '/gioi-thieu'),
                            ('songs',      '/bai-hat'),
                            ('artists',    '/nghe-nhan'),
                            ('villages', '/lang-quan-ho'),
                        ]:
                            ui.link(t(key), target=path).classes('text-sm text-[#f5f5f0]/70 hover:text-white no-underline transition-all hover:translate-x-1 font-medium')

                # Lien he
                with ui.column().classes('lg:col-span-3 gap-8'):
                    ui.label(t('footer_contact')).classes('font-display text-[10px] font-black text-[#d68e33] tracking-[0.4em] uppercase opacity-80')
                    with ui.column().classes('gap-6'):
                        with ui.row().classes('items-start gap-4 group cursor-pointer'):
                            ui.icon('place', size='22px', color='secondary').classes('group-hover:scale-110 transition-transform')
                            ui.label(t('footer_address')).classes('text-sm leading-relaxed text-[#f5f5f0]/70 group-hover:text-white transition-colors')
                        
                        with ui.row().classes('items-start gap-4 group cursor-pointer'):
                            ui.icon('mail', size='22px', color='secondary').classes('group-hover:scale-110 transition-transform')
                            ui.label('quanho@bacninh.gov.vn').classes('text-sm text-[#f5f5f0]/70 group-hover:text-white transition-colors')

                # Dang ky tin
                with ui.column().classes('lg:col-span-3 gap-8'):
                    ui.label(t('footer_newsletter_title')).classes('font-display text-[10px] font-black text-[#d68e33] tracking-[0.4em] uppercase opacity-80')
                    ui.label(t('footer_newsletter_desc')).classes('text-xs leading-relaxed opacity-50 text-[#f5f5f0] font-light')
                    
                    with ui.element('div').classes('w-full relative group'):
                        newsletter_input = ui.input(placeholder=t('email_field') + '...').props('dark borderless').classes('w-full bg-white/5 rounded-full px-6 text-sm border border-white/10 focus:border-[#d68e33]/50 transition-all h-12 text-white flex items-center')
                        with newsletter_input.add_slot('append'):
                            ui.button(icon='send', on_click=lambda: ui.notify(t('save_success'))).props('flat round dense color=secondary').classes('mr-2 hover:scale-125 transition-transform')

            # Thanh ban quyen
            ui.separator().classes('my-12 opacity-5 bg-white')
            with ui.row().classes('w-full justify-between items-center gap-10 flex-wrap'):
                from datetime import datetime
                current_year = datetime.now().year
                with ui.row().classes('items-center gap-8'):
                    ui.label(f'© {current_year} ' + t('hero_quan_ho') + ' ' + t('hero_bac_ninh') + '.').classes('text-xs font-bold text-[#f5f5f0]/30 tracking-wide')
                    with ui.row().classes('gap-8 hidden sm:flex'):
                        for link_key in ['footer_terms', 'footer_privacy', 'footer_contact_link']:
                            ui.link(t(link_key), '#').classes('text-[10px] uppercase tracking-[0.2em] font-black text-[#f5f5f0]/20 hover:text-[#d68e33] no-underline transition-colors')
                
                with ui.row().classes('gap-4'):
                    socials = [
                        ('mdi-facebook', 'https://facebook.com'),
                        ('mdi-youtube', 'https://youtube.com'),
                        ('mdi-instagram', 'https://instagram.com'),
                        ('mdi-twitter', 'https://twitter.com')
                    ]
                    for icon, link in socials:
                        with ui.element('a').classes('h-11 w-11 flex items-center justify-center rounded-xl bg-white/5 hover:bg-[#d68e33] hover:rotate-6 transition-all duration-300 group shadow-lg border border-white/5').props(f'href="{link}" target="_blank"'):
                            ui.icon(icon, color='white', size='22px').classes('group-hover:scale-110 transition-transform opacity-70 group-hover:opacity-100')

def section_title(title, subtitle=None):
    # Tieu de trang
    with ui.column().classes('mb-8 text-center w-full items-center gap-2'):
        ui.image('/static/common/lotus-ornament.png').classes('mx-auto mb-2 h-10 w-10 opacity-70')
        ui.label(title).classes('font-display text-3xl font-bold text-foreground md:text-4xl')
        if subtitle:
            ui.label(subtitle).classes('mx-auto max-w-2xl text-muted-foreground text-sm')

def filter_pills(options, active_option, on_change):
    # Bo loc
    with ui.row().classes('gap-3 mb-12'):
        for opt in options:
            is_active = opt == active_option
            ui.button(opt, on_click=lambda o=opt: on_change(o)).props('unelevated rounded-full' if is_active else 'outline rounded-full').classes(
                f'px-6 py-2 text-sm font-bold transition-all '
                f'{"bg-primary text-white shadow-md" if is_active else "text-muted-foreground border-border hover:border-primary hover:text-primary"}'
            )

def empty_state(message, icon='search_off'):
    # Trang thai trong
    with ui.column().classes('items-center justify-center py-32 w-full opacity-60 gap-4'):
        ui.icon(icon, size='64px').classes('text-muted-foreground/30')
        ui.label(message).classes('text-xl italic font-light tracking-wide')

def page_header(title, subtitle):
    # Dau trang
    with ui.element('section').classes('bg-card/30 pt-16 pb-8 border-b border-border w-full flex justify-center').style('padding-top: 80px;'):
        with theme.container().classes('text-center'):
            ui.image('/static/common/lotus-ornament.png').classes('mb-6 h-12 w-12 mx-auto')
            ui.label(title).classes('font-display text-5xl font-black text-foreground mb-4 tracking-tight')
            ui.label(subtitle).classes('max-w-2xl mx-auto text-lg text-muted-foreground font-light leading-relaxed')

def pagination_controls(state, total_count, on_change):
    # Dieu khien phan trang
    total_pages = (total_count + state.items_per_page - 1) // state.items_per_page
    if total_pages <= 1:
        return
        
    with ui.row().classes('w-full justify-center mt-12 gap-2 items-center'):
        ui.button(icon='chevron_left', on_click=lambda: (setattr(state, 'page', max(1, state.page-1)), on_change.refresh())) \
            .props('flat round dense').classes('text-primary').tooltip(t('prev_page'))
        
        max_btns = 5
        start_p = max(1, state.page - 2)
        end_p = min(total_pages, start_p + max_btns - 1)
        if end_p - start_p < max_btns - 1:
            start_p = max(1, end_p - max_btns + 1)
            
        if start_p > 1:
            ui.button('1', on_click=lambda: (setattr(state, 'page', 1), on_change.refresh())).props('flat round dense color=grey')
            if start_p > 2:
                ui.label('...').classes('text-muted-foreground')
            
        for p in range(start_p, end_p + 1):
            is_active = (p == state.page)
            ui.button(str(p), on_click=lambda p=p: (setattr(state, 'page', p), on_change.refresh())) \
                .props(f'flat round dense {"color=primary shadow-md bg-primary/10" if is_active else "color=grey"}') \
                .classes('font-bold text-sm width-8')
                
        if end_p < total_pages:
            if end_p < total_pages - 1:
                ui.label('...').classes('text-muted-foreground')
            ui.button(str(total_pages), on_click=lambda: (setattr(state, 'page', total_pages), on_change.refresh())).props('flat round dense color=grey')

        ui.button(icon='chevron_right', on_click=lambda: (setattr(state, 'page', min(total_pages, state.page+1)), on_change.refresh())) \
            .props('flat round dense').classes('text-primary').tooltip(t('next_page'))
