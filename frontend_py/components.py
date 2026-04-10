from nicegui import ui, app
import theme

def navbar():
    # Detect current path for active state
    current_path = ui.context.client.page.path if hasattr(ui.context, 'client') and hasattr(ui.context.client, 'page') else '/'
    
    with ui.element('header').classes('sticky top-0 z-50 w-full border-b border-border bg-background/90 backdrop-blur-md'):
        with theme.container().classes('flex h-16 items-center justify-between px-4'):
            # Logo
            with ui.link(target='/').classes('flex items-center gap-2 no-underline transition-opacity hover:opacity-80'):
                ui.image('/static/lotus-ornament.png').classes('h-8 w-8')
                with ui.element('span').classes('font-display text-xl font-bold text-primary'):
                    ui.label('Quan Họ ')
                    ui.label('Bắc Ninh').classes('text-accent')

            # Nav Items (Desktop)
            with ui.row().classes('hidden items-center gap-1 lg:flex'):
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
                        f'rounded-md px-3 py-2 text-sm font-medium transition-colors hover:bg-muted hover:text-primary no-underline '
                        f'{"bg-muted text-primary font-semibold" if is_active else "text-muted-foreground"}'
                    )

            # Desktop Actions
            with ui.row().classes('flex items-center gap-2'):
                # Search
                ui.button(icon='search').props('flat round size=sm').classes('text-muted-foreground hover:text-primary')
                
                # Theme Toggle (Simplified for now)
                ui.button(icon='dark_mode').props('flat round size=sm').classes('text-muted-foreground hover:text-primary')
                
                # Language Toggle
                ui.label('VI').classes('flex h-9 w-9 items-center justify-center rounded-md text-sm font-bold text-muted-foreground transition-colors hover:bg-muted hover:text-primary cursor-pointer')
                
                # Auth Buttons
                with ui.row().classes('hidden sm:flex items-center gap-1'):
                    ui.button('Đăng nhập', icon='login').props('flat rounded size=sm').classes('text-muted-foreground font-medium px-3')
                    ui.button('Đăng ký', icon='person_add').props('unelevated rounded size=sm').classes('bg-primary text-primary-foreground font-semibold px-4 shadow-sm hover:bg-primary/90')
                
                # Mobile Menu Trigger
                mobile_btn = ui.button(icon='menu').props('flat round').classes('lg:hidden text-muted-foreground')
                
                with ui.dialog() as drawer:
                    with ui.card().classes('w-72 h-full p-0 overflow-hidden'):
                        with ui.column().classes('p-4 gap-1'):
                            with ui.row().classes('justify-between items-center mb-6 px-2'):
                                ui.label('Menu').classes('font-bold text-lg')
                                ui.button(icon='close', on_click=drawer.close).props('flat round size=sm')
                            
                            for path, key, label in nav_items:
                                is_active = (current_path == path)
                                ui.link(label, target=path).classes(
                                    f'w-full px-4 py-3 rounded-md transition-colors no-underline '
                                    f'{"bg-muted text-primary font-bold" if is_active else "text-muted-foreground hover:bg-muted/50"}'
                                )
                            
                            # Mobile Auth
                            ui.element('div').classes('mt-4 border-t border-border pt-4 px-2 space-y-2')
                            ui.button('Đăng nhập', icon='login').props('flat rounded size=md').classes('w-full text-muted-foreground justify-start')
                            ui.button('Đăng ký', icon='person_add').props('unelevated rounded size=md').classes('w-full bg-primary text-primary-foreground justify-start px-4')
                
                mobile_btn.on_click(drawer.open)


def footer():
    with ui.element('footer').classes('w-full border-t border-border bg-card mt-auto shrink-0'):
        with ui.element('div').classes('mx-auto max-w-7xl px-4 py-12'):
            with ui.element('div').classes('grid grid-cols-1 gap-12 md:grid-cols-3'):
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

            # Bottom Bar
            ui.element('div').classes('mt-12 border-t border-border pt-8 text-center')
            ui.label('© 2026 Quan Họ Bắc Ninh. Di sản văn hóa phi vật thể của nhân loại.').classes('text-xs text-muted-foreground')


def hero_banner():
    with ui.element('section').classes('relative flex min-h-[70vh] items-center overflow-hidden w-full'):
        # Background Image
        ui.image('/static/hero-banner.jpg').classes('absolute inset-0 h-full w-full object-cover')
        # Overlay
        ui.element('div').classes('absolute inset-0 bg-hero-gradient opacity-70')
        
        # Content
        with ui.element('div').classes('relative z-10 container mx-auto px-4 py-20 text-center flex flex-col items-center'):
            ui.label('DI SẢN VĂN HÓA PHI VẬT THỂ UNESCO').classes(
                'mb-4 text-sm font-medium uppercase tracking-[0.3em] text-gold-light'
            ).style('animation: fade-in-up 0.8s ease-out')
            
            with ui.column().classes('gap-0 flex flex-col items-center').style('animation: fade-in-up 1s ease-out 0.2s both'):
                ui.label('Quan Họ').classes('font-display text-5xl font-bold leading-tight text-white md:text-7xl lg:text-8xl')
                ui.label('Bắc Ninh').classes('font-display text-5xl font-bold leading-tight text-gradient-gold md:text-7xl lg:text-8xl')
            
            ui.label(
                'Khám phá vẻ đẹp tinh tế của dân ca Quan họ — '
                'tiếng hát giao duyên ngọt ngào bên dòng sông Cầu xứ Kinh Bắc.'
            ).classes('mx-auto mt-8 max-w-2xl text-lg text-white/80 leading-relaxed md:text-xl').style('animation: fade-in-up 1s ease-out 0.4s both')
            
            with ui.row().classes('mt-10 flex flex-wrap justify-center gap-4').style('animation: fade-in-up 1s ease-out 0.6s both'):
                ui.button('Nghe ngay', icon='play_arrow', on_click=lambda: ui.navigate.to('/bai-hat')).props('unelevated rounded-lg').classes(
                    'bg-accent text-accent-foreground font-bold px-8 py-4 shadow-elevated transform transition-transform hover:scale-105'
                )
                ui.button('Tìm hiểu thêm', on_click=lambda: ui.navigate.to('/gioi-thieu')).props('outline rounded-lg').classes(
                    'border-white/30 text-white font-bold px-8 py-4 hover:bg-white/10'
                )

def section_title(title, subtitle=None):
    with ui.column().classes('mb-12 text-center w-full items-center gap-2'):
        ui.image('/static/lotus-ornament.png').classes('mx-auto mb-2 h-10 w-10 opacity-70')
        ui.label(title).classes('font-display text-3xl font-bold text-foreground md:text-4xl')
        if subtitle:
            ui.label(subtitle).classes('mx-auto max-w-2xl text-muted-foreground')

def song_card(title, artist, image_url, melody=None, duration=None):
    with ui.element('div').classes('relative group'):
        # Favorite button
        with ui.element('div').classes(
            'absolute right-3 top-3 z-10 flex h-8 w-8 items-center justify-center rounded-full '
            'bg-background/80 text-muted-foreground backdrop-blur-sm cursor-pointer '
            'hover:bg-primary hover:text-white transition-all shadow-sm'
        ):
            ui.icon('favorite_border', size='18px')
            
        with ui.card().classes(
            'group overflow-hidden rounded-lg border border-border bg-card shadow-card '
            'hover:shadow-elevated transition-all p-0'
        ):
            # Thumbnail
            with ui.element('div').classes('relative aspect-[4/3] overflow-hidden'):
                ui.image(image_url).classes('h-full w-full object-cover transition-transform duration-500 group-hover:scale-110')
                # Play overlay
                with ui.element('div').classes(
                    'absolute inset-0 flex items-center justify-center bg-black/0 '
                    'group-hover:bg-black/30 transition-all'
                ):
                    with ui.element('div').classes(
                        'flex h-12 w-12 scale-0 items-center justify-center rounded-full '
                        'bg-primary text-white transition-transform group-hover:scale-100 shadow-lg'
                    ):
                        ui.icon('play_arrow', size='24px')
            
            # Info
            with ui.column().classes('p-5 gap-1'):
                ui.label(title).classes('font-display text-base font-bold text-foreground line-clamp-1 group-hover:text-primary transition-colors')
                ui.label(artist).classes('text-sm text-muted-foreground font-medium')
                
                with ui.row().classes('mt-3 flex items-center gap-4 text-[11px] text-muted-foreground font-medium'):
                    with ui.row().classes('items-center gap-1'):
                        ui.icon('music_note', size='14px').classes('text-primary/70')
                        ui.label(melody or 'Làn điệu cổ')
                    with ui.row().classes('items-center gap-1'):
                        ui.icon('schedule', size='14px').classes('text-primary/70')
                        ui.label(duration or '03:45')

def artist_card(name, photo_url, title, index=0):
    with ui.card().classes(
        'group overflow-hidden rounded-lg border border-border bg-card shadow-card '
        'hover:shadow-elevated transition-all p-0 cursor-pointer'
    ):
        with ui.element('div').classes('relative aspect-square overflow-hidden'):
            ui.image(photo_url).classes('h-full w-full object-cover transition-transform duration-500 group-hover:scale-105')
            with ui.element('div').classes('absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 to-transparent p-4'):
                ui.label(name).classes('font-display text-lg font-bold text-white')
        
        with ui.column().classes('p-4 gap-2'):
            with ui.row().classes('items-center gap-2 text-sm text-muted-foreground'):
                ui.icon('place', size='16px').classes('text-primary')
                ui.label(f'Làng {title or "Kinh Bắc"}')
            with ui.row().classes('items-center gap-2 text-sm text-muted-foreground'):
                ui.icon('workspace_premium', size='16px').classes('text-gold')
                ui.label(f'{12 + index} bài hát')

def news_card(title, image_url, type='Tin tức', date='--/--/----'):
    with ui.element('div').classes('group relative overflow-hidden'):
        with ui.link().classes(
            'flex gap-4 rounded-lg border border-border bg-background p-4 shadow-card '
            'transition-all hover:shadow-elevated hover:border-primary/50 no-underline'
        ):
            ui.image(image_url).classes('h-24 w-24 flex-shrink-0 rounded-md object-cover transition-transform duration-500 group-hover:scale-105')
            
            with ui.column().classes('min-w-0 flex-1'):
                ui.label(type).classes('inline-block rounded bg-primary/10 px-2 py-0.5 text-[10px] font-bold text-primary uppercase tracking-wider')
                ui.label(title).classes('mt-1 line-clamp-2 font-display text-sm font-bold text-foreground group-hover:text-primary transition-colors leading-snug')
                with ui.row().classes('mt-2 items-center gap-1 text-[11px] text-muted-foreground'):
                    ui.icon('calendar_today', size='12px')
                    ui.label(date)

def hero_stats_section():
    with ui.element('section').classes('bg-card py-20 border-y border-border w-full'):
        with theme.container().classes('grid items-center gap-16 md:grid-cols-2'):
            # Left side
            with ui.column().classes('gap-4'):
                with ui.element('h2').classes('font-display text-3xl font-bold text-foreground md:text-4xl lg:text-5xl'):
                    ui.label('Sức sống mãnh liệt của ')
                    ui.label('Di sản văn hóa').classes('text-primary')
                
                ui.label(
                    'Dân ca Quan họ Bắc Ninh không chỉ là một hình thức ca hát, mà còn là biểu hiện cao nhất '
                    'của sự thanh lịch, văn minh và nghĩa tình của người dân xứ Bắc.'
                ).classes('leading-relaxed text-muted-foreground text-lg md:text-xl')
                
                with ui.link(target='/gioi-thieu').classes('mt-4 no-underline'):
                    with ui.button('Khám phá lịch sử', icon='arrow_forward').props('unelevated rounded-lg').classes(
                        'bg-primary text-white font-bold px-8 py-3 shadow-md hover:shadow-lg transition-all transform hover:scale-105'
                    ):
                        pass
            
            # Right side: Stats grid
            with ui.element('div').classes('grid grid-cols-2 gap-4'):
                stats = [
                    ('49', 'Làng Quan họ gốc', 'text-primary', 'groups'),
                    ('300+', 'Làn điệu cổ', 'text-accent', 'music_note'),
                    ('2009', 'UNESCO công nhận', 'text-terracotta', 'stars'),
                    ('600+', 'Năm lịch sử', 'text-jade', 'history')
                ]
                for val, label, color_class, icon in stats:
                    with ui.element('div').classes('rounded-xl bg-muted/50 p-6 text-center border border-border/50 shadow-sm transition-all hover:shadow-md'):
                        ui.icon(icon, size='32px').classes(f'{color_class} mb-2 opacity-80')
                        ui.label(val).classes(f'font-display text-3xl font-bold {color_class} mb-1')
                        ui.label(label).classes('text-[10px] font-bold text-muted-foreground uppercase tracking-widest')

def chatbot_persona():
    with ui.element('div').classes('fixed bottom-8 right-8 z-[100] chat-persona'):
        with ui.link(target='/chatbot').classes('block no-underline'):
            with ui.element('div').classes('relative group'):
                with ui.element('div').classes('h-16 w-16 rounded-full border-4 border-white shadow-elevated overflow-hidden bg-white'):
                    ui.image('/static/chatbot-avatar.png').classes('h-full w-full object-cover')
                with ui.element('div').classes('absolute -top-1 -right-1 bg-green-500 h-4 w-4 rounded-full border-2 border-white shadow-sm'):
                    pass
                ui.label('Bạn cần giúp đỡ?').classes(
                    'absolute right-20 top-1/2 -translate-y-1/2 bg-white px-4 py-2 rounded-lg '
                    'text-sm font-bold text-foreground shadow-lg opacity-0 group-hover:opacity-100 '
                    'transition-opacity whitespace-nowrap pointer-events-none'
                )

def intro_feature_card(icon_name, title, desc):
    with ui.card().classes(
        'group relative overflow-hidden rounded-2xl border border-border bg-background p-8 '
        'shadow-sm transition-all hover:-translate-y-1 hover:shadow-elevated hover:border-primary/50'
    ):
        with ui.element('div').classes('mb-6 inline-flex h-14 w-14 items-center justify-center rounded-xl bg-primary/10 transition-colors group-hover:bg-primary/20'):
            ui.icon(icon_name, size='24px').classes('text-primary')
        ui.label(title).classes('mb-4 font-display text-2xl font-bold text-foreground')
        ui.label(desc).classes('text-muted-foreground leading-relaxed')

def costume_block(title, desc, image_url, items=None, reverse=False):
    classes = 'flex flex-col items-center gap-10 md:flex-row' + ('-reverse' if reverse else '')
    with ui.element('div').classes(classes + ' w-full py-12'):
        with ui.element('div').classes('md:w-1/2 relative w-full'):
            ui.element('div').classes(f'absolute -inset-4 rounded-2xl bg-gradient-to-{"l" if reverse else "r"} from-primary/20 to-transparent blur-xl opacity-50')
            ui.image(image_url).classes('relative rounded-2xl shadow-elevated object-cover aspect-video w-full')
        with ui.column().classes('md:w-1/2 space-y-4 px-4 w-full'):
            ui.label(title).classes(f'font-display text-4xl font-bold { "text-foreground" if reverse else "text-primary"}')
            ui.label(desc).classes('text-lg text-muted-foreground leading-relaxed')
            if items:
                with ui.column().classes('space-y-2 mt-4 text-muted-foreground'):
                    for item in items:
                        with ui.row().classes('items-center gap-2'):
                            ui.icon('check_circle', size='20px').classes('text-accent')
                            ui.label(item)

def timeline_item(year, text, is_last=False):
    with ui.row().classes('group relative flex flex-col md:flex-row gap-8 w-full'):
        with ui.element('div').classes('md:w-1/3 text-left md:text-right shrink-0 pt-1'):
            ui.label(year).classes('font-display text-3xl font-bold text-primary group-hover:text-accent transition-colors')
        with ui.column().classes('hidden md:flex flex-col items-center'):
            with ui.element('div').classes('flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full border-4 border-background bg-primary text-primary-foreground shadow-sm group-hover:scale-110 transition-transform'):
                ui.element('div').classes('h-2 w-2 rounded-full bg-white')
            if not is_last:
                ui.element('div').classes('w-0.5 flex-1 bg-gradient-to-b from-primary/50 to-transparent mt-2 opacity-50')
        with ui.element('div').classes('md:w-2/3 pb-8 md:pb-0 w-full'):
            with ui.card().classes('rounded-xl bg-background p-6 border border-border shadow-sm group-hover:shadow-md transition-shadow'):
                ui.label(text).classes('text-muted-foreground leading-relaxed text-lg')

def unesco_quote(text, subtitle=None):
    with ui.column().classes('mt-10 items-center w-full'):
        if subtitle:
            ui.label(subtitle).classes('text-primary font-bold tracking-widest text-xs mb-4 opacity-70')
        with ui.element('blockquote').classes('text-xl font-light italic leading-loose text-muted-foreground px-8 border-l-4 border-primary bg-card/30 py-6 rounded-r-xl shadow-sm w-full'):
            ui.label(f'"{text}"')

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
    with ui.element('section').classes('bg-card/30 pt-32 pb-20 border-b border-border w-full flex justify-center'):
        with theme.container().classes('text-center'):
            ui.image('/static/lotus-ornament.png').classes('mb-6 h-12 w-12 mx-auto')
            ui.label(title).classes('font-display text-5xl font-black text-foreground mb-4 tracking-tight')
            ui.label(subtitle).classes('max-w-2xl mx-auto text-lg text-muted-foreground font-light leading-relaxed')
