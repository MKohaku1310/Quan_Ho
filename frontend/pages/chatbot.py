from nicegui import app, ui
import theme
import components
import asyncio
from api import api_client
from datetime import datetime

@ui.page('/chatbot')
async def chatbot_page():
    # Initialize history in session if not exists
    if 'chat_history' not in app.storage.user:
        app.storage.user['chat_history'] = [
            {'role': 'bot', 'text': 'Chào bạn! Tôi là Trợ lý Quan Họ AI. Tôi có thể giúp gì cho bạn hôm nay?', 'time': datetime.now().strftime('%H:%M')}
        ]

    with theme.frame():
        with ui.element('section').classes('relative h-[calc(100vh-80px)] md:h-[calc(100vh-100px)] py-4 md:py-8 bg-background w-full overflow-hidden'):
            with theme.container().classes('max-w-4xl h-full flex flex-col'):
                
                # Chat Header
                with ui.row().classes('items-center gap-4 mb-4 bg-card p-4 rounded-2xl border border-border shadow-sm shrink-0 mx-2'):
                    ui.image('/static/common/chatbot-avatar.png').classes('w-12 h-12 rounded-full border-2 border-primary/20 bg-muted shadow-sm')
                    with ui.column().classes('gap-0'):
                        ui.label('Trợ lý Quan Họ AI').classes('font-display text-lg font-bold text-primary')
                        with ui.row().classes('items-center gap-1.5'):
                            ui.element('div').classes('w-2 h-2 rounded-full bg-positive animate-pulse')
                            ui.label('Sẵn sàng hỗ trợ').classes('text-[10px] text-muted-foreground uppercase font-bold tracking-wider')

                # Message Area
                @ui.refreshable
                def message_list():
                    with ui.column().classes('w-full gap-4 overflow-y-auto flex-grow p-4 scroll-smooth'):
                        for msg in app.storage.user['chat_history']:
                            sent = msg['role'] == 'user'
                            with ui.row().classes(f'w-full {"justify-end" if sent else "justify-start"}'):
                                with ui.card().classes(f'max-w-[85%] md:max-w-[70%] p-4 rounded-2xl shadow-sm border {"bg-primary text-white border-primary" if sent else "bg-card border-border text-foreground"}'):
                                    ui.label(msg['text']).classes('text-sm leading-relaxed whitespace-pre-line')
                                    ui.label(msg['time']).classes(f'text-[9px] mt-1 opacity-60 {"text-right w-full" if sent else "text-left"}')
                        
                        # Typing Indicator
                        if state.is_typing:
                            with ui.row().classes('w-full justify-start items-center gap-2'):
                                with ui.card().classes('p-3 rounded-2xl bg-card border border-border flex flex-row items-center gap-1'):
                                    ui.element('div').classes('w-1.5 h-1.5 rounded-full bg-primary/40 animate-bounce')
                                    ui.element('div').classes('w-1.5 h-1.5 rounded-full bg-primary/60 animate-bounce [animation-delay:0.2s]')
                                    ui.element('div').classes('w-1.5 h-1.5 rounded-full bg-primary/80 animate-bounce [animation-delay:0.4s]')
                        
                        # Direct call to scroll to bottom after rendering
                        ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)')

                class ChatState:
                    def __init__(self):
                        self.is_typing = False
                
                state = ChatState()
                
                with ui.element('div').classes('flex-grow overflow-hidden relative mb-4'):
                    message_list()

                # Quick Replies
                with ui.row().classes('w-full gap-2 mb-4 px-2 overflow-x-auto no-scrollbar flex-nowrap shrink-0'):
                    quick_options = [
                        ("Giới thiệu Quan họ", "Giới thiệu Quan họ"),
                        ("Sự kiện sắp tới", "Sự kiện sắp tới"),
                        ("Bài hát nổi tiếng", "Bài hát nổi tiếng"),
                        ("49 làng Quan họ", "49 làng Quan họ")
                    ]
                    for label, val in quick_options:
                        ui.button(label, on_click=lambda v=val: handle_send(v)).props('outline rounded-full dense size="sm"').classes('text-[11px] font-bold px-4 shrink-0 border-primary/30 text-primary bg-primary/5 hover:bg-primary/10')

                # Input Section
                with ui.row().classes('w-full bg-card shadow-elevated rounded-2xl p-2 border border-border items-center shrink-0'):
                    msg_input = ui.input(placeholder='Hỏi điều gì đó về Quan họ...').props('rounded borderless').classes('flex-1 px-4 bg-transparent')
                    
                    async def handle_send(text=None):
                        val = text or msg_input.value
                        if not val: return
                        if not text: msg_input.value = ''
                        
                        # Add user message
                        app.storage.user['chat_history'].append({
                            'role': 'user', 'text': val, 'time': datetime.now().strftime('%H:%M')
                        })
                        message_list.refresh()
                        
                        # Show typing
                        state.is_typing = True
                        message_list.refresh()
                        
                        # Get Bot Response
                        response = await api_client.ask_chatbot(val)
                        await asyncio.sleep(1.0) # Artificial delay for better feel
                        
                        # Add bot response
                        app.storage.user['chat_history'].append({
                            'role': 'bot', 'text': response or 'Tôi không thể kết nối hệ thống lúc này. Vui lòng thử lại!', 'time': datetime.now().strftime('%H:%M')
                        })
                        
                        state.is_typing = False
                        message_list.refresh()

                    ui.button(icon='send', on_click=handle_send).props('round unelevated shadow-md').classes('bg-primary text-white')
                    msg_input.on('keydown.enter', lambda: handle_send())

                # Footer hint
                ui.label('Thông tin mang tính chất tham khảo, hãy khám phá thêm tại các chuyên mục chính.').classes('text-[10px] text-muted-foreground w-full text-center mt-3 opacity-60')

