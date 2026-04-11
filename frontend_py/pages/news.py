from nicegui import app, ui
import theme
import components
from api import api_client
import asyncio

@ui.page('/tin-tuc', response_timeout=60.0)
async def news_page():
    with theme.frame():
        components.page_header('Tin tức & Sự kiện', 'Cập nhật dòng chảy văn hóa Quan họ đương đại')

        state = type('state', (), {'filter': 'Tất cả'})()

        @ui.refreshable
        async def news_content():
            # Parallel data fetching
            tasks = [api_client.get_articles(), api_client.get_events()]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            articles = results[0] if isinstance(results[0], list) else []
            events = results[1] if isinstance(results[1], list) else []
            
            all_news = [{**a, 'ui_type': 'Tin tức'} for a in (articles or [])] + [{**e, 'ui_type': 'Sự kiện'} for e in (events or [])]
            filtered = [n for n in all_news if state.filter == 'Tất cả' or n['ui_type'] == state.filter]


            with ui.element('section').classes('py-20 w-full'):
                with theme.container():
                    components.filter_pills(['Tất cả', 'Tin tức', 'Sự kiện'], state.filter, lambda v: (setattr(state, 'filter', v), news_content.refresh()))
                    if not filtered:
                        components.empty_state('Không có dữ liệu phù hợp.')
                    else:
                        with ui.row().classes('grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 w-full'):
                            for item in filtered:
                                components.news_card(
                                    item.get('id'), item.get('title', 'Thông báo'),
                                    item.get('image_url', 'https://images.unsplash.com/photo-1599908608021-b5d929aa054e?auto=format&fit=crop&q=80&w=400'),
                                    type=item.get('ui_type', 'Tin tức'), date=(item.get('created_at') or item.get('start_date') or '--/--/----')[:10],
                                )
        await news_content()

@ui.page('/tin-tuc/{id}')
async def news_detail_page(id: int):
    with theme.frame():
        news_data = await api_client.get_article(id)
        if not news_data:
            components.empty_state('Không tìm thấy bản tin này.')
            return
            
        with ui.element('section').classes('py-16 bg-background w-full'):
            with theme.container().classes('max-w-3xl'):
                ui.label(news_data.get('title', 'Tiêu đề')).classes('font-display text-3xl md:text-4xl font-bold mb-4')
                ui.label(news_data.get('content', '')).classes('text-lg text-foreground whitespace-pre-line leading-relaxed')

@ui.page('/su-kien/{id}')
async def event_detail_page(id: int):
    with theme.frame():
        event_data = await api_client.get_event(id)
        if not event_data:
            components.empty_state('Không tìm thấy sự kiện này.')
            return
            
        with ui.element('section').classes('py-16 bg-background w-full'):
            with theme.container().classes('max-w-3xl'):
                ui.label(event_data.get('title', 'Tên sự kiện')).classes('font-display text-3xl font-bold mb-4')
                ui.label(event_data.get('description', '')).classes('text-lg text-foreground whitespace-pre-line leading-relaxed')
