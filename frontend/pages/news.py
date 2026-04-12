from nicegui import app, ui
import theme
import components
from api import api_client
import asyncio
from datetime import datetime

def _show_registration_dialog(event_id, title, button_ref):
    token = app.storage.user.get('token') or app.storage.user.get('access_token')
    if not token:
        with ui.dialog() as dialog, ui.card().classes('p-8 rounded-2xl shadow-elevated border border-border bg-card max-w-sm w-full'):
            with ui.column().classes('items-center gap-4 text-center w-full'):
                ui.element('div').classes('flex h-16 w-16 items-center justify-center rounded-full bg-primary/10 text-primary mb-2').add(ui.icon('lock_person', size='2rem'))
                ui.label('Yêu cầu đăng nhập').classes('text-2xl font-bold font-display text-foreground')
                ui.label('Vui lòng đăng nhập vào tài khoản của bạn để đăng ký tham gia sự kiện này.').classes('text-muted-foreground text-sm leading-relaxed')
                with ui.row().classes('w-full justify-center gap-3 mt-4 flex-nowrap'):
                    ui.button('Đóng', on_click=dialog.close).props('outline color="grey"').classes('flex-1 rounded-lg')
                    ui.button('Đăng nhập', on_click=lambda: ui.navigate.to('/dang-nhap')).props('color="primary" unelevated').classes('flex-1 rounded-lg font-bold')
        dialog.open()
    else:
        user_name = app.storage.user.get('user_name', '')
        email_val = app.storage.user.get('email', '')

        with ui.dialog() as dialog, ui.card().classes('p-6 sm:p-8 w-[450px] max-w-[95vw] rounded-2xl shadow-elevated border border-border bg-card'):
            with ui.row().classes('items-center gap-3 mb-6 w-full'):
                ui.element('div').classes('flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full bg-primary/10 text-primary').add(ui.icon('how_to_reg', size='1.5rem'))
                with ui.column().classes('gap-0 flex-1 min-w-0'):
                    ui.label('Đăng ký tham gia').classes('text-sm text-muted-foreground font-medium')
                    ui.label(title).classes('text-lg font-bold font-display text-foreground line-clamp-1')
            
            with ui.column().classes('w-full gap-4'):
                name_input = ui.input('Họ và tên *').classes('w-full').props('outlined dense')
                name_input.value = user_name
                
                email_input = ui.input('Email').classes('w-full').props('outlined dense')
                email_input.value = email_val
                
                phone_input = ui.input('Số điện thoại *').classes('w-full').props('outlined dense')
                note_input = ui.textarea('Ghi chú thêm').classes('w-full').props('outlined auto-grow')
                
                status_label = ui.label("").classes("text-negative text-sm font-medium hidden bg-negative/10 px-3 py-2 rounded-lg w-full text-center")
                
                async def submit():
                    if not phone_input.value or not name_input.value:
                        status_label.text = "Vui lòng nhập đầy đủ thông tin bắt buộc (*)"
                        status_label.classes(remove='hidden')
                        return
                    
                    sub_btn.props('loading')
                    data = {
                        "name": name_input.value,
                        "email": email_input.value,
                        "phone": phone_input.value,
                        "note": note_input.value
                    }
                    res = await api_client.register_event(event_id, data)
                    sub_btn.props(remove='loading')
                    
                    if res is not None:
                        dialog.close()
                        ui.notify('Đăng ký sự kiện thành công!', type='positive', position='top', icon='check_circle')
                        button_ref.text = 'Đã đăng ký'
                        button_ref.props('color="grey" disable icon="check_circle"')
                    else:
                        status_label.text = "Đăng ký thất bại. Vui lòng thử lại sau."
                        status_label.classes(remove='hidden')

                with ui.row().classes('w-full justify-end gap-3 mt-2'):
                    ui.button('Hủy', on_click=dialog.close).props('flat color="grey"').classes('px-4 rounded-lg font-medium')
                    sub_btn = ui.button('Xác nhận đăng ký', on_click=submit).props('color="primary" unelevated').classes('px-6 rounded-lg font-bold shadow-sm')
        dialog.open()

@ui.page('/tin-tuc', response_timeout=60.0)
async def news_page():
    with theme.frame():
        components.page_header('Tin tức & Sự kiện', 'Cập nhật dòng chảy văn hóa Quan họ đương đại')

        # Shared state
        class NewsState:
            def __init__(self, news, events):
                self.all_news = news
                self.all_events = events
                self.filtered_news = news
                self.filtered_events = events
                
                self.search_query = ''
                self.month_filter = 'Tất cả'
                self.year_filter = 'Tất cả'
                
                self.news_page = 1
                self.events_page = 1
                self.items_per_page = 6

        # Fetch data
        news_data = await api_client.get_articles(article_type='news')
        event_data = await api_client.get_articles(article_type='event')
        
        # Enhanced Mocks with Rich Content & AI Images
        if not news_data:
            news_data = [
                {
                    'id': 1, 
                    'title': 'Khai mạc triển lãm "Sức sống Quan họ" tại TP. Bắc Ninh', 
                    'description': 'Triển lãm trưng bày hơn 200 hiện vật, hình ảnh quý hiếm về lịch sử hình thành và phát triển của dân ca Quan họ, thu hút hàng nghìn lượt khách tham quan ngay trong ngày đầu khai mạc. Đây là sự kiện quan trọng nhằm tôn vinh các giá trị văn hóa truyền thống của vùng Kinh Bắc.', 
                    'created_at': '2026-04-10', 
                    'category': 'Văn hóa', 
                    'image_url': '/static/village_diem_ancient_gate_1775935115741.png'
                },
                {
                    'id': 2, 
                    'title': 'Nghệ nhân ưu tú truyền dạy kỹ thuật "Vang-Rền-Nền-Nảy" cho thế hệ trẻ', 
                    'description': 'Tại nhà văn hóa làng Diềm, các lớp dạy hát Quan họ miễn phí cho thiếu nhi đang diễn ra sôi nổi. Các nghệ nhân gạo cội không chỉ dạy lời hát mà còn truyền thụ cách lấy hơi, luyến láy và phong thái thanh lịch của người Quan họ.', 
                    'created_at': '2026-04-08', 
                    'category': 'Giáo dục', 
                    'image_url': '/static/quan_ho_teaching_children_1775935150468.png'
                },
                {
                    'id': 3, 
                    'title': 'Bắc Ninh đề xuất mở rộng không gian diễn xướng Quan họ tại cộng đồng', 
                    'description': 'Đề án mới tập trung vào việc khôi phục các canh hát cửa đình, hát dưới thuyền tại các làng Quan họ gốc, giúp di sản gắn bó mật thiết hơn với đời sống thường nhật của người dân.', 
                    'created_at': '2026-04-05', 
                    'category': 'Chính sách', 
                    'image_url': 'https://images.unsplash.com/photo-1599908608021-b5d929aa054e'
                }
            ]
        if not event_data:
            event_data = [
                {
                    'id': 101, 
                    'title': 'Đêm Quan họ trên Thuyền Rồng - Hẹn hò tháng Giêng', 
                    'description': 'Canh hát đặc biệt diễn ra dưới ánh trăng tại hồ Nguyên Phi Ỷ Lan, tái hiện không gian giao duyên xưa với sự góp mặt của 50 cặp liền anh, liền chị. Du khách sẽ được thưởng thức những làn điệu mượt mà trong không gian thơ mộng nhất.', 
                    'start_date': '2026-05-15', 
                    'location': 'Hồ Nguyên Phi Ỷ Lan, TP. Bắc Ninh', 
                    'available_slots': 150, 
                    'image_url': '/static/quan_ho_festival_boat_1775935130553.png'
                },
                {
                    'id': 102, 
                    'title': 'Giao lưu "Câu hát trao duyên" - Tiên Du 2026', 
                    'description': 'Chương trình giao lưu văn hóa giữa các CLB Quan họ tiêu biểu trên toàn tỉnh. Đây là cơ hội để các liền anh, liền chị chia sẻ kinh nghiệm và trình diễn những bài Quan họ cổ ít người biết đến.', 
                    'start_date': '2026-06-20', 
                    'location': 'Trung tâm Văn hóa Huyện Tiên Du', 
                    'available_slots': 300, 
                    'image_url': 'https://images.unsplash.com/photo-1526462981764-f6cf0f4ea260'
                }
            ]

        state = NewsState(news_data, event_data)

        def apply_filters():
            q = state.search_query.lower()
            m = state.month_filter
            y = state.year_filter
            
            def match(item, date_key):
                date_val = item.get(date_key, '')
                if not date_val: return False
                try:
                    dt = datetime.fromisoformat(date_val.replace('Z', '+00:00'))
                    match_m = (m == 'Tất cả' or dt.month == int(m))
                    match_y = (y == 'Tất cả' or dt.year == int(y))
                    return match_m and match_y
                except: return True # Fallback for malformed
            
            state.filtered_news = [n for n in state.all_news if (q in n.get('title','').lower() or q in n.get('description','').lower()) and match(n, 'created_at')]
            state.filtered_events = [e for e in state.all_events if (q in e.get('title','').lower() or q in e.get('description','').lower()) and match(e, 'start_date')]
            
            state.news_page = 1
            state.events_page = 1
            content_area.refresh()

        @ui.refreshable
        def content_area():
            with ui.tabs().classes('w-full border-b border-border bg-card/30 rounded-t-2xl shadow-sm') as tabs:
                news_tab = ui.tab('Tin tức', icon='article').classes('font-bold px-4 sm:px-8 py-4')
                event_tab = ui.tab('Sự kiện', icon='event').classes('font-bold px-4 sm:px-8 py-4')

            with ui.tab_panels(tabs, value=news_tab).classes('w-full bg-transparent p-0 mt-8'):
                with ui.tab_panel(news_tab).classes('p-0 w-full'):
                    # News Grid
                    start = (state.news_page - 1) * state.items_per_page
                    end = start + state.items_per_page
                    page_items = state.filtered_news[start:end]
                    
                    if not page_items:
                        components.empty_state('Không tìm thấy tin tức nào.')
                    else:
                        with ui.row().classes('grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8 w-full px-2'):
                            for item in page_items:
                                components.news_grid_card(item)
                        
                        # Pagination UI
                        total_pages = (len(state.filtered_news) + state.items_per_page - 1) // state.items_per_page
                        if total_pages > 1:
                            with ui.row().classes('w-full justify-center mt-12 gap-2'):
                                ui.button(icon='chevron_left', on_click=lambda: (setattr(state, 'news_page', max(1, state.news_page-1)), content_area.refresh())).props('flat round').classes('text-primary')
                                for p in range(1, total_pages + 1):
                                    ui.button(str(p), on_click=lambda p=p: (setattr(state, 'news_page', p), content_area.refresh())).props(f'flat round {"color=primary shadow-md bg-primary/10" if p == state.news_page else "color=grey"}').classes('font-bold')
                                ui.button(icon='chevron_right', on_click=lambda: (setattr(state, 'news_page', min(total_pages, state.news_page+1)), content_area.refresh())).props('flat round').classes('text-primary')

                with ui.tab_panel(event_tab).classes('p-0 w-full'):
                    # Events Grid
                    start = (state.events_page - 1) * state.items_per_page
                    end = start + state.items_per_page
                    page_items = state.filtered_events[start:end]
                    
                    if not page_items:
                        components.empty_state('Không tìm thấy sự kiện nào.')
                    else:
                        with ui.row().classes('grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8 w-full px-2'):
                            for item in page_items:
                                components.event_grid_card(item, on_register=_show_registration_dialog)
                        
                        total_pages = (len(state.filtered_events) + state.items_per_page - 1) // state.items_per_page
                        if total_pages > 1:
                            with ui.row().classes('w-full justify-center mt-12 gap-2'):
                                ui.button(icon='chevron_left', on_click=lambda: (setattr(state, 'events_page', max(1, state.events_page-1)), content_area.refresh())).props('flat round').classes('text-primary')
                                for p in range(1, total_pages + 1):
                                    ui.button(str(p), on_click=lambda p=p: (setattr(state, 'events_page', p), content_area.refresh())).props(f'flat round {"color=primary shadow-md bg-primary/10" if p == state.events_page else "color=grey"}').classes('font-bold')
                                ui.button(icon='chevron_right', on_click=lambda: (setattr(state, 'events_page', min(total_pages, state.events_page+1)), content_area.refresh())).props('flat round').classes('text-primary')

        # Main Layout
        with ui.element('section').classes('py-12 md:py-16 bg-background min-h-screen'):
            with theme.container():
                # Filter Bar: Responsive Row/Col
                with ui.element('div').classes('w-full mb-10 gap-4 bg-card/30 p-4 sm:p-6 rounded-2xl border border-border items-center flex flex-col sm:flex-row'):
                    search = ui.input(placeholder='Tìm kiếm bài viết, sự kiện...').classes('flex-1 w-full bg-background rounded-lg').props('outlined dense clearable icon="search"')
                    search.on('update:model-value', lambda e: (setattr(state, 'search_query', e or ''), apply_filters()))
                    
                    with ui.element('div').classes('w-full sm:w-auto flex gap-3'):
                        months = ['Tất cả'] + [str(i) for i in range(1, 13)]
                        month_sel = ui.select(months, value='Tất cả', label='Tháng').classes('flex-1 sm:w-28 bg-background').props('outlined dense')
                        month_sel.on('update:model-value', lambda e: (setattr(state, 'month_filter', e), apply_filters()))
                        
                        years = ['Tất cả', '2024', '2025', '2026']
                        year_sel = ui.select(years, value='Tất cả', label='Năm').classes('flex-1 sm:w-28 bg-background').props('outlined dense')
                        year_sel.on('update:model-value', lambda e: (setattr(state, 'year_filter', e), apply_filters()))

                content_area()

@ui.page('/tin-tuc/{id}')
async def news_detail_page(id: int):
    with theme.frame():
        news_data = await api_client.get_article(id)
        # Mock fallback
        if not news_data:
            news_data = {'id': id, 'title': f'Chi tiết bản tin số {id}', 'content': 'Nội dung đầy đủ của bản tin về văn hóa Quan họ Bắc Ninh sẽ được hiển thị tại đây. Đây là bài viết chuyên sâu về các hoạt động bảo tồn dân ca Quan họ, trình bày về lịch sử, nghệ thuật và những nỗ lực gìn giữ di sản văn hóa phi vật thể của nhân loại.\n\nQuan họ Bắc Ninh không chỉ là những câu hát mượt mà, đằm thắm mà còn là nếp sống, là văn hóa ứng xử "kính trên nhường dưới", trọng nghĩa trọng tình của người dân vùng Kinh Bắc.', 'created_at': '2026-04-11', 'category': 'Văn hóa', 'image_url': 'https://picsum.photos/id/45/1200/600'}
            
        with ui.element('section').classes('w-full bg-background pb-20'):
            # Hero Image Header
            with ui.element('div').classes('relative h-[400px] md:h-[500px] w-full mb-12'):
                ui.image(news_data.get('image_url')).classes('w-full h-full object-cover')
                with ui.element('div').classes('absolute inset-0 bg-gradient-to-t from-background to-transparent'):
                    with theme.container().classes('h-full flex flex-col justify-end pb-12'):
                        ui.label(news_data.get('category', 'Tin tức')).classes('bg-primary text-white text-xs font-bold px-3 py-1 rounded-full w-fit mb-4 uppercase tracking-widest')
                        ui.label(news_data.get('title')).classes('font-display text-4xl md:text-5xl font-bold text-foreground mb-4 drop-shadow-sm')
                        with ui.row().classes('items-center gap-4 text-muted-foreground'):
                            with ui.row().classes('items-center gap-1'):
                                ui.icon('schedule', size='18px')
                                ui.label(news_data.get('created_at', '')[:10])
                            ui.label('|')
                            ui.label('Tác giả: Ban Biên Tập')

            with theme.container().classes('grid grid-cols-1 lg:grid-cols-3 gap-12'):
                # Main Content
                with ui.column().classes('lg:col-span-2 gap-8'):
                    ui.label(news_data.get('content', '')).classes('text-lg leading-relaxed text-foreground/90 whitespace-pre-line text-justify')
                    
                    # Share buttons
                    with ui.row().classes('w-full items-center gap-4 py-8 border-y border-border mt-12'):
                        ui.label('Chia sẻ bài viết:').classes('font-bold text-sm uppercase text-muted-foreground')
                        ui.button(icon='facebook').props('flat round color="primary"')
                        ui.button(icon='share').props('flat round color="primary"')

                # Sidebar
                with ui.column().classes('gap-8'):
                    ui.label('Tin liên quan').classes('text-2xl font-bold font-display border-l-4 border-primary pl-4 mb-2')
                    for i in range(1, 4):
                        with ui.row().classes('gap-4 group cursor-pointer pb-6 border-b border-border/50').on('click', lambda i=i: ui.navigate.to(f'/tin-tuc/{i}')):
                            ui.image(f'https://picsum.photos/id/{i+5}/200/200').classes('w-20 h-20 rounded-xl object-cover shrink-0')
                            with ui.column().classes('gap-1'):
                                ui.label(f'Bài viết liên quan số {i} về di sản Quan họ').classes('text-sm font-bold line-clamp-2 group-hover:text-primary transition-colors')
                                ui.label('2026-04-10').classes('text-[10px] text-muted-foreground')

@ui.page('/su-kien/{id}')
async def event_detail_page(id: int):
    # This can reuse components or have its own detail layout
    await news_detail_page(id) # Simple reuse for now
