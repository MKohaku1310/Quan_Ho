from nicegui import ui, app
import theme

def navbar():
    # Detect current path for active state
    current_path = ui.context.client.page.path if hasattr(ui.context, 'client') and hasattr(ui.context.client, 'page') else '/'
    
    # Glassmorphism navbar – using ui.header to ensure it sticks to the top correctly
    with ui.header().classes('qh-navbar fixed top-0 left-0 right-0 z-[100] w-full transition-all duration-300').style(
        'background: rgba(255, 248, 240, 0.75); '
        'backdrop-filter: blur(16px) saturate(180%); '
        '-webkit-backdrop-filter: blur(16px) saturate(180%); '
        'border-bottom: 0.5px solid rgba(180, 120, 60, 0.1); '
        'box-shadow: 0 4px 30px rgba(0, 0, 0, 0.05);'
    ).props('elevated=false'):
        with theme.container().classes('flex h-14 items-center px-4'):
            # 1. Left: Logo (Container flex-1 to push center)
            with ui.element('div').classes('flex-1 flex justify-start items-center'):
                with ui.link(target='/').classes('flex items-center gap-2 no-underline transition-opacity hover:opacity-80 shrink-0'):
                    ui.image('/static/lotus-ornament.png').classes('h-7 w-7')
                    ui.label('Quan Họ Bắc Ninh').classes('font-display text-lg font-bold text-primary whitespace-nowrap')

            # 2. Center: Nav Items (Desktop)
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

            # 3. Right: Actions (Container flex-1 to push center)
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

            # Bottom Bar — Premium copyright bar
            ui.element('div').classes('mt-12 border-t border-border pt-8')
            with ui.row().classes('w-full justify-between items-center gap-4 flex-wrap'):
                with ui.row().classes('items-center gap-2'):
                    ui.label('© 2024 Quan Họ Bắc Ninh.').classes('text-xs font-bold text-foreground')
                    ui.label('Trân quý và bảo tồn di sản thế giới.').classes('text-xs text-muted-foreground')
                
                with ui.row().classes('gap-4'):
                    for link_label in ['Điều khoản', 'Bảo mật', 'Liên hệ']:
                        ui.link(link_label, '#').classes('text-[10px] uppercase tracking-widest font-bold text-muted-foreground hover:text-primary no-underline transition-colors')


def hero_banner():
    # Extra top padding to compensate for fixed navbar
    with ui.element('section').classes('relative flex min-h-[85vh] items-center overflow-hidden w-full').style('padding-top: 56px;'):
        # Background Image
        ui.image('/static/hero-banner.jpg').classes('absolute inset-0 h-full w-full object-cover')
        # Overlay
        ui.element('div').classes('absolute inset-0 bg-hero-gradient opacity-70')
        
        # Content
        with ui.element('div').classes('relative z-10 container mx-auto px-4 py-20 text-center flex flex-col items-center'):
            ui.label('DI SẢN VĂN HÓA PHI VẬT THỂ UNESCO').classes(
                'mb-4 text-sm font-medium uppercase tracking-[0.3em] text-gold-light'
            ).style('animation: fade-in-up 0.8s ease-out')
            
            with ui.column().classes('gap-2 flex flex-col items-center').style('animation: fade-in-up 1s ease-out 0.2s both'):
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
        
        # Animated scroll-down indicator
        with ui.element('div').classes('absolute bottom-8 left-1/2 -translate-x-1/2 z-10 flex flex-col items-center gap-2 cursor-pointer').style(
            'animation: float 2s ease-in-out infinite;'
        ):
            ui.label('Cuộn xuống').classes('text-white/60 text-xs uppercase tracking-widest font-medium')
            ui.icon('keyboard_arrow_down', size='28px').classes('text-white/70')

def section_title(title, subtitle=None):
    with ui.column().classes('mb-12 text-center w-full items-center gap-2'):
        ui.image('/static/lotus-ornament.png').classes('mx-auto mb-2 h-10 w-10 opacity-70')
        ui.label(title).classes('font-display text-3xl font-bold text-foreground md:text-4xl')
        if subtitle:
            ui.label(subtitle).classes('mx-auto max-w-2xl text-muted-foreground')

def song_card(id, title, artist, image_url, melody=None, duration=None):
    with ui.element('div').classes('relative group cursor-pointer').on('click', lambda: ui.navigate.to(f'/bai-hat/{id}')):
        # Favorite button (prevent event propagation)
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
            with ui.element('div').classes('relative aspect-[4/3] w-full overflow-hidden'):
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

def artist_card(id, name, photo_url, title, index=0):
    with ui.card().classes(
        'group overflow-hidden rounded-lg border border-border bg-card shadow-card '
        'hover:shadow-elevated transition-all p-0 cursor-pointer'
    ).on('click', lambda: ui.navigate.to(f'/nghe-nhan/{id}')):
        with ui.element('div').classes('relative aspect-square w-full overflow-hidden'):
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

def news_card(id, title, image_url, type='Tin tức', date='--/--/----'):
    target = f'/su-kien/{id}' if type == 'Sự kiện' else f'/tin-tuc/{id}'
    with ui.element('div').classes('group relative overflow-hidden'):
        with ui.link(target=target).classes(
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
        'shadow-sm transition-all duration-300 hover:-translate-y-2 hover:shadow-2xl hover:border-primary/40 '
        'h-full flex flex-col'
    ):
        # Decorative background pulse on hover
        ui.element('div').classes(
            'absolute -right-8 -top-8 h-32 w-32 rounded-full bg-primary/5 transition-transform '
            'duration-500 group-hover:scale-150'
        )
        
        with ui.element('div').classes(
            'mb-6 inline-flex h-14 w-14 items-center justify-center rounded-xl '
            'bg-primary/10 text-primary transition-all duration-300 '
            'group-hover:bg-primary group-hover:text-white group-hover:shadow-lg group-hover:shadow-primary/30'
        ):
            ui.icon(icon_name, size='24px')
            
        ui.label(title).classes('mb-4 font-display text-2xl font-bold text-foreground transition-colors group-hover:text-primary')
        ui.label(desc).classes('text-muted-foreground leading-relaxed flex-1')

def costume_block(title, desc, image_url, items=None, reverse=False):
    classes = 'flex flex-col items-center gap-16 md:flex-row' + ('-reverse' if reverse else '')
    with ui.element('div').classes(classes + ' w-full py-20 relative overflow-hidden'):
        # 1. Background Decoration (Ornament)
        ornament_pos = 'right-[-10%] top-1/2 -translate-y-1/2' if not reverse else 'left-[-10%] top-1/2 -translate-y-1/2'
        ui.image('/static/lotus-ornament.png').classes(
            f'absolute {ornament_pos} h-[400px] w-[400px] opacity-[0.04] pointer-events-none rotate-12 z-0'
        )

        # 2. Vertical Stamp Decoration
        stamp_pos = 'left-0' if not reverse else 'right-0'
        with ui.element('div').classes(f'absolute {stamp_pos} top-1/2 -translate-y-1/2 hidden lg:flex flex-col items-center gap-4 opacity-20 pointer-events-none z-0'):
            ui.element('div').classes('w-px h-24 bg-primary')
            ui.label('DI SẢN KINH BẮC').classes('text-[10px] font-bold tracking-[0.8em] text-primary uppercase [writing-mode:vertical-lr] rotate-180')
            ui.element('div').classes('w-px h-24 bg-primary')

        # 3. Image column
        with ui.element('div').classes('md:w-5/12 relative w-full group z-10'):
            # Ambient glow - matching the theme better
            ui.element('div').classes(
                f'absolute -inset-6 rounded-3xl bg-primary/5 blur-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-1000'
            )
            
            with ui.card().classes('relative rounded-3xl shadow-elevated overflow-hidden aspect-[4/5] w-full p-0 border-none group'):
                # Main Image
                img = ui.image(image_url).classes('h-full w-full object-cover relative z-10 transition-transform duration-1000 group-hover:scale-110')
                img.on('error', lambda: img.set_source('https://images.unsplash.com/photo-1599908608021-b5d929aa054e?auto=format&fit=crop&q=80&w=800'))
                
                # Overlay Gradient on image for depth
                ui.element('div').classes('absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-transparent opacity-60 z-20 group-hover:opacity-20 transition-opacity')

        # 4. Text column
        with ui.column().classes('md:w-7/12 space-y-8 px-6 w-full z-10'):
            with ui.column().classes('gap-3'):
                with ui.row().classes('items-center gap-3 animate-fade-in'):
                    ui.element('div').classes('h-px w-8 bg-primary/40')
                    ui.label('TRANG PHỤC TRUYỀN THỐNG').classes('text-xs font-bold tracking-[0.4em] text-primary/80 uppercase')
                
                ui.label(title).classes(f'font-display text-5xl font-black text-foreground leading-tight drop-shadow-sm')
            
            ui.label(desc).classes('text-xl text-muted-foreground leading-relaxed font-light max-w-2xl')
            
            if items:
                with ui.column().classes('w-full mt-4'):
                    with ui.row().classes('items-center gap-2 mb-6'):
                        ui.icon('auto_awesome', size='16px').classes('text-primary')
                        ui.label('Chi tiết đặc trưng:').classes('font-display text-sm font-bold text-primary uppercase tracking-widest')
                    
                    with ui.row().classes('grid grid-cols-1 sm:grid-cols-2 gap-6 w-full'):
                        for item in items:
                            # Rich item cards instead of simple list
                            with ui.card().classes('p-5 bg-card/40 border border-border/50 rounded-2xl shadow-sm hover:shadow-md hover:border-primary/20 transition-all group/item'):
                                with ui.row().classes('items-center gap-4'):
                                    with ui.element('div').classes('h-10 w-10 flex items-center justify-center rounded-xl bg-primary/5 text-primary group-hover/item:bg-primary group-hover/item:text-white transition-colors'):
                                        ui.icon('check_circle', size='20px')
                                    with ui.column().classes('gap-0'):
                                        ui.label(item).classes('text-sm font-bold text-foreground')
                                        ui.label('Yếu tố nghệ thuật tiêu biểu').classes('text-[10px] text-muted-foreground uppercase tracking-widest')

def timeline_item(year, text, index=0, total=4):
    is_even = index % 2 == 0
    is_last = index == total - 1
    
    with ui.row().classes(f'relative flex flex-col md:flex-row w-full {"md:flex-row-reverse" if not is_even else ""} items-center gap-8 mb-12'):
        # 1. Spacer/Content on one side
        with ui.element('div').classes('md:w-1/2 flex flex-col items-center ' + ('md:items-end md:pr-12' if is_even else 'md:items-start md:pl-12')):
            with ui.card().classes(
                'relative w-full max-w-md rounded-2xl p-6 border border-border bg-card shadow-sm '
                'hover:shadow-xl hover:border-primary/30 transition-all duration-300'
            ):
                # Adaptive arrow tip
                ui.element('div').classes(
                    'absolute top-1/2 -translate-y-1/2 w-4 h-4 bg-card border-l border-t border-border rotate-45 hidden md:block ' +
                    ('-right-2 rotate-[135deg]' if is_even else '-left-2 -rotate-45')
                )
                
                ui.label(year).classes('font-display text-2xl font-bold text-primary mb-2')
                ui.label(text).classes('text-muted-foreground leading-relaxed')

        # 2. Central Line and Dot
        with ui.element('div').classes('absolute left-1/2 -translate-x-1/2 h-full flex flex-col items-center z-10 hidden md:flex'):
            # Dot with glow
            with ui.element('div').classes('relative h-6 w-6 rounded-full bg-primary border-4 border-background shadow-lg'):
                ui.element('div').classes('absolute -inset-2 bg-primary/20 rounded-full animate-ping')
            
            if not is_last:
                ui.element('div').classes('w-0.5 flex-1 bg-gradient-to-b from-primary via-primary/50 to-transparent')

        # 3. Year for mobile (displayed above card if needed, but we put it in card for simplicity)
        # 4. Spacer on the other side
        with ui.element('div').classes('md:w-1/2 hidden md:block') : pass

def unesco_quote(text, subtitle=None):
    with ui.column().classes('items-center w-full py-2'):
        if subtitle:
            ui.label(subtitle).classes('text-primary font-bold tracking-[0.3em] text-[10px] mb-4 opacity-80')
        with ui.element('blockquote').classes('relative text-2xl font-light italic leading-loose text-muted-foreground px-12 py-4'):
            # Large quote marks
            ui.label('“').classes('absolute top-0 left-0 text-7xl text-primary/10 font-serif leading-none')
            ui.label(text).classes('relative z-10')
            ui.label('”').classes('absolute bottom-0 right-0 text-7xl text-primary/10 font-serif leading-none')
            
        # Attribution line
        with ui.row().classes('mt-4 items-center gap-3 opacity-70'):
            ui.element('div').classes('h-px w-10 bg-primary/30')
            ui.label('Nguồn: UNESCO, 2009').classes('text-xs font-semibold tracking-wider text-primary')

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
