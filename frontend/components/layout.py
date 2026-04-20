from nicegui import app, ui
import theme
from datetime import datetime
from translation import t
from api import api_client

def hero_banner():
    # Banner chinh cua trang chu - Refined to better match Image 1
    with ui.element('section').classes('relative flex min-h-[600px] lg:min-h-[85vh] items-center overflow-hidden w-full shadow-2xl'):
        # Dual-layer background to show ENTIRE content of square images on wide screens
        # Layer 1: Blurred fill to handle aspect ratio mismatch
        ui.image('/static/home/hero-banner.jpg').classes('absolute inset-0 h-full w-full').style('object-fit: cover; filter: blur(30px); opacity: 0.3;')
        
        # Layer 2: Actual image with 'contain' to ensure 100% visibility without cropping
        ui.image('/static/home/hero-banner.jpg').classes('absolute inset-0 h-full w-full').style('object-fit: contain; object-position: center;')
        
        # Premium Heritage Overlay (Warm Ink/Charcoal tone)
        ui.element('div').classes('absolute inset-0 bg-[#0c0502]/65 z-0') 
        ui.element('div').classes('absolute inset-0 bg-gradient-to-t from-[#1a0c05] via-transparent to-black/40 z-0')
        
        with ui.element('div').classes('relative z-20 w-full px-4 text-center flex flex-col items-center justify-center py-20 min-h-screen'):
            # UNESCO Label - Elegant and spaced
            ui.label(t('unesco_badge')).classes(
                'text-[10px] md:text-xs font-bold uppercase tracking-[0.5em] text-white/70 mb-10'
            ).style('animation: fade-in-up 0.8s ease-out')
            
            # Main Title - Playfair Display with better scaling
            with ui.column().classes('gap-0 flex flex-col items-center mb-6').style('animation: fade-in-up 1s ease-out 0.2s both'):
                ui.label(t('hero_quan_ho')).classes('font-display text-6xl md:text-8xl lg:text-9xl font-black leading-tight text-white drop-shadow-2xl')
                ui.label(t('hero_bac_ninh')).classes('font-display text-5xl md:text-7xl lg:text-8xl font-black leading-[0.9] text-[#d68e33] tracking-tight')
            
            # Description - More compact and readable
            ui.label(t('hero_desc')).classes(
                'mx-auto mt-6 max-w-2xl text-sm md:text-lg text-white/90 leading-relaxed font-light italic text-center'
            ).style('animation: fade-in-up 1s ease-out 0.4s both')
            
            # Action Buttons - Warm gold and outline
            # Hero Buttons
            with ui.row().classes('mt-12 flex flex-wrap justify-center items-center gap-6 w-full').style('animation: fade-in-up 1s ease-out 0.6s both'):
                ui.button(t('hero_listen_now'), on_click=lambda: ui.navigate.to('/bai-hat')).props('unelevated rounded-sm').classes(
                    'bg-primary text-white font-bold h-14 text-sm hover:bg-primary/90 transition-all transform hover:scale-105 shadow-xl uppercase tracking-widest flex items-center justify-center min-w-[200px]'
                )
                ui.button(t('hero_learn_more'), on_click=lambda: ui.navigate.to('/gioi-thieu')).props('outline rounded-sm').classes(
                    'border-2 border-white/60 text-white font-bold h-14 text-sm hover:bg-white/10 backdrop-blur-sm transition-all transform hover:scale-105 uppercase tracking-widest flex items-center justify-center min-w-[200px]'
                )
        
        # Scroll Down Indicator - Refined positioning to prevent misalignment
        with ui.element('div').classes('absolute z-20 cursor-pointer group').style(
            'bottom: 1.5rem; left: 50%; transform: translateX(-50%);'
        ).on('click', lambda: ui.run_javascript(
            'document.getElementById("home-content").scrollIntoView({behavior: "smooth"})'
        )):
            with ui.element('div').classes('flex flex-col items-center gap-2').style('animation: bounce 3s infinite;'):
                ui.label(t('scroll_down')).classes(
                    'text-white/60 text-[9px] font-bold uppercase tracking-[0.2em] text-center -mr-[0.2em]'
                )
                ui.icon('keyboard_arrow_down', size='28px').classes('text-white/60 -mt-1')

            
def hero_stats_section():
    # Phan thong ke so lieu
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
    # Khoi tao lich su chat va trang thai neu chua co
    if 'chat_history' not in app.storage.user:
        app.storage.user['chat_history'] = [
            {'role': 'bot', 'text': t('chatbot_greet'), 'time': datetime.now().strftime('%H:%M')}
        ]
    if 'chat_open' not in app.storage.user:
        app.storage.user['chat_open'] = False
    if 'chat_is_typing' not in app.storage.user:
        app.storage.user['chat_is_typing'] = False
    if 'chat_input' not in app.storage.user:
        app.storage.user['chat_input'] = ''

    # Goi y cau hoi
    suggestions = [
        "Quan họ là gì?",
        "Lễ hội sắp tới",
        "49 làng Quan họ",
        "Nghe làn điệu cổ"
    ]

    def toggle_chat():
        app.storage.user['chat_open'] = not app.storage.user['chat_open']
        chat_container.refresh()
        if app.storage.user['chat_open']:
            ui.timer(0.3, lambda: chat_scroll.scroll_to(percent=1.0), once=True)

    async def send_msg(text_val):
        if not text_val or not text_val.strip(): return
        
        # Clear input immediately for UX
        input_text = text_val.strip()
        app.storage.user['chat_input'] = ''
        
        # Luu tin nhan nguoi dung
        app.storage.user['chat_history'].append({
            'role': 'user', 'text': input_text, 'time': datetime.now().strftime('%H:%M')
        })
        app.storage.user['chat_is_typing'] = True
        
        chat_messages.refresh()
        chat_container.refresh()
        
        ui.timer(0.1, lambda: chat_scroll.scroll_to(percent=1.0), once=True)
        
        # Goi API chatbot
        try:
            history = app.storage.user.get('chat_history', [])
            bot_response = await api_client.ask_chatbot(input_text, history=history)
            
            # Neu bot khong tra loi hoac tra loi qua ngan/rong
            if not bot_response or len(bot_response.strip()) < 2:
                lang = app.storage.user.get('language', 'vi')
                if any(greet in input_text.lower() for greet in ['halo', 'chào', 'hi']):
                    if lang == 'vi':
                        bot_response = "Dạ, em Liền chị xin chào Quý khách ạ! Chúc Quý khách một ngày mới thật nhiều niềm vui và luôn yêu mến những làn điệu Quan họ quê em."
                    else:
                        bot_response = "Greetings! I am Lien Chi, your cultural guide. I wish you a wonderful day exploring the beautiful Quan ho folk songs of our homeland."
                else:
                    bot_response = t('chatbot_busy')
        except Exception as e:
            print(f"Chatbot API Error: {e}")
            bot_response = t('chatbot_error')
        
        # Luu tin nhan bot
        app.storage.user['chat_history'].append({
            'role': 'bot', 'text': bot_response, 'time': datetime.now().strftime('%H:%M')
        })
        app.storage.user['chat_is_typing'] = False
        chat_messages.refresh()
        chat_container.refresh()
        ui.timer(0.2, lambda: chat_scroll.scroll_to(percent=1.0), once=True)

    def clear_chat():
        app.storage.user['chat_history'] = [
            {'role': 'bot', 'text': t('chatbot_greet'), 'time': datetime.now().strftime('%H:%M')}
        ]
        app.storage.user['chat_is_typing'] = False
        chat_messages.refresh()

    # Giao dien Chatbot
    with ui.element('div').classes('fixed bottom-6 right-6 z-[1000] flex flex-col items-end gap-4 pointer-events-none'):
        
        @ui.refreshable
        def chat_messages():
            global chat_scroll
            with ui.scroll_area().classes('flex-1 p-6 bg-white/10 backdrop-blur-sm') as chat_scroll:
                with ui.column().classes('w-full gap-6'):
                    # Guide Text
                    with ui.column().classes('items-center w-full mb-6 opacity-30 text-center gap-1'):
                        ui.icon('auto_awesome', size='20px', color='primary')
                        ui.label('Di sản văn hóa Quan họ Bắc Ninh').classes('text-[10px] uppercase font-black tracking-[0.3em]')
                        ui.label('Virtual Assistant • UNESCO Heritage Guide').classes('text-[8px] font-bold')

                    for msg in app.storage.user['chat_history']:
                        sent = msg['role'] == 'user'
                        with ui.row().classes(f'w-full {"justify-end" if sent else "justify-start"} items-start gap-3'):
                            if not sent:
                                with ui.element('div').classes('shrink-0 mt-1'):
                                    ui.image('/static/common/chatbot-avatar.png').classes('w-10 h-10 rounded-2xl shadow-lg border-2 border-white object-cover')
                            
                            with ui.element('div').classes(f'max-w-[75%] flex flex-col {"items-end" if sent else "items-start"}'):
                                # Bubble
                                with ui.card().classes(
                                    f'p-4 rounded-[1.5rem] shadow-sm border-none transition-all '
                                    f'{"bg-[#8b0000] text-white rounded-tr-none" if sent else "bg-white/90 text-[#2c1810] rounded-tl-none"}'
                                ).style('box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1);'):
                                    if sent:
                                        ui.label(msg['text']).classes('text-sm leading-relaxed font-semibold')
                                    else:
                                        ui.markdown(msg['text']).classes('text-sm leading-relaxed prose prose-sm prose-p:my-1 prose-headings:text-primary prose-headings:font-black')
                                
                                # Timestamp
                                ui.label(msg['time']).classes(f'text-[9px] mt-1.5 opacity-40 px-1 font-bold tracking-widest')
                            
                            if sent:
                                with ui.element('div').classes('shrink-0 mt-1'):
                                    ui.avatar('person', color='primary').classes('size-10 shadow-lg border-2 border-white text-white')
                    
                    if app.storage.user.get('chat_is_typing'):
                        with ui.row().classes('w-full justify-start items-center gap-4'):
                            ui.image('/static/common/chatbot-avatar.png').classes('w-10 h-10 rounded-2xl shadow-lg opacity-40 animate-pulse object-cover')
                            with ui.row().classes('gap-1.5 items-center p-3 bg-white/60 rounded-full shadow-inner'):
                                ui.element('div').classes('w-2 h-2 bg-primary/30 rounded-full animate-bounce [animation-delay:-0.3s]')
                                ui.element('div').classes('w-2 h-2 bg-primary/30 rounded-full animate-bounce [animation-delay:-0.15s]')
                                ui.element('div').classes('w-2 h-2 bg-primary/30 rounded-full animate-bounce')

                    if len(app.storage.user['chat_history']) <= 2:
                        with ui.row().classes('flex-wrap gap-2.5 mt-6 justify-center'):
                            for s in suggestions:
                                with ui.button(on_click=lambda s=s: send_msg(s)).props('unelevated rounded-full size=sm').classes('bg-white/80 text-primary border border-primary/10 hover:bg-primary hover:text-white transition-all transform hover:scale-105 shadow-sm px-4'):
                                    ui.label(s).classes('text-[11px] font-bold lowercase')

        @ui.refreshable
        def chat_container():
            with ui.card().classes(
                'w-[400px] max-w-[95vw] h-[580px] max-h-[80vh] flex flex-col p-0 shadow-2xl border-none overflow-hidden transition-all duration-700 transform origin-bottom-right rounded-[2.5rem] bg-[#fdfaf5]'
            ).style(
                f'transform: scale({"1" if app.storage.user.get("chat_open") else "0"}); opacity: {"1" if app.storage.user.get("chat_open") else "0"}; pointer-events: {"auto" if app.storage.user.get("chat_open") else "none"};'
                f'background-color: #fdfaf5; background-image: radial-gradient(#d4af37 0.5px, transparent 0.5px); background-size: 20px 20px; background-attachment: fixed; opacity: 1;'
            ):
                # Header
                with ui.element('div').classes('w-full p-6 bg-gradient-to-br from-[#8b0000] to-[#5a0000] text-white shrink-0 relative overflow-hidden'):
                    ui.image('/static/common/lotus-pattern.png').classes('absolute -right-6 -top-6 w-32 opacity-15 pointer-events-none rotate-12')
                    
                    # Action Buttons (Absolute Top Right)
                    with ui.row().classes('absolute top-4 right-4 items-center gap-1 z-20'):
                        ui.button(icon='refresh', on_click=clear_chat).props('flat round color=white size=sm').classes('hover:bg-white/10 opacity-60 hover:opacity-100 transition-opacity').tooltip('Xóa hội thoại')
                        ui.button(icon='close', on_click=toggle_chat).props('flat round color=white size=sm').classes('hover:bg-white/10 opacity-60 hover:opacity-100 transition-opacity')

                    # Branding (Left)
                    with ui.row().classes('items-center gap-4 relative z-10 pr-16'):
                        with ui.element('div').classes('relative group'):
                            ui.image('/static/common/chatbot-avatar.png').classes('w-12 h-12 rounded-2xl border-2 border-white/40 shadow-xl object-cover transition-transform group-hover:scale-105')
                            ui.element('div').classes('absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 border-[3px] border-white rounded-full animate-pulse')
                            
                        with ui.column().classes('gap-0'):
                            ui.label(t('chatbot_title')).classes('font-display font-black text-lg leading-tight tracking-tight')
                            with ui.row().classes('items-center gap-1.5 opacity-80'):
                                ui.element('div').classes('w-1.5 h-1.5 bg-green-400 rounded-full')
                                ui.label(t('chatbot_online')).classes('text-[8px] uppercase font-black tracking-[0.2em]')

                chat_messages()

                # Input Area
                ui.separator().classes('opacity-5')
                with ui.row().classes('w-full p-6 bg-white/95 backdrop-blur-xl items-center gap-4 shrink-0 border-t border-primary/10 shadow-[0_-8px_30px_rgba(0,0,0,0.04)]'):
                    ti = ui.input(placeholder=t('chatbot_placeholder')).props('rounded border-none borderless').classes('flex-1 h-12 bg-[#f5f5f0] px-6 rounded-2xl transition-all focus:ring-2 focus:ring-primary/20 text-sm font-medium border-none shadow-inner flex items-center').bind_value(app.storage.user, 'chat_input')
                    with ti.add_slot('append'):
                         ui.button(icon='send', on_click=lambda: send_msg(ti.value)).props('unelevated round color=primary size=lg').classes('hover:scale-110 active:scale-90 transition-all shadow-xl -mr-2')
                    ti.on('keydown.enter', lambda: send_msg(ti.value))

        chat_container()

        # Nut mo chat
        with ui.button(on_click=toggle_chat).props('round unelevated').classes(
            'w-20 h-20 shadow-2xl bg-white border-4 border-primary hover:rotate-3 transition-all duration-500 p-0 overflow-hidden pointer-events-auto relative group scale-100 hover:scale-105'
        ):
            ui.image('/static/common/chatbot-avatar.png').classes('w-full h-full object-cover transition-transform group-hover:scale-110')
            # Hieu ung song am
            ui.element('div').classes('absolute inset-0 border-4 border-primary/40 rounded-full animate-ping opacity-30')
            # Badge chat
            with ui.element('div').classes('absolute bottom-0 right-0 bg-[#8b0000] p-2 rounded-tl-2xl shadow-lg border-l-2 border-t-2 border-white/20'):
                ui.icon('chat', size='24px', color='white').classes('animate-bounce [animation-iteration-count:3]')


def costume_block(title, desc, image_url, items=None, reverse=False):
    # Khoi gioi thieu trang phuc
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


def _timeline_card(year: str, text: str):
    # The hien thi moc thoi gian
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
    # Nut tron tren timeline
    with ui.element('div').classes(
        'relative h-12 w-12 flex-shrink-0 flex items-center justify-center '
        'bg-primary border-2 border-[#d4af37]/60 shadow-elevated '
        'transition-all duration-300 hover:scale-125 cursor-pointer z-30 rotate-3'
    ):
        ui.element('div').classes('absolute inset-1.5 border border-white/20')
        ui.icon('adjust', size='24px').classes('text-white/40')
        ui.element('div').classes('absolute -inset-4 border border-primary/5 rounded-full animate-ping opacity-20')


def _timeline_ornament(flip: bool = False):
    # Trang tri hoa sen
    rotate = '-rotate-12' if not flip else 'rotate-45'
    padding = 'pr-10' if not flip else 'pl-10'
    with ui.element('div').classes(
        f'opacity-[0.07] grayscale hover:grayscale-0 hover:opacity-100 '
        f'transition-all duration-1000 transform hover:scale-125 {padding}'
    ):
        ui.image('/static/common/lotus-ornament.png').classes(f'h-24 w-24 {rotate}')


def timeline_item(year: str, text: str, index: int = 0, total: int = 4):
    # Cac thanh phan timeline
    is_even = index % 2 == 0

    with ui.element('div').classes('relative flex flex-row flex-nowrap items-center w-full my-8'):
        with ui.element('div').classes('w-[45%] flex flex-col items-end pr-4 md:pr-12'):
            if is_even:
                _timeline_card(year, text)
            else:
                _timeline_ornament(flip=False)

        with ui.element('div').classes('w-[10%] flex justify-center items-center shrink-0'):
            _timeline_dot()

        with ui.element('div').classes('w-[45%] flex flex-col items-start pl-4 md:pl-12'):
            if not is_even:
                _timeline_card(year, text)
            else:
                _timeline_ornament(flip=True)


def section_title(title: str, subtitle: str = None):
    # Tieu de cua cac phan
    with ui.column().classes('items-center text-center gap-2 mb-10 w-full'):
        ui.label(title).classes('font-display text-3xl md:text-4xl font-black text-foreground')
        if subtitle:
            ui.label(subtitle).classes('text-muted-foreground text-base md:text-lg font-light max-w-2xl')
        ui.element('div').classes('h-1 w-16 bg-primary rounded-full mt-2')


def intro_feature_card(icon: str, title: str, desc: str):
    # The tinh nang gioi thieu
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
    # Trich dan UNESCO
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