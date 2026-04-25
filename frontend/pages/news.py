from nicegui import app, ui
import theme
import components
from api import api_client
import asyncio
from datetime import datetime
from translation import t, tc

def _show_registration_dialog(event_item, button_ref):
    event_id = event_item.get('id')
    title = event_item.get('title')
    token = app.storage.user.get('token') or app.storage.user.get('access_token')
    if not token:
        with ui.dialog() as dialog, ui.card().classes('p-8 rounded-2xl shadow-elevated border border-border bg-card max-w-sm w-full'):
            with ui.column().classes('items-center gap-4 text-center w-full'):
                with ui.element('div').classes('flex h-16 w-16 items-center justify-center rounded-full bg-primary/10 text-primary mb-2'):
                    ui.icon('lock_person', size='2rem')
                ui.label(t('login_required')).classes('text-2xl font-bold font-display text-foreground')
                ui.label(t('login_message')).classes('text-muted-foreground text-sm leading-relaxed')
                with ui.row().classes('w-full justify-center gap-3 mt-4 flex-nowrap'):
                    ui.button(t('close'), on_click=dialog.close).props('outline color="grey"').classes('flex-1 rounded-lg')
                    ui.button(t('login'), on_click=lambda: ui.navigate.to('/dang-nhap')).props('color="primary" unelevated').classes('flex-1 rounded-lg font-bold')
        dialog.open()
    else:
        user_name = app.storage.user.get('user_name', '')
        email_val = app.storage.user.get('email', '')

        with ui.dialog() as dialog, ui.card().classes('p-0 w-[500px] max-w-[95vw] rounded-3xl overflow-hidden glass-card shadow-elevated border-none'):
            # Decorative Header with Pattern
            with ui.element('div').classes('w-full h-32 bg-hero-gradient relative overflow-hidden flex items-center px-8'):
                with ui.element('div').classes('absolute -right-4 -top-4 opacity-10'):
                    ui.icon('lotus', size='10rem', color='white')
                with ui.column().classes('gap-0 z-10'):
                    ui.label(t('register_event')).classes('text-white/70 text-sm font-bold uppercase tracking-widest')
                    ui.label(title).classes('text-white text-2xl font-bold font-display line-clamp-1 mt-1')
            
            with ui.column().classes('w-full p-8 gap-6 bg-white/40'):
                with ui.column().classes('w-full gap-4'):
                    name_input = ui.input(t('name_required')).classes('w-full modern-input').props('outlined rounded-2xl')
                    name_input.value = user_name
                    
                    email_input = ui.input(t('email_field')).classes('w-full modern-input').props('outlined rounded-2xl')
                    email_input.value = email_val
                    
                    phone_input = ui.input(t('phone_required')).classes('w-full modern-input').props('outlined rounded-2xl')
                    note_input = ui.textarea(t('note_field')).classes('w-full modern-input').props('outlined rounded-2xl auto-grow')
                
                status_label = ui.label("").classes("text-negative text-sm font-medium hidden bg-negative/5 px-4 py-3 rounded-xl w-full text-center border border-negative/10")
                
                async def submit():
                    if not phone_input.value or not name_input.value:
                        status_label.text = t('required_fields')
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
                        ui.notify(t('register_success'), type='positive', position='top', icon='check_circle')
                        button_ref.text = t('already_registered')
                        button_ref.props('color="grey" disable icon="check_circle"')
                    else:
                        error_msg = api_client.get_last_error()
                        if error_msg and "Already registered" in error_msg:
                            status_label.text = t('already_registered')
                        else:
                            status_label.text = t('register_failed')
                        status_label.classes(remove='hidden')

                with ui.row().classes('w-full justify-between items-center mt-4'):
                    ui.button(t('cancel'), on_click=dialog.close).props('flat color="grey"').classes('px-6 rounded-xl font-bold lowercase')
                    sub_btn = ui.button(t('confirm_register'), on_click=submit).props('color="primary" unelevated').classes('px-10 py-3 rounded-2xl font-bold elevated-btn shadow-lg')
        dialog.open()

@ui.page('/tin-tuc', response_timeout=60.0)
async def news_page():
    with theme.frame():
        components.page_header(t('news_title'), t('news_subtitle'))
        
        # Shared state
        class NewsState:
            def __init__(self):
                self.search_query = ''
                self.month_filter = t('all_categories')
                self.year_filter = t('all_categories')
                
                self.news_page = 1
                self.events_page = 1
                self.items_per_page = 8

                self.news_count = 0
                self.news_items = []
                self.events_count = 0
                self.events_items = []

        state = NewsState()

        @ui.refreshable
        async def content_area():
            # Load News with Search
            state.news_count = await api_client.get_articles_count(article_type='tin-tuc', search=state.search_query)
            news_skip = (state.news_page - 1) * state.items_per_page
            state.news_items = await api_client.get_articles(article_type='tin-tuc', skip=news_skip, limit=state.items_per_page, search=state.search_query)

            # Load Events with Search
            state.events_count = await api_client.get_events_count(search=state.search_query)
            events_skip = (state.events_page - 1) * state.items_per_page
            state.events_items = await api_client.get_events(skip=events_skip, limit=state.items_per_page, search=state.search_query)

            with ui.tabs().classes('w-full border-b border-border bg-card/30 rounded-t-2xl shadow-sm') as tabs:
                news_tab = ui.tab(t('news_tab'), icon='article').classes('font-bold px-4 sm:px-8 py-4')
                event_tab = ui.tab(t('events_tab'), icon='event').classes('font-bold px-4 sm:px-8 py-4')

            with ui.tab_panels(tabs, value=news_tab).classes('w-full bg-transparent p-0 mt-8'):
                with ui.tab_panel(news_tab).classes('p-0 w-full'):
                    if not state.news_items:
                        components.empty_state(t('no_news'))
                    else:
                        with ui.row().classes('grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 w-full'):
                            for item in state.news_items:
                                components.news_grid_card(item)
                        
                        # Pagination UI for News
                        class NewsPageState:
                            def __init__(self, page, ipp):
                                self.page = page
                                self.items_per_page = ipp
                            def __setattr__(self, name, value):
                                super().__setattr__(name, value)
                                if name == 'page': setattr(state, 'news_page', value)
                        
                        news_pagination_state = NewsPageState(state.news_page, state.items_per_page)
                        components.pagination_controls(news_pagination_state, state.news_count, content_area)

                with ui.tab_panel(event_tab).classes('p-0 w-full'):
                    if not state.events_items:
                        components.empty_state(t('no_news'))
                    else:
                        with ui.row().classes('grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 w-full'):
                            for item in state.events_items:
                                components.event_grid_card(item, on_register=_show_registration_dialog)
                        
                        # Pagination UI for Events
                        class EventPageState:
                            def __init__(self, page, ipp):
                                self.page = page
                                self.items_per_page = ipp
                            def __setattr__(self, name, value):
                                super().__setattr__(name, value)
                                if name == 'page': setattr(state, 'events_page', value)
                        
                        event_pagination_state = EventPageState(state.events_page, state.items_per_page)
                        components.pagination_controls(event_pagination_state, state.events_count, content_area)

        with ui.element('section').classes('pt-6 pb-16 bg-background min-h-screen'):
            with theme.container():
                # Modern Filter Bar (Flexible layout)
                with ui.element('div').classes('modern-search-card mb-6 w-full p-3 rounded-xl flex flex-col sm:flex-row items-center gap-3 relative z-50'):
                    search = ui.input(
                        placeholder=t('search_news'),
                        on_change=lambda e: (setattr(state, 'search_query', e.value or ''), setattr(state, 'news_page', 1), setattr(state, 'events_page', 1), content_area.refresh())
                    ).classes('modern-input flex-1 w-full bg-background rounded-lg').props('outlined clearable debounce=500 icon=search')
                    
                    with ui.row().classes('flex-1 w-full sm:w-auto items-center justify-between sm:justify-end gap-3'):
                        months = ['All'] + [str(i) for i in range(1, 13)]
                        month_sel = ui.select(
                            {m: (t('all_categories') if m == 'All' else f"{t('month_label')} {m}") for m in months}, 
                            value='All',
                            label=t('month_label'),
                            on_change=lambda e: (setattr(state, 'month_filter', e.value if e.value != 'All' else ''), setattr(state, 'news_page', 1), setattr(state, 'events_page', 1), content_area.refresh())
                        ).classes('modern-select w-28 sm:w-36 bg-background').props('outlined rounded-lg options-dense')
                        
                        years = [t('all_categories'), '2024', '2025', '2026']
                        year_sel = ui.select(
                            years, 
                            value=t('all_categories'),
                            label=t('year_label'),
                            on_change=lambda e: (setattr(state, 'year_filter', e.value or t('all_categories')), setattr(state, 'news_page', 1), setattr(state, 'events_page', 1), content_area.refresh())
                        ).classes('modern-select w-28 sm:w-36 bg-background').props('outlined dense rounded-lg options-dense')
                        
                        if app.storage.user.get('role') == 'admin':
                            with ui.row().classes('gap-2 shrink-0'):
                                ui.button(icon='add_circle', on_click=lambda: ui.navigate.to('/admin/edit/news/0')).props('unelevated round size=md').classes('bg-primary text-white shadow-md hover:scale-110 transition-transform cursor-pointer pointer-events-auto')
                                ui.button(icon='event', on_click=lambda: ui.navigate.to('/admin/edit/event/0')).props('unelevated round size=md color=secondary').classes('shadow-md hover:scale-110 transition-transform cursor-pointer pointer-events-auto')

                await content_area()

@ui.page('/tin-tuc/{id}')
async def article_detail_page(id: int):
    with theme.frame():
        news_data = await api_client.get_article(id)
        # Fetch related news for the sidebar
        try:
            related = await api_client.get_articles(article_type='tin-tuc')
            related = [n for n in related if n.get('id') != id][:3]
        except:
            related = []

        await _render_detail_view(news_data, is_event=False, related_news=related)

@ui.page('/su-kien/{id}')
async def event_detail_page(id: int):
    with theme.frame():
        event_data = await api_client.get_event(id)
        # Fetch related events for the sidebar
        try:
            related = await api_client.get_events()
            related = [e for e in related if e.get('id') != id][:3]
        except:
            related = []

        await _render_detail_view(event_data, is_event=True, related_news=related)

async def _render_detail_view(data, is_event=False, related_news=None):
    if not data:
        components.empty_state(t('updating'))
        return

    with ui.element('section').classes('relative w-full bg-background bg-paper-texture pb-24 overflow-hidden'):
        # Cultural decoration
        ui.image('/static/common/lotus-pattern.png').classes('absolute -right-20 -top-20 w-80 opacity-5 pointer-events-none rotate-12')
        ui.image('/static/common/lotus-pattern.png').classes('absolute -left-20 bottom-20 w-64 opacity-5 pointer-events-none -rotate-12')

        # Elegant Header with Masking
        with ui.element('div').classes('relative w-full h-[450px] md:h-[550px] mb-[-60px] z-0 overflow-hidden'):
            with ui.image(data.get('image_url') or 'https://images.unsplash.com/photo-1526462981764-f6cf0f4ea260').classes('w-full h-full object-cover transition-transform duration-1000 hover:scale-105'):
                with ui.element('div').classes('absolute inset-0 bg-gradient-to-b from-black/40 via-transparent to-background/90'):
                    with theme.container().classes('h-full flex flex-col justify-center pt-20'):
                        # Breadcrumbs
                        with ui.row().classes('items-center gap-2 mb-6 text-xs font-black tracking-widest uppercase text-white/80'):
                            ui.link(t('nav_home'), '/').classes('hover:text-primary transition-colors no-underline text-white')
                            ui.label('/')
                            ui.link(t('news_title'), '/tin-tuc').classes('hover:text-primary transition-colors no-underline text-white')
                            ui.label('/')
                            ui.label(t('event_label') if is_event else t('news_label')).classes('text-white')

                        ui.label(tc(data, 'title')).classes('font-display text-3xl md:text-5xl lg:text-6xl font-black text-white mb-4 drop-shadow-2xl max-w-4xl tracking-tight leading-tight')
                        
                        with ui.row().classes('items-center gap-6 text-white/90'):
                            with ui.row().classes('items-center gap-2'):
                                ui.icon('schedule', size='20px').classes('text-white/60')
                                date_val = data.get('created_at' if not is_event else 'start_date', '')
                                ui.label(date_val[:10] if date_val else '--/--/----').classes('text-lg font-bold')
                            ui.element('div').classes('h-4 w-[1px] bg-white/30')
                            ui.label(tc(data, 'category') or (t('event_label') if is_event else t('news_label'))).classes('text-sm font-black uppercase tracking-wider')

        with theme.container().classes('relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-12'):
            # Main Content Column
            with ui.column().classes('lg:col-span-8 gap-8'):
                with ui.card().classes('w-full p-8 md:p-14 rounded-[32px] border border-border bg-white shadow-elevated').style('box-shadow: 0 20px 50px -10px rgba(0,0,0,0.05)'):
                    if is_event:
                        with ui.element('div').classes('flex flex-wrap items-center gap-6 p-6 bg-primary/5 rounded-2xl mb-10 border border-primary/10'):
                            with ui.row().classes('items-center gap-3'):
                                ui.icon('place', color='primary', size='24px')
                                with ui.column().classes('gap-0'):
                                    ui.label(t('village_location_title')).classes('text-[10px] text-primary font-black uppercase tracking-tight')
                                    ui.label(tc(data, 'location') or t('hero_bac_ninh')).classes('text-base font-bold')
                            
                            with ui.row().classes('items-center gap-3'):
                                ui.icon('how_to_reg', color='primary', size='24px')
                                with ui.column().classes('gap-0'):
                                    ui.label(t('status_label')).classes('text-[10px] text-primary font-black uppercase tracking-tight')
                                    ui.label(t('status_upcoming')).classes('text-base font-bold')

                    # Article Content - Rendered as HTML to support rich text from database
                    ui.html(tc(data, 'content') or tc(data, 'description') or t('updating')).classes('text-xl leading-[2.2] text-foreground/90 text-justify font-medium')
                    
                    if is_event:
                        with ui.row().classes('w-full justify-center mt-16 pt-8 border-t border-border/40'):
                            is_reg = data.get('is_registered', False)
                            btn_text = t('already_registered') if is_reg else t('register_event')
                            btn_props = 'color="grey" disable icon="check_circle"' if is_reg else 'color="primary" unelevated size="lg" icon="how_to_reg"'
                            
                            btn = ui.button(btn_text).props(btn_props).classes('px-12 py-4 rounded-2xl font-black shadow-xl shadow-primary/20 hover:scale-105 transition-transform uppercase tracking-widest')
                            if not is_reg:
                                btn.on('click', lambda: _show_registration_dialog(data, btn))
                    
                    # Social Interaction Row
                    with ui.row().classes('w-full items-center justify-between py-10 border-t border-border/40 mt-16'):
                        with ui.row().classes('items-center gap-4'):
                            ui.label(f"{t('footer_connect')}:").classes('font-black text-xs uppercase text-muted-foreground tracking-widest')
                            ui.button(icon='facebook').props('flat round color="primary"').classes('bg-primary/5')
                            ui.button(icon='share').props('flat round color="primary"').classes('bg-primary/5')
                        
                        ui.button(t('back_to_library'), on_click=lambda: ui.navigate.to('/tin-tuc')).props('flat icon="arrow_back"').classes('font-black text-xs uppercase tracking-widest text-primary')

                # Comment Section (Studio Integrated)
                with ui.column().classes('w-full mt-8 gap-8'):
                    ui.label(t('comments_title')).classes('text-3xl font-display font-black border-l-8 border-primary pl-6 py-2 tracking-tight')
                    
                    @ui.refreshable
                    async def render_news_comments():
                        comments = await api_client.get_comments(article_id=data['id'])
                        if not comments:
                            with ui.card().classes('w-full p-12 flex flex-col items-center justify-center border border-dashed border-border bg-card/40 opacity-60'):
                                ui.icon('chat_bubble_outline', size='3rem').classes('text-muted-foreground/30 mb-4')
                                ui.label(t('no_comments')).classes('text-sm italic font-medium')
                        else:
                            with ui.column().classes('gap-8 w-full'):
                                for c in comments:
                                    with ui.row().classes('gap-6 items-start w-full group'):
                                        with ui.column().classes('shrink-0'):
                                            ui.avatar(icon='account_circle', color='muted-foreground').classes('shadow-lg border-2 border-white size-12')
                                        
                                        with ui.column().classes('flex-1 gap-2'):
                                            with ui.row().classes('items-center justify-between w-full'):
                                                with ui.row().classes('items-center gap-3'):
                                                    ui.label((c.get('user') or {}).get('name', t('anonymous'))).classes('font-bold text-base text-foreground')
                                                    ui.label(c.get('created_at', '')[:10]).classes('text-[10px] text-muted-foreground font-black tracking-widest uppercase')
                                                
                                                if app.storage.user.get('role') == 'admin':
                                                    async def del_com(c_id=c['id']):
                                                        if await api_client.delete_comment(c_id):
                                                            ui.notify(t('deleted_comment'), type='positive')
                                                            render_news_comments.refresh()
                                                    ui.button(icon='delete', on_click=del_com).props('flat round dense size=sm color=negative').classes('opacity-0 group-hover:opacity-100 transition-opacity bg-negative/5')
                                            
                                            with ui.card().classes('w-full p-5 rounded-2xl rounded-tl-none border border-border/50 bg-white/80 backdrop-blur-sm shadow-sm'):
                                                ui.label(c.get('content')).classes('text-base text-foreground/80 leading-relaxed')
                    
                    await render_news_comments()

                    if app.storage.user.get('is_authenticated'):
                        with ui.card().classes('w-full p-6 md:p-8 bg-white border border-border rounded-3xl shadow-sm mt-4'):
                            with ui.row().classes('w-full items-start gap-4'):
                                ui.avatar(icon='person', color='primary').classes('shadow-md size-12')
                                with ui.column().classes('flex-1 gap-4'):
                                    comment_input = ui.textarea(placeholder=t('comment_placeholder')).props('outlined rounded-2xl autogrow counter maxLength=500').classes('w-full modern-input bg-white/80 text-base')
                                    async def post_news_comment():
                                        if not comment_input.value.strip(): return
                                        res = await api_client.create_comment(content=comment_input.value, article_id=data['id'])
                                        if res:
                                            comment_input.value = ''
                                            ui.notify(t('comment_sent'), icon='check_circle', color='positive')
                                            render_news_comments.refresh()
                                    ui.button(t('post_comment'), icon='send', on_click=post_news_comment).props('unelevated rounded-xl size=lg').classes('bg-primary text-white font-black px-10 self-end shadow-lg shadow-primary/20')
                    else:
                        with ui.card().classes('w-full p-10 border border-dashed border-border bg-card/30 flex flex-col items-center gap-4 text-center'):
                            ui.label(t('comment_login_hint')).classes('text-base font-medium text-muted-foreground')
                            ui.button(t('login'), on_click=lambda: ui.navigate.to('/dang-nhap')).props('unelevated rounded-full color=primary').classes('px-10 font-bold')

            # Sidebar (Related / Meta)
            with ui.column().classes('lg:col-span-4 gap-8'):
                if is_event and app.storage.user.get('role') == 'admin':
                    regs = await api_client.get_event_registrations(data.get('id'))
                    with ui.card().classes('w-full p-6 bg-card border border-border rounded-[24px] shadow-sm'):
                        ui.label(t('registration_list')).classes('text-lg font-black uppercase tracking-widest text-primary mb-6 border-b border-primary/10 pb-2')
                        if not regs:
                            ui.label(t('no_registrations')).classes('text-muted-foreground italic text-sm')
                        else:
                            with ui.column().classes('gap-4 w-full'):
                                for r in regs:
                                    with ui.row().classes('w-full justify-between items-center bg-white p-3 rounded-xl border border-border/30'):
                                        ui.label(r.get('name') or (r.get('user') or {}).get('name', 'N/A')).classes('font-bold text-sm')
                                        ui.label(r.get('phone') or 'N/A').classes('text-[10px] font-black opacity-60 bg-muted px-2 py-0.5 rounded')

                # Sidebar Widget: Related News
                with ui.card().classes('w-full p-8 border border-white/40 bg-white/40 backdrop-blur-xl rounded-[32px] sticky top-24'):
                    ui.label(t('footer_explore')).classes('text-sm font-black uppercase tracking-[0.3em] text-primary mb-8 border-b-2 border-primary/20 pb-3')
                    
                    related_news = related_news or []
                    if not related_news:
                        ui.label(t('updating')).classes('text-xs italic text-muted-foreground')
                    else:
                        with ui.column().classes('gap-8 w-full'):
                            for art in related_news:
                                target = f'/su-kien/{art["id"]}' if is_event else f'/tin-tuc/{art["id"]}'
                                with ui.row().classes('gap-4 group cursor-pointer items-center').on('click', lambda a=target: ui.navigate.to(a)):
                                    with ui.element('div').classes('shrink-0 w-20 h-20 rounded-2xl overflow-hidden shadow-md'):
                                        ui.image(art.get('image_url') or 'https://picsum.photos/seed/quanho/100/100').classes('w-full h-full object-cover transition-transform group-hover:scale-110 duration-500')
                                    with ui.column().classes('gap-1 flex-1'):
                                        ui.label(art.get('title')).classes('text-sm font-bold group-hover:text-primary transition-colors line-clamp-2 leading-tight')
                                        ui.label(t('card_view_detail')).classes('text-[9px] font-black uppercase tracking-widest text-muted-foreground/60')

                # Sidebar Decorative
                with ui.element('div').classes('w-full p-8 flex justify-center opacity-30 mt-4'):
                    ui.image('/static/common/lotus-pattern.png').classes('w-20')
