from nicegui import ui
import theme

def hero_banner():
    with ui.element('section').classes('relative flex min-h-[92vh] items-center overflow-hidden w-full').style('padding-top: 56px;'):
        ui.image('/static/hero-banner-v2.png').classes('absolute inset-0 h-full w-full object-cover object-center')
        ui.element('div').classes('absolute inset-0 bg-hero-gradient opacity-70')
        
        with ui.element('div').classes('relative z-10 container mx-auto px-4 pt-20 pb-52 text-center flex flex-col items-center'):
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
        
        with ui.element('div').classes('absolute z-10 flex flex-col items-center gap-2 cursor-pointer group opacity-80').style(
            'bottom: 2rem; left: 50%; transform: translateX(-50%); animation: float 2s ease-in-out infinite;'
        ).on('click', lambda: ui.run_javascript(
            'document.getElementById("home-content").scrollIntoView({behavior: "smooth"})'
        )):
            ui.label('Cuộn xuống').classes('text-white text-xs uppercase tracking-widest font-medium group-hover:opacity-100')
            ui.icon('keyboard_arrow_down', size='28px').classes('text-white group-hover:opacity-100')

            
def hero_stats_section():
    with ui.element('section').classes('bg-card py-20 border-y border-border w-full'):
        with theme.container().classes('grid items-center gap-16 md:grid-cols-2'):
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
    alignment = 'self-start' if not reverse else 'self-end'
    
    with ui.card().classes(
        f'relative w-full max-w-[1000px] {alignment} overflow-hidden rounded-[2rem] border border-border/50 '
        f'bg-card/40 shadow-elevated hover:shadow-2xl transition-all duration-500 p-0 group z-10'
    ):
        ui.image('/static/lotus-ornament.png').classes(
            'absolute right-[-5%] top-[-10%] h-[300px] w-[300px] opacity-[0.03] pointer-events-none rotate-12 z-0'
        )
        
        with ui.element('div').classes(f'flex flex-col md:flex-row' + ('-reverse' if reverse else '') + ' w-full h-full'):
            with ui.element('div').classes('md:w-5/12 relative aspect-[4/5] md:aspect-auto overflow-hidden'):
                img = ui.image(image_url).classes(
                    'h-full w-full object-cover transition-transform duration-1000 group-hover:scale-105'
                )
                img.on('error', lambda: img.set_source('https://images.unsplash.com/photo-1599908608021-b5d929aa054e?auto=format&fit=crop&q=80&w=800'))
                ui.element('div').classes('absolute inset-0 bg-gradient-to-t from-black/20 via-transparent to-transparent opacity-60')
                with ui.element('div').classes('absolute bottom-4 left-4 bg-primary/90 text-white px-3 py-1 rounded-full backdrop-blur-sm z-20'):
                    ui.label('TRUYỀN THỐNG').classes('text-[10px] font-black tracking-widest')

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


# ─── Timeline helpers ────────────────────────────────────────────────────────

def _timeline_card(year: str, text: str):
    """Thẻ cuộn giấy dùng chung cho cả trái lẫn phải."""
    parts = year.rsplit(' ', 1)
    top_text, bottom_text = (parts[0], parts[1]) if len(parts) > 1 else (year[:2], year[2:])
    bottom_size = 'text-xl' if len(bottom_text) <= 5 else 'text-base'
    if len(bottom_text) > 9:
        bottom_size = 'text-[12px]'

    with ui.card().classes(
        'relative w-full max-w-sm p-0 overflow-hidden border-none shadow-elevated '
        'group/card bg-paper-texture transition-all duration-500 hover:-translate-y-2 z-20'
    ).style('box-shadow: 0 20px 40px -20px rgba(139, 0, 0, 0.3);'):
        ui.element('div').classes('absolute inset-3 border-2 border-[#d4af37]/40 pointer-events-none rounded-lg')
        ui.element('div').classes('absolute inset-[15px] border border-[#d4af37]/20 pointer-events-none rounded-sm')
        ui.image('/static/lotus-ornament.png').classes(
            'absolute -right-4 -bottom-4 h-32 w-32 opacity-[0.05] pointer-events-none '
            '-rotate-12 group-hover/card:scale-110 transition-transform'
        )
        with ui.column().classes('p-8 gap-4 relative z-10'):
            with ui.element('div').classes('flex items-center gap-4 mb-2'):
                with ui.element('div').classes(
                    'seal-stamped relative h-16 w-16 flex flex-col items-center '
                    'justify-center rounded-sm rotate-3 shadow-lg'
                ):
                    ui.label(top_text).classes('text-[10px] font-black text-white/90 leading-none tracking-widest uppercase')
                    ui.label(bottom_text).classes(f'{bottom_size} font-black text-white leading-none tracking-tighter mt-1 whitespace-nowrap overflow-hidden')
                    ui.element('div').classes('absolute inset-1.5 border border-white/20')
                with ui.column().classes('gap-0'):
                    ui.label('KỶ NGUYÊN').classes('text-[8px] font-black tracking-[0.4em] text-primary/50 uppercase')
                    ui.label('KINH BẮC').classes('text-[10px] font-bold text-primary/70 tracking-widest')
            ui.label(year).classes(
                'font-display text-3xl font-bold text-foreground mb-1 '
                'group-hover/card:text-primary transition-colors italic'
            )
            ui.label(text).classes('text-[15px] text-muted-foreground leading-relaxed italic font-light font-body')
            ui.element('div').classes('h-px w-1/2 bg-gradient-to-r from-transparent via-primary/20 to-transparent mt-2 mx-auto')


def _timeline_dot():
    """Nút dấu đỏ ở giữa, căn chỉnh với thẻ."""
    with ui.element('div').classes(
        'relative h-12 w-12 flex-shrink-0 flex items-center justify-center '
        'bg-primary border-2 border-[#d4af37]/60 shadow-elevated '
        'transition-all duration-300 hover:scale-125 cursor-pointer z-30 rotate-3'
    ):
        ui.element('div').classes('absolute inset-1.5 border border-white/20')
        ui.icon('adjust', size='24px').classes('text-white/40')
        ui.element('div').classes('absolute -inset-4 border border-primary/5 rounded-full animate-ping opacity-20')


def _timeline_ornament(flip: bool = False):
    """Hình trang trí ở phía trống."""
    rotate = '-rotate-12' if not flip else 'rotate-45'
    padding = 'pr-10' if not flip else 'pl-10'
    with ui.element('div').classes(
        f'opacity-[0.07] grayscale hover:grayscale-0 hover:opacity-100 '
        f'transition-all duration-1000 transform hover:scale-125 {padding}'
    ):
        ui.image('/static/lotus-ornament.png').classes(f'h-24 w-24 {rotate}')


def timeline_item(year: str, text: str, index: int = 0, total: int = 4):
    """
    Layout 3 cột: [45% nội dung/trống] [10% nút đỏ] [45% trống/nội dung]
    Chẵn → thẻ bên TRÁI, lẻ → thẻ bên PHẢI.
    Nút đỏ luôn ở giữa, thẳng hàng với thẻ nhờ items-center trên row.
    """
    is_even = index % 2 == 0

    with ui.row().classes('relative flex flex-row items-center w-full my-8'):

        # ── Cột TRÁI (45%) ──────────────────────────────────────────────────
        with ui.element('div').classes('w-[45%] flex flex-col items-end pr-8 md:pr-12'):
            if is_even:
                _timeline_card(year, text)
            else:
                _timeline_ornament(flip=False)

        # ── Cột GIỮA (10%) — nút đỏ ─────────────────────────────────────────
        with ui.element('div').classes('w-[10%] flex justify-center items-center'):
            _timeline_dot()

        # ── Cột PHẢI (45%) ──────────────────────────────────────────────────
        with ui.element('div').classes('w-[45%] flex flex-col items-start pl-8 md:pl-12'):
            if not is_even:
                _timeline_card(year, text)
            else:
                _timeline_ornament(flip=True)


def section_title(title: str, subtitle: str = None):
    with ui.column().classes('items-center text-center gap-2 mb-10 w-full'):
        ui.label(title).classes('font-display text-3xl md:text-4xl font-black text-foreground')
        if subtitle:
            ui.label(subtitle).classes('text-muted-foreground text-base md:text-lg font-light max-w-2xl')
        ui.element('div').classes('h-1 w-16 bg-primary rounded-full mt-2')


def intro_feature_card(icon: str, title: str, desc: str):
    with ui.card().classes(
        'flex flex-col items-center text-center gap-4 p-8 rounded-2xl '
        'border border-border/50 bg-card/60 shadow-sm hover:shadow-md '
        'transition-all duration-300 hover:-translate-y-1'
    ):
        with ui.element('div').classes('h-14 w-14 rounded-full bg-primary/10 flex items-center justify-center'):
            ui.icon(icon, size='28px').classes('text-primary')
        ui.label(title).classes('font-display text-lg font-bold text-foreground')
        ui.label(desc).classes('text-sm text-muted-foreground leading-relaxed font-light')


def unesco_quote(text: str, subtitle: str = None):
    with ui.column().classes('items-center w-full py-2'):
        if subtitle:
            ui.label(subtitle).classes('text-primary font-bold tracking-[0.3em] text-[10px] mb-4 opacity-80')
        with ui.element('blockquote').classes('relative text-2xl font-light italic leading-loose text-muted-foreground px-12 py-4'):
            ui.label('"').classes('absolute top-0 left-0 text-7xl text-primary/10 font-serif leading-none')
            ui.label(text).classes('relative z-10')
            ui.label('"').classes('absolute bottom-0 right-0 text-7xl text-primary/10 font-serif leading-none')
        with ui.row().classes('mt-4 items-center gap-3 opacity-70'):
            ui.element('div').classes('h-px w-10 bg-primary/30')
            ui.label('Nguồn: UNESCO, 2009').classes('text-xs font-semibold tracking-wider text-primary')