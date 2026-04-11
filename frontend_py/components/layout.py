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
    # Determine alignment for staggering effect
    alignment = 'self-start' if not reverse else 'self-end'
    
    with ui.card().classes(
        f'relative w-full max-w-[1000px] {alignment} overflow-hidden rounded-[2rem] border border-border/50 '
        f'bg-card/40 shadow-elevated hover:shadow-2xl transition-all duration-500 p-0 group z-10'
    ):
        # Background Decoration (Subtle Ornament)
        ui.image('/static/lotus-ornament.png').classes(
            'absolute right-[-5%] top-[-10%] h-[300px] w-[300px] opacity-[0.03] pointer-events-none rotate-12 z-0'
        )
        
        with ui.element('div').classes(f'flex flex-col md:flex-row' + ('-reverse' if reverse else '') + ' w-full h-full'):
            # 1. Image portion (Fixed aspect ratio on desktop, full width on mobile)
            with ui.element('div').classes('md:w-5/12 relative aspect-[4/5] md:aspect-auto overflow-hidden'):
                img = ui.image(image_url).classes(
                    'h-full w-full object-cover transition-transform duration-1000 group-hover:scale-105'
                )
                img.on('error', lambda: img.set_source('https://images.unsplash.com/photo-1599908608021-b5d929aa054e?auto=format&fit=crop&q=80&w=800'))
                
                # Overlay Gradient inside image
                ui.element('div').classes('absolute inset-0 bg-gradient-to-t from-black/20 via-transparent to-transparent opacity-60')
                
                # Decorative Label on Image
                with ui.element('div').classes('absolute bottom-4 left-4 bg-primary/90 text-white px-3 py-1 rounded-full backdrop-blur-sm z-20'):
                    ui.label('TRUYỀN THỐNG').classes('text-[10px] font-black tracking-widest')

            # 2. Content portion
            with ui.column().classes('md:w-7/12 p-8 md:p-12 justify-center gap-6 z-10'):
                with ui.column().classes('gap-2'):
                    with ui.row().classes('items-center gap-2 mb-2'):
                        ui.element('div').classes('h-px w-6 bg-primary/40')
                        ui.label('DI SẢN KINH BẮC').classes('text-[10px] font-bold tracking-[0.3em] text-primary/70 uppercase')
                    
                    ui.label(title).classes('font-display text-4xl font-black text-foreground leading-tight')
                
                ui.label(desc).classes('text-base text-muted-foreground leading-relaxed font-light')
                
                if items:
                    with ui.column().classes('w-full mt-2'):
                        with ui.row().classes('items-center gap-2 mb-4'):
                            ui.icon('auto_awesome', size='14px').classes('text-primary/60')
                            ui.label('Đặc trưng nghệ thuật:').classes('text-[10px] font-bold text-primary/70 uppercase tracking-widest')
                        
                        with ui.row().classes('grid grid-cols-1 sm:grid-cols-2 gap-3 w-full'):
                            for item in items:
                                with ui.card().classes('p-3 bg-white/50 border border-border/40 rounded-xl shadow-sm hover:border-primary/30 transition-all'):
                                    with ui.row().classes('items-center gap-2'):
                                        ui.icon('verified', size='14px').classes('text-primary')
                                        ui.label(item).classes('text-xs font-bold text-foreground truncate')

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
