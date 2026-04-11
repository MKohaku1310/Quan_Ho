from nicegui import ui
import theme

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

def costume_block(title, desc, image_url, items=None, reverse=False):
    classes = 'flex flex-col items-center gap-10 md:flex-row' + ('-reverse' if reverse else '')
    with ui.element('div').classes(classes + ' w-full py-12 relative overflow-hidden'):
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
            # Ambient glow
            ui.element('div').classes(
                f'absolute -inset-6 rounded-3xl bg-primary/5 blur-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-1000'
            )
            
            with ui.card().classes('relative rounded-3xl shadow-elevated overflow-hidden aspect-[4/5] w-full p-0 border-none group'):
                # Main Image
                img = ui.image(image_url).classes('h-full w-full object-cover relative z-10 transition-transform duration-1000 group-hover:scale-110')
                img.on('error', lambda: img.set_source('https://images.unsplash.com/photo-1599908608021-b5d929aa054e?auto=format&fit=crop&q=80&w=800'))
                
                # Overlay Gradient
                ui.element('div').classes('absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-transparent opacity-60 z-20 group-hover:opacity-20 transition-opacity')

        # 4. Text column
        with ui.column().classes('md:w-7/12 space-y-8 px-6 w-full z-10'):
            with ui.column().classes('gap-3'):
                with ui.row().classes('items-center gap-3 animate-fade-in'):
                    ui.element('div').classes('h-px w-8 bg-primary/40')
                    ui.label('TRANG PHỤC TRUYỀN THỐNG').classes('text-xs font-bold tracking-[0.4em] text-primary/80 uppercase')
                
                ui.label(title).classes(f'font-display text-5xl font-black text-foreground leading-tight drop-shadow-sm')
            
            ui.label(desc).classes('text-lg text-muted-foreground leading-relaxed font-light max-w-2xl')
            
            if items:
                with ui.column().classes('w-full mt-4'):
                    with ui.row().classes('items-center gap-2 mb-6'):
                        ui.icon('auto_awesome', size='16px').classes('text-primary')
                        ui.label('Chi tiết đặc trưng:').classes('font-display text-sm font-bold text-primary uppercase tracking-widest')
                    
                    with ui.row().classes('grid grid-cols-1 sm:grid-cols-2 gap-6 w-full'):
                        for item in items:
                            with ui.card().classes('p-4 bg-card/60 border border-border/80 rounded-2xl shadow-sm hover:shadow-md hover:border-primary/40 transition-all group/item'):
                                with ui.row().classes('items-center gap-3'):
                                    with ui.element('div').classes('h-8 w-8 flex items-center justify-center rounded-lg bg-primary/10 text-primary group-hover/item:bg-primary group-hover/item:text-white transition-colors'):
                                        ui.icon('verified', size='16px')
                                    with ui.column().classes('gap-0'):
                                        ui.label(item).classes('text-xs font-bold text-foreground')
                                        ui.label('Tinh hoa nghệ thuật').classes('text-[8px] text-muted-foreground uppercase tracking-widest')

def timeline_item(year, text, index=0, total=4):
    is_even = index % 2 == 0
    is_last = index == total - 1
    
    with ui.row().classes(f'relative flex flex-col md:flex-row w-full {"md:flex-row-reverse" if not is_even else ""} items-center gap-6 mb-6'):
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

        # 2. Central Line and Dot (The Silk Thread)
        with ui.element('div').classes('absolute left-1/2 -translate-x-1/2 h-full flex flex-col items-center z-10 hidden md:flex'):
            # The Silk Thread Line
            ui.element('div').classes('w-px flex-1 bg-gradient-to-b from-primary/30 via-primary to-primary/30 shadow-[0_0_10px_rgba(180,120,60,0.3)]')
            
            # Dot with glow
            with ui.element('div').classes('relative h-5 w-5 rounded-full bg-primary border-4 border-background shadow-lg my-1 scale-110'):
                ui.element('div').classes('absolute -inset-2 bg-primary/20 rounded-full animate-ping')
            
            if not is_last:
                ui.element('div').classes('w-px flex-1 bg-gradient-to-t from-primary/30 via-primary to-primary/30')

        # 3. Spacer on the other side
        with ui.element('div').classes('md:w-1/2 flex justify-center items-center px-12 md:px-0') : 
            if is_even:
                 ui.icon('history_edu', size='64px').classes('text-primary/5 opacity-50 rotate-12')
            else:
                 ui.icon('flare', size='64px').classes('text-primary/5 opacity-50 -rotate-12')

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
