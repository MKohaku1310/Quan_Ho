from nicegui import app, ui
import theme
from datetime import datetime
from translation import t
from api import api_client


def hero_banner():
    # Fixed overflow and height to prevent bleeding into other sections
    with ui.element('section').classes('relative flex min-h-[400px] md:min-h-[500px] lg:min-h-[65vh] items-center overflow-hidden w-full shadow-2xl'):
        ui.image('/static/home/hero-banner.jpg').classes('absolute inset-0 h-full w-full object-cover object-bottom')
        ui.element('div').classes('absolute inset-0 bg-hero-gradient opacity-80 md:opacity-75')
        
        # Floating Lanterns (Studio Flourish)
        for i, pos in enumerate(['left-10 md:left-20 top-32', 'right-10 md:right-32 top-48', 'left-1/4 bottom-32 opacity-30']):
            ui.icon('light', size='2rem').classes(f'absolute {pos} text-gold-light animate-pulse pointer-events-none z-20')
            
        with ui.element('div').classes('relative z-10 container mx-auto px-4 pt-4 pb-24 text-center flex flex-col items-center min-h-[400px] justify-center overflow-visible'):
            # Silk Ribbon (Studio Banner)
            with ui.element('div').classes('mb-6 relative'):
                ui.element('div').classes('absolute inset-0 bg-hero-gradient rotate-[-2deg] transform z-[-1] shadow-lg rounded-sm px-12 py-6 opacity-80')
                ui.label(t('unesco_badge')).classes(
                    'text-sm font-black uppercase tracking-[0.5em] text-white drop-shadow-md'
                ).style('animation: fade-in-up 0.8s ease-out')
            
            with ui.column().classes('gap-2 flex flex-col items-center').style('animation: fade-in-up 1s ease-out 0.2s both'):
                ui.label(t('hero_quan_ho')).classes('font-display text-6xl font-black leading-tight text-white md:text-8xl lg:text-9xl tracking-tighter drop-shadow-2xl')
                ui.label(t('hero_bac_ninh')).classes('font-display text-5xl font-black leading-tight text-gradient-gold md:text-7xl lg:text-8xl tracking-tight')
            
            ui.label(t('hero_desc')).classes('mx-auto mt-10 max-w-3xl text-lg text-white/90 leading-relaxed md:text-2xl font-light italic').style('animation: fade-in-up 1s ease-out 0.4s both')
            
            with ui.row().classes('mt-12 flex flex-wrap justify-center gap-6').style('animation: fade-in-up 1s ease-out 0.6s both'):
                ui.button(t('hero_listen_now'), icon='play_arrow', on_click=lambda: ui.navigate.to('/bai-hat')).props('unelevated rounded-xl size=lg').classes(
                    'bg-accent text-accent-foreground font-black px-12 py-5 shadow-elevated transform transition-all hover:scale-105 tracking-widest'
                )
                ui.button(t('hero_learn_more'), on_click=lambda: ui.navigate.to('/gioi-thieu')).props('outline rounded-xl size=lg').classes(
                    'border-white/40 text-white font-black px-12 py-5 hover:bg-white/10 backdrop-blur-sm tracking-widest'
                )
        
        with ui.element('div').classes('absolute z-10 flex flex-col items-center gap-3 cursor-pointer group opacity-90').style(
            'bottom: 2.5rem; left: 50%; transform: translateX(-50%); animation: bounce 2.4s infinite;'
        ).on('click', lambda: ui.run_javascript(
            'document.getElementById("home-content").scrollIntoView({behavior: "smooth"})'
        )):
            ui.label(t('scroll_down')).classes('text-white text-[11px] font-bold uppercase tracking-[0.2em] group-hover:opacity-100 drop-shadow-lg')
            ui.icon('keyboard_arrow_down', size='36px').classes('text-white group-hover:opacity-100 -mt-2')

            
def hero_stats_section():
    with ui.element('section').classes('bg-card py-20 border-y border-border w-full'):
        with theme.container().classes('grid items-center gap-16 md:grid-cols-2'):
            with ui.column().classes('gap-4'):
                with ui.element('h2').classes('font-display text-3xl font-bold text-foreground md:text-4xl lg:text-5xl'):
                    ui.label(t('stats_resilience_title'))
                    ui.label(t('stats_heritage')).classes('text-primary')
                
                ui.label(t('stats_desc')).classes('leading-relaxed text-muted-foreground text-lg md:text-xl')
                
                with ui.link(target='/gioi-thieu').classes('mt-4 no-underline'):
                    with ui.button(t('explore_now'), icon='arrow_forward').props('unelevated rounded-lg').classes(
                        'bg-primary text-white font-bold px-8 py-3 shadow-md hover:shadow-lg transition-all transform hover:scale-105'
                    ):
                        pass
            
            with ui.element('div').classes('grid grid-cols-2 gap-4'):
                stats = [
                    ('49', t('stats_villages_label'), 'text-primary', 'groups'),
                    ('300+', t('stats_melodies_label'), 'text-accent', 'music_note'),
                    ('2009', t('stats_unesco_label'), 'text-terracotta', 'stars'),
                    ('600+', t('stats_history_label'), 'text-jade', 'history')
                ]
                for val, label, color_class, icon in stats:
                    with ui.element('div').classes('rounded-xl bg-muted/50 p-6 text-center border border-border/50 shadow-sm transition-all hover:shadow-md'):
                        ui.icon(icon, size='32px').classes(f'{color_class} mb-2 opacity-80')
                        ui.label(val).classes(f'font-display text-3xl font-bold {color_class} mb-1')
                        ui.label(label).classes('text-[10px] font-bold text-muted-foreground uppercase tracking-widest')


def chatbot_persona():
    # Khởi tạo history nếu chưa có
    if 'chat_history' not in app.storage.user:
        app.storage.user['chat_history'] = [
            {'role': 'bot', 'text': t('chatbot_greet'), 'time': datetime.now().strftime('%H:%M')}
        ]

    # Suggestions for users
    suggestions = [
        "Quan họ là gì?",
        "Lễ hội sắp tới",
        "49 làng Quan họ",
        "Nghe làn điệu cổ"
    ]

    class ChatState:
        def __init__(self):
            self.is_open = False
            self.is_typing = False
            self.persona = 'liền anh' # Default
    
    state = ChatState()

    def toggle_chat():
        state.is_open = not state.is_open
        chat_container.refresh()
        if state.is_open:
            # Scroll to bottom after opening
            ui.run_javascript('setTimeout(() => { var el = document.getElementById("chat-scroll"); if(el) el.scrollTop = el.scrollHeight; }, 300)')

    async def send_msg(text_val):
        if not text_val: return
        
        # Thêm tin nhắn user
        app.storage.user['chat_history'].append({
            'role': 'user', 'text': text_val, 'time': datetime.now().strftime('%H:%M')
        })
        chat_messages.refresh()
        
        # Hiệu ứng đang gõ
        state.is_typing = True
        chat_messages.refresh()
        ui.run_javascript('var el = document.getElementById("chat-scroll"); if(el) el.scrollTop = el.scrollHeight;')
        
        # Gọi API với history
        history = app.storage.user.get('chat_history', [])
        response_data = await api_client.ask_chatbot(text_val, history=history)
        bot_response = response_data.get('response') if response_data else t('chatbot_busy')
        
        # Thêm tin nhắn bot
        app.storage.user['chat_history'].append({
            'role': 'bot', 'text': bot_response, 'time': datetime.now().strftime('%H:%M')
        })
        state.is_typing = False
        chat_messages.refresh()
        # Cuộn xuống
        ui.run_javascript('setTimeout(() => { var el = document.getElementById("chat-scroll"); if(el) el.scrollTop = el.scrollHeight; }, 100)')

    def clear_chat():
        app.storage.user['chat_history'] = [
            {'role': 'bot', 'text': t('chatbot_greet'), 'time': datetime.now().strftime('%H:%M')}
        ]
        chat_messages.refresh()

    # Container chính của Chatbot
    with ui.element('div').classes('fixed bottom-6 right-6 z-[1000] flex flex-col items-end gap-4 pointer-events-none'):
        
        # Chat Messages Section
        @ui.refreshable
        def chat_messages():
            # Height limited to fit nicely
            with ui.scroll_area().classes('flex-1 p-4 bg-white/20 backdrop-blur-md').props('id=chat-scroll'):
                with ui.column().classes('w-full gap-5'):
                    # Welcome Info
                    with ui.column().classes('items-center w-full mb-4 opacity-40 text-center gap-1'):
                        ui.icon('info', size='14px')
                        ui.label('Trò chuyện cùng Liền Anh & Liền Chị ảo').classes('text-[9px] uppercase font-black tracking-widest')
                        ui.label('Dữ liệu được cập nhật từ Di sản UNESCO').classes('text-[8px]')

                    for msg in app.storage.user['chat_history']:
                        sent = msg['role'] == 'user'
                        with ui.row().classes(f'w-full {"justify-end" if sent else "justify-start"}'):
                            if not sent:
                                ui.avatar('account_circle', color='primary').classes('size-8 shadow-sm mr-2 mt-1')
                            
                            with ui.element('div').classes(f'max-w-[80%] flex flex-col {"items-end" if sent else "items-start"}'):
                                with ui.card().classes(
                                    f'p-4 rounded-2xl shadow-sm border transition-all '
                                    f'{"bg-primary text-white border-primary rounded-tr-none" if sent else "bg-white border-border text-foreground rounded-tl-none"}'
                                ):
                                    if sent:
                                        ui.label(msg['text']).classes('text-sm leading-relaxed')
                                    else:
                                        # Bot response supports Markdown
                                        ui.markdown(msg['text']).classes('text-sm leading-relaxed prose prose-sm prose-p:my-1')
                                
                                ui.label(msg['time']).classes(f'text-[8px] mt-1 opacity-50 px-1 font-black')
                    
                    if state.is_typing:
                        with ui.row().classes('w-full justify-start items-center gap-2'):
                            ui.avatar('account_circle', color='primary').classes('size-6 opacity-50 animate-pulse')
                            with ui.row().classes('gap-1 items-center p-2 bg-white/40 rounded-full'):
                                ui.element('div').classes('w-1.5 h-1.5 bg-primary/40 rounded-full animate-bounce [animation-delay:-0.3s]')
                                ui.element('div').classes('w-1.5 h-1.5 bg-primary/40 rounded-full animate-bounce [animation-delay:-0.15s]')
                                ui.element('div').classes('w-1.5 h-1.5 bg-primary/40 rounded-full animate-bounce')

                    # Quick Suggestions (only if history is short or empty)
                    if len(app.storage.user['chat_history']) <= 2:
                        with ui.row().classes('flex-wrap gap-2 mt-4 justify-start'):
                            for s in suggestions:
                                ui.button(s, on_click=lambda s=s: send_msg(s)).props('outline rounded-full dense size=sm').classes('text-[10px] lowercase px-3 py-1 border-primary/20 text-primary hover:bg-primary/5 transition-colors')

        # Tách container ra để refresh phần ẩn hiện
        @ui.refreshable
        def chat_container():
            # Main Box
            with ui.card().classes(
                'w-[380px] max-w-[90vw] h-[600px] max-h-[80vh] flex flex-col p-0 shadow-elevated border-none overflow-hidden transition-all duration-500 transform origin-bottom-right rounded-[2rem] bg-[#fdfaf5]'
            ).style(
                f'transform: scale({"1" if state.is_open else "0"}); opacity: {"1" if state.is_open else "0"}; pointer-events: {"auto" if state.is_open else "none"}; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);'
            ):
                # Header with Gradient
                with ui.row().classes('w-full p-6 bg-gradient-to-r from-primary to-[#801414] text-white items-center justify-between shrink-0 relative overflow-hidden'):
                    # Background pattern
                    ui.image('/static/common/lotus-pattern.png').classes('absolute -right-4 -top-4 w-24 opacity-10 pointer-events-none rotate-12')
                    
                    with ui.row().classes('items-center gap-4 relative z-10'):
                        with ui.element('div').classes('relative'):
                            ui.image('/static/common/chatbot-avatar.png').classes('w-12 h-12 rounded-2xl border-2 border-white/30 shadow-lg object-cover')
                            ui.element('div').classes('absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 border-2 border-white rounded-full')
                            
                        with ui.column().classes('gap-0'):
                            ui.label(t('chatbot_title')).classes('font-display font-black text-lg leading-tight')
                            ui.label(t('chatbot_online')).classes('text-[10px] opacity-70 uppercase tracking-[0.2em] font-black')
                    
                    with ui.row().classes('items-center gap-1'):
                        ui.button(icon='refresh', on_click=clear_chat).props('flat round color=white size=sm').tooltip('Xóa hội thoại')
                        ui.button(icon='close', on_click=toggle_chat).props('flat round color=white size=sm')

                chat_messages()

                # Footer/Input
                ui.separator().classes('opacity-10')
                with ui.row().classes('w-full p-4 bg-white/80 backdrop-blur-md items-center gap-3 shrink-0'):
                    ti = ui.input(placeholder=t('chatbot_placeholder')).props('rounded outlined borderless bg-muted/20').classes('flex-1 modern-input h-12 px-4')
                    with ti.add_slot('append'):
                         ui.button(icon='send', on_click=lambda: send_msg(ti.value) or setattr(ti, 'value', '')).props('flat round color=primary').classes('mr-1 hover:scale-110 transition-transform')
                    ti.on('keydown.enter', lambda: send_msg(ti.value) or setattr(ti, 'value', ''))

        chat_container()

        # Nút bong bóng (Bubble Button)
        with ui.button(on_click=toggle_chat).props('round unelevated').classes(
            'w-18 h-18 shadow-2xl bg-white border-4 border-primary hover:rotate-6 transition-all duration-500 p-0 overflow-hidden pointer-events-auto relative group'
        ):
            ui.image('/static/common/chatbot-avatar.png').classes('w-full h-full object-cover transition-transform group-hover:scale-110')
            # Pulse Effect
            ui.element('div').classes('absolute inset-0 border-4 border-primary/30 rounded-full animate-ping')
            # Chat Icon Overlay
            with ui.element('div').classes('absolute bottom-0 right-0 bg-primary p-1.5 rounded-tl-xl shadow-lg'):
                ui.icon('chat', size='16px', color='white')


def costume_block(title, desc, image_url, items=None, reverse=False):
    alignment = 'self-start' if not reverse else 'self-end'
    
    with ui.card().classes(
        f'relative w-full max-w-[1000px] {alignment} overflow-visible rounded-[2rem] border border-border/50 '
        f'bg-card/40 shadow-elevated hover:shadow-2xl transition-all duration-500 p-0 group z-10'
    ):
        ui.image('/static/common/lotus-ornament.png').classes(
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
                    ui.label(t('costume_tradition')).classes('text-[10px] font-black tracking-widest')

            with ui.column().classes('md:w-7/12 p-8 md:p-12 justify-center gap-6 z-10'):
                with ui.column().classes('gap-2'):
                    with ui.row().classes('items-center gap-2 mb-2'):
                        ui.element('div').classes('h-px w-6 bg-primary/40')
                        ui.label(t('heritage_kinh_bac')).classes('text-[10px] font-bold tracking-[0.3em] text-primary/70 uppercase')
                    ui.label(title).classes('font-display text-4xl font-black text-foreground leading-tight')
                
                ui.label(desc).classes('text-base text-muted-foreground leading-relaxed font-light')
                
                if items:
                    with ui.column().classes('w-full mt-2'):
                        with ui.row().classes('items-center gap-2 mb-4'):
                            ui.icon('auto_awesome', size='14px').classes('text-primary/60')
                            ui.label(t('artistic_features')).classes('text-[10px] font-bold text-primary/70 uppercase tracking-widest')
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
        ui.image('/static/common/lotus-ornament.png').classes(
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
                    ui.label(t('era_label')).classes('text-[8px] font-black tracking-[0.4em] text-primary/50 uppercase')
                    ui.label(t('era_kinh_bac')).classes('text-[10px] font-bold text-primary/70 tracking-widest')
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
        ui.image('/static/common/lotus-ornament.png').classes(f'h-24 w-24 {rotate}')


def timeline_item(year: str, text: str, index: int = 0, total: int = 4):
    """
    Layout 3 cột: [45% nội dung/trống] [10% nút đỏ] [45% trống/nội dung]
    Chẵn → thẻ bên TRÁI, lẻ → thẻ bên PHẢI.
    Nút đỏ luôn ở giữa, thẳng hàng với thẻ nhờ items-center trên row.
    """
    is_even = index % 2 == 0

    with ui.element('div').classes('relative flex flex-row flex-nowrap items-center w-full my-8'):

        # ── Cột TRÁI (45%) ──────────────────────────────────────────────────
        with ui.element('div').classes('w-[45%] flex flex-col items-end pr-4 md:pr-12'):
            if is_even:
                _timeline_card(year, text)
            else:
                _timeline_ornament(flip=False)

        # ── Cột GIỮA (10%) — nút đỏ ─────────────────────────────────────────
        with ui.element('div').classes('w-[10%] flex justify-center items-center shrink-0'):
            _timeline_dot()

        # ── Cột PHẢI (45%) ──────────────────────────────────────────────────
        with ui.element('div').classes('w-[45%] flex flex-col items-start pl-4 md:pl-12'):
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
            ui.label(t('source_unesco')).classes('text-xs font-semibold tracking-wider text-primary')