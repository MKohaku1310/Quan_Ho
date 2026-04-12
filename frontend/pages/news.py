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
                with ui.element('div').classes('flex h-16 w-16 items-center justify-center rounded-full bg-primary/10 text-primary mb-2'):
                    ui.icon('lock_person', size='2rem')
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
                with ui.element('div').classes('flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full bg-primary/10 text-primary'):
                    ui.icon('how_to_reg', size='1.5rem')
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
                self.items_per_page = 8

        # Fetch data
        news_data = await api_client.get_articles(article_type='news')
        event_data = await api_client.get_articles(article_type='event')

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
                        with ui.row().classes('grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 w-full'):
                            for item in page_items:
                                components.news_grid_card(item)
                        
                        # Pagination UI
                        total_pages = (len(state.filtered_news) + state.items_per_page - 1) // state.items_per_page
                        if total_pages > 1:
                            with ui.row().classes('w-full justify-center mt-12 gap-2'):
                                ui.button(icon='chevron_left', on_click=lambda: (setattr(state, 'news_page', max(1, state.news_page-1)), content_area.refresh())).props('flat round dense').classes('text-primary')
                                for p in range(1, total_pages + 1):
                                    ui.button(str(p), on_click=lambda p=p: (setattr(state, 'news_page', p), content_area.refresh())).props(f'flat round dense {"color=primary shadow-md bg-primary/10" if p == state.news_page else "color=grey"}').classes('font-bold text-sm')
                                ui.button(icon='chevron_right', on_click=lambda: (setattr(state, 'news_page', min(total_pages, state.news_page+1)), content_area.refresh())).props('flat round dense').classes('text-primary')

                with ui.tab_panel(event_tab).classes('p-0 w-full'):
                    # Events Grid
                    start = (state.events_page - 1) * state.items_per_page
                    end = start + state.items_per_page
                    page_items = state.filtered_events[start:end]
                    
                    if not page_items:
                        components.empty_state('Không tìm thấy sự kiện nào.')
                    else:
                        with ui.row().classes('grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 w-full'):
                            for item in page_items:
                                components.event_grid_card(item, on_register=_show_registration_dialog)
                        
                        total_pages = (len(state.filtered_events) + state.items_per_page - 1) // state.items_per_page
                        if total_pages > 1:
                            with ui.row().classes('w-full justify-center mt-12 gap-2'):
                                ui.button(icon='chevron_left', on_click=lambda: (setattr(state, 'events_page', max(1, state.events_page-1)), content_area.refresh())).props('flat round dense').classes('text-primary')
                                for p in range(1, total_pages + 1):
                                    ui.button(str(p), on_click=lambda p=p: (setattr(state, 'events_page', p), content_area.refresh())).props(f'flat round dense {"color=primary shadow-md bg-primary/10" if p == state.events_page else "color=grey"}').classes('font-bold text-sm')
                                ui.button(icon='chevron_right', on_click=lambda: (setattr(state, 'events_page', min(total_pages, state.events_page+1)), content_area.refresh())).props('flat round dense').classes('text-primary')

        with ui.element('section').classes('pt-6 pb-16 bg-background min-h-screen'):
            with theme.container():
                # Modern Filter Bar (Single Row)
                with ui.element('div').classes('modern-search-card mb-6 w-full p-2 sm:p-3 rounded-xl flex items-center gap-2 sm:gap-4'):
                    search = ui.input(placeholder='Tìm kiếm bài viết, sự kiện...').classes('modern-input flex-1 bg-background rounded-lg').props('outlined dense clearable debounce=500 icon=search')
                    search.on('update:model-value', lambda e: (setattr(state, 'search_query', e or ''), apply_filters()))
                    
                    months = ['Tất cả'] + [str(i) for i in range(1, 13)]
                    month_sel = ui.select(months, value='Tất cả').classes('modern-select w-20 sm:w-28 bg-background').props('outlined dense rounded-lg options-dense prefix="Tháng:"')
                    month_sel.on('update:model-value', lambda e: (setattr(state, 'month_filter', e or 'Tất cả'), apply_filters()))
                    
                    years = ['Tất cả', '2024', '2025', '2026']
                    year_sel = ui.select(years, value='Tất cả').classes('modern-select w-20 sm:w-28 bg-background').props('outlined dense rounded-lg options-dense prefix="Năm:"')
                    year_sel.on('update:model-value', lambda e: (setattr(state, 'year_filter', e or 'Tất cả'), apply_filters()))
                    
                    if app.storage.user.get('role') == 'admin':
                        ui.button(icon='add_circle', on_click=lambda: ui.navigate.to('/admin/edit/news/0')).props('unelevated round size=md').classes('bg-primary text-white shadow-md hover:scale-110 transition-transform shrink-0')

                content_area()

@ui.page('/tin-tuc/{id}')
async def article_detail_page(id: int):
    with theme.frame():
        news_data = await api_client.get_article(id)
        if not news_data:
            components.empty_state('Không tìm thấy bài viết này.')
            return
            
        _render_detail_view(news_data, is_event=False)

@ui.page('/su-kien/{id}')
async def event_detail_page(id: int):
    with theme.frame():
        event_data = await api_client.get_event(id)
        if not event_data:
            components.empty_state('Không tìm thấy sự kiện này.')
            return
            
        _render_detail_view(event_data, is_event=True)

def _render_detail_view(data, is_event=False):
    with ui.element('section').classes('w-full bg-background pb-20'):
        # Hero Image Header
        with ui.element('div').classes('relative h-[400px] md:h-[500px] w-full mb-12'):
            ui.image(data.get('image_url') or 'https://images.unsplash.com/photo-1526462981764-f6cf0f4ea260').classes('w-full h-full object-cover')
            with ui.element('div').classes('absolute inset-0 bg-gradient-to-t from-background to-transparent'):
                with theme.container().classes('h-full flex flex-col justify-end pb-12'):
                    ui.label(data.get('category' if not is_event else 'location', 'Văn hóa' if not is_event else 'Sự kiện')).classes('bg-primary text-white text-xs font-bold px-3 py-1 rounded-full w-fit mb-4 uppercase tracking-widest')
                    ui.label(data.get('title')).classes('font-display text-4xl md:text-5xl font-bold text-foreground mb-4 drop-shadow-sm')
                    with ui.row().classes('items-center gap-4 text-muted-foreground'):
                        with ui.row().classes('items-center gap-1'):
                            ui.icon('schedule', size='18px')
                            date_val = data.get('created_at' if not is_event else 'start_date', '')
                            ui.label(date_val[:10] if date_val else '--/--/----')
                        ui.label('|')
                        ui.label(f'Loại: {"Sự kiện" if is_event else "Tin tức"}')

        with theme.container().classes('grid grid-cols-1 lg:grid-cols-3 gap-12'):
            # Main Content
            with ui.column().classes('lg:col-span-2 gap-8'):
                if is_event:
                    with ui.card().classes('w-full p-6 bg-primary/5 border border-primary/20 rounded-2xl mb-6 shadow-sm'):
                        with ui.row().classes('items-center gap-4'):
                            ui.icon('place', color='primary', size='2rem')
                            with ui.column().classes('gap-0'):
                                ui.label('Địa điểm tổ chức').classes('text-xs text-primary font-bold uppercase tracking-wider')
                                ui.label(data.get('location', 'Bắc Ninh')).classes('text-lg font-bold')
                
                ui.label(data.get('content') or data.get('description', 'Chưa có thông tin chi tiết.')).classes('text-lg leading-relaxed text-foreground/90 whitespace-pre-line text-justify')
                
                if is_event:
                    with ui.row().classes('w-full justify-center mt-12'):
                        btn = ui.button('Đăng ký tham gia ngay').props('color="primary" unelevated size="lg" icon="how_to_reg"').classes('px-10 py-3 rounded-xl font-bold shadow-lg hover:scale-105 transition-transform')
                        btn.on('click', lambda: _show_registration_dialog(data.get('id'), data.get('title'), btn))

                # Share buttons
                with ui.row().classes('w-full items-center gap-4 py-8 border-y border-border mt-12'):
                    ui.label('Chia sẻ:').classes('font-bold text-sm uppercase text-muted-foreground')
                    ui.button(icon='facebook').props('flat round color="primary"')
                    ui.button(icon='share').props('flat round color="primary"')

            # Sidebar
            with ui.column().classes('gap-8'):
                ui.label('Khám phá thêm').classes('text-2xl font-bold font-display border-l-4 border-primary pl-4 mb-2')
                # Simple back button
                ui.button('Quay lại danh sách', on_click=lambda: ui.navigate.to('/tin-tuc')).props('flat icon="arrow_back" color="primary"').classes('font-bold')
                # Related content placeholder
                with ui.column().classes('gap-4'):
                    for i in range(1, 4):
                        with ui.row().classes('gap-4 group cursor-pointer pb-4 border-b border-border/50').on('click', lambda i=i: ui.navigate.to(f'/tin-tuc/{i}')):
                            ui.image(f'https://picsum.photos/id/{i+10}/100/100').classes('w-16 h-16 rounded-lg object-cover')
                            with ui.column().classes('gap-0'):
                                ui.label(f'Bài viết liên quan {i}').classes('text-sm font-bold group-hover:text-primary transition-colors')
                                ui.label('Xem chi tiết').classes('text-[10px] text-muted-foreground')
