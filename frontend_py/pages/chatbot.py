from nicegui import ui
import theme
import components
import asyncio

@ui.page('/chatbot')
def chatbot_page():
    with theme.frame():
        with ui.element('section').classes('relative min-h-[90vh] py-12 bg-background w-full'):
            with theme.container().classes('max-w-4xl'):
                # Header
                with ui.row().classes('items-center gap-4 mb-8 bg-card p-6 rounded-2xl border border-border shadow-sm'):
                    ui.image('/static/chatbot-avatar.png').classes('w-20 h-20 rounded-full border-4 border-white shadow-sm')
                    with ui.column().classes('gap-0'):
                        ui.label('Trợ lý Quan Họ AI').classes('font-display text-2xl font-bold text-primary')
                        ui.label('Tôi có thể giúp bạn tìm hiểu về văn hóa Quan họ Kinh Bắc').classes('text-muted-foreground text-sm')

                # Chat Area
                chat_container = ui.column().classes('w-full gap-4 overflow-y-auto mb-20 p-4 bg-muted/30 rounded-2xl min-h-[400px]')
                
                with chat_container:
                    ui.chat_message('Chào bạn! Tôi là Trợ lý AI của Quan Họ Bắc Ninh. Bạn muốn tìm hiểu về trang phục, làn điệu hay lịch sử Quan họ?', 
                                   name='Bot', stamp='Hôm nay', avatar='/static/chatbot-avatar.png').classes('w-full')

                # Input bar
                with ui.row().classes('fixed bottom-8 left-1/2 -translate-x-1/2 w-full max-w-3xl px-4 z-50'):
                    with ui.row().classes('w-full bg-card shadow-elevated rounded-full p-2 border border-border items-center'):
                        msg_input = ui.input(placeholder='Nhập câu hỏi của bạn...').props('rounded borderless').classes('flex-1 px-6 bg-transparent')
                        
                        async def send_message():
                            text = msg_input.value
                            if not text: return
                            msg_input.value = ''
                            
                            with chat_container:
                                ui.chat_message(text, sent=True, name='Bạn', stamp='Vừa xong').classes('w-full')
                                response = "Xin lỗi, tôi chưa hiểu ý bạn. Bạn có thể hỏi về 'trang phục', 'làng nghề' hoặc 'unesco' được không?"
                                lowered = text.lower()
                                if 'trang phục' in lowered or 'mặc' in lowered:
                                    response = "Trang phục Quan họ rất đặc trưng: Liền chị thường mặc áo mớ ba mớ bảy, nón quai thao, khăn mỏ quạ. Liền anh mặc áo the, khăn xếp, che ô đen."
                                elif 'unesco' in lowered or 'công nhận' in lowered:
                                    response = "Dân ca Quan họ Bắc Ninh đã được UNESCO ghi danh là Di sản văn hóa phi vật thể nhân loại vào ngày 30/09/2009."
                                elif 'chào' in lowered:
                                    response = "Chào bạn! Chúc bạn có một ngày tìm hiểu văn hóa thật thú vị."
                                
                                await asyncio.sleep(0.5)
                                ui.chat_message(response, name='Bot', stamp='Vừa xong', avatar='/static/chatbot-avatar.png').classes('w-full')
                                ui.scroll_to(chat_container)

                        ui.button(icon='send', on_click=send_message).props('round unelevated').classes('bg-primary text-white')
                        msg_input.on('keydown.enter', send_message)
