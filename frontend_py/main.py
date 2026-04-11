from nicegui import app, ui
import theme
import components
from api import api_client
import asyncio
import os
import re
import uuid
from typing import Optional, List, Dict

def get_embed_url(video_url: str) -> Optional[str]:
    if not video_url: return None
    video_url = video_url.strip()
    
    # Standard YouTube regex for various formats
    yt_regex = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
    match = re.search(yt_regex, video_url)
    
    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/embed/{video_id}?rel=0"
    
    # If it's already an embed URL or other video source, return as is
    return video_url

# ---------------------------------------------------------------------------
# Serve static files
# ---------------------------------------------------------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
app.add_static_files('/static', os.path.join(current_dir, 'static'))


# ---------------------------------------------------------------------------
# Pages  –  dùng @theme.page_layout('/path') thay cho cặp decorator cũ
# ---------------------------------------------------------------------------

@ui.page('/')
async def home_page():
    with theme.frame():
        components.hero_banner()

        with ui.element('section').classes('py-24 bg-background w-full'):
            with theme.container():
                components.section_title('Bài hát nổi bật', 'Những làn điệu Quan họ kinh điển được yêu thích nhất')

                melodies = await api_client.get_melodies()
                featured_melodies = melodies[:3] if melodies else []

                if not featured_melodies:
                    with ui.row().classes('w-full justify-center py-20'):
                        ui.spinner(size='xl', color='primary', thickness=2)
                else:
                    with ui.row().classes('grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 w-full'):
                        cat_map = {'co': 'Làn điệu cổ', 'moi': 'Làn điệu mới', 'cai-bien': 'Làn điệu cải biên'}
                        for song in featured_melodies:
                            components.song_card(
                                song.get('id'),
                                song.get('name', 'Không tiêu đề'),
                                song.get('artist', {}).get('name', 'Nghệ nhân') if isinstance(song.get('artist'), dict) else 'Nghệ nhân',
                                song.get('image_url') or 'https://images.unsplash.com/photo-1599908608021-b5d929aa054e?auto=format&fit=crop&q=80&w=400',
                                melody=cat_map.get(song.get('category'), 'Làn điệu cổ'),
                                duration=song.get('duration'),
                            )

                with ui.row().classes('mt-12 w-full justify-center'):
                    with ui.link(target='/bai-hat').classes('no-underline flex items-center gap-2 text-primary font-bold cursor-pointer group'):
                        ui.label('Khám phá thư viện').classes('text-sm uppercase tracking-widest')
                        ui.icon('arrow_forward', size='20px').classes('group-hover:translate-x-1 transition-transform')

        components.hero_stats_section()

        with ui.element('section').classes('py-24 bg-background w-full'):
            with theme.container():
                components.section_title('Nghệ nhân tiêu biểu', 'Những người giữ lửa cho di sản Quan họ muôn đời')

                artists_data = await api_client.get_artists()
                featured_artists = artists_data[:4] if artists_data else []

                if not featured_artists:
                    ui.label('Đang tìm kiếm nghệ nhân...').classes('w-full text-center py-10 italic text-muted-foreground')
                else:
                    with ui.row().classes('grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 w-full'):
                        for i, artist in enumerate(featured_artists):
                            components.artist_card(
                                artist.get('id'),
                                artist.get('name', 'Nghệ nhân'),
                                artist.get('image_url', '/static/chatbot-avatar.png'),
                                artist.get('village', 'Kinh Bắc'),
                                index=i
                            )

        with ui.element('section').classes('bg-card py-24 border-t border-border w-full'):
            with theme.container():
                components.section_title('Tin tức & Sự kiện', 'Cập nhật hoạt động văn hóa tiêu biểu')

                articles = await api_client.get_articles()
                events   = await api_client.get_events()
                news_items = (articles[:2] if articles else []) + (events[:2] if events else [])

                if not news_items:
                    ui.label('Không có tin tức mới.').classes('w-full text-center py-10 opacity-50')
                else:
                    with ui.row().classes('grid grid-cols-1 lg:grid-cols-2 gap-6 w-full'):
                        for item in news_items:
                            components.news_card(
                                item.get('id'),
                                item.get('title', 'Thông báo mới'),
                                item.get('image_url', 'https://images.unsplash.com/photo-1526462981764-f6cf0f4ea260?auto=format&fit=crop&q=80&w=400'),
                                type='Sự kiện' if 'start_date' in item else 'Tin tức',
                                date=(item.get('created_at') or item.get('start_date') or '--/--/----')[:10],
                            )

                    with ui.row().classes('mt-12 w-full justify-center'):
                        with ui.link(target='/tin-tuc').classes('no-underline flex items-center gap-2 text-primary font-bold cursor-pointer group'):
                            ui.label('Xem thêm tin tức').classes('text-sm uppercase tracking-widest')
                            ui.icon('arrow_forward', size='20px').classes('group-hover:translate-x-1 transition-transform')


@ui.page('/gioi-thieu')
def introduction_page():
    with theme.frame():
        with ui.element('section').classes('relative min-h-[70vh] flex items-center justify-center overflow-hidden w-full').style('padding-top: 56px;'):
            ui.image('/static/hero-banner.jpg').classes('absolute inset-0 h-full w-full object-cover')
            ui.element('div').classes('absolute inset-0 bg-hero-gradient opacity-80')
            with ui.column().classes('relative z-10 text-center items-center px-4 gap-6'):
                ui.label('LỊCH SỬ VÀ GIÁ TRỊ VĂN HÓA').classes('text-xs font-bold tracking-[0.4em] text-gold-light uppercase animate-fade-in')
                with ui.column().classes('gap-2 animate-fade-in-up'):
                    ui.label('Giới thiệu').classes('font-display text-3xl md:text-4xl font-bold text-white/90 shadow-sm')
                    ui.label('Quan Họ Bắc Ninh').classes('font-display text-5xl md:text-8xl font-black text-gradient-gold drop-shadow-2xl')
            
            # Scroll Arrow
            with ui.element('div').classes('absolute bottom-10 left-1/2 -translate-x-1/2 z-10 flex flex-col items-center gap-2 cursor-pointer opacity-70 hover:opacity-100 transition-opacity').style('animation: float 2.5s ease-in-out infinite;'):
                ui.label('Khám phá').classes('text-white/50 text-[10px] uppercase tracking-[0.3em] font-bold')
                ui.icon('expand_more', size='32px').classes('text-white')

        with ui.element('section').classes('py-24 bg-background w-full'):
            with theme.container():
                components.section_title('Quan họ là gì?')
                with ui.column().classes('max-w-4xl mx-auto text-center items-center gap-8 text-muted-foreground text-lg md:text-xl leading-relaxed font-light'):
                    ui.label('Dân ca Quan họ Bắc Ninh là một hình thức hát giao duyên đối đáp giữa nam (liền anh) và nữ (liền chị), phổ biến tại vùng Kinh Bắc xưa, nay là tỉnh Bắc Ninh và Bắc Giang.')
                    ui.label('Năm 2009, Quan họ được UNESCO vinh danh là Di sản Văn hóa Phi vật thể đại diện của Nhân loại, khẳng định sức sống mãnh liệt và giá trị nhân văn sâu sắc của thể loại âm nhạc này.').classes('bg-primary/5 p-8 rounded-3xl border border-primary/10 text-foreground italic')

        with ui.element('section').classes('py-24 bg-card/60 border-y border-border w-full relative overflow-hidden'):
            # Decorative patterns
            ui.image('/static/lotus-ornament.png').classes('absolute -left-20 -top-20 w-80 h-80 opacity-[0.03] rotate-12 pointer-events-none')
            with theme.container():
                components.section_title('Bản Sắc Nghệ Thuật', 'Khám phá những nét đặc trưng làm nên linh hồn của dân ca Quan họ.')
                with ui.row().classes('grid gap-10 md:grid-cols-3 mt-8 w-full items-stretch'):
                    components.intro_feature_card('music_note', 'Lề lối giao duyên', 'Lối hát đối đáp nam nữ với kỹ thuật "Vang, Rền, Nền, Nảy" điêu luyện, tinh tế trong từng nhịp phách.')
                    components.intro_feature_card('groups', 'Tục kết chạ', 'Sự gắn kết thiêng liêng giữa các làng Quan họ, tạo nên cộng đồng gắn bó bền chặt qua nhiều thế hệ.')
                    components.intro_feature_card('favorite', 'Liền anh, Liền chị', 'Cách xưng hô đầy trân trọng, thanh lịch thể hiện nét văn hóa ứng xử Kinh Bắc hào hoa, phong nhã.')

        with ui.element('section').classes('py-32 bg-background w-full relative overflow-hidden'):
            # Subtle background pattern for the whole section
            ui.element('div').classes('absolute inset-0 bg-pattern-lotus opacity-[0.4] pointer-events-none')
            
            with theme.container():
                components.section_title('Trang Phục Truyền Thống', 'Mỗi bộ trang phục là một tác phẩm nghệ thuật mang đậm dấu ấn dân gian.')
                with ui.column().classes('mt-16 gap-32 w-full'):
                    components.costume_block(
                        'Trang phục Liền chị',
                        'Nổi bật với chiếc áo mớ ba mớ bảy rực rỡ, vuông mỏ quạ đội đầu, nón quai thao thắt dải lụa thướt tha mang vẻ đẹp dịu dàng nhưng đầy kiêu sa.',
                        'https://images.unsplash.com/photo-1580974852861-c381510bc98a?auto=format&fit=crop&q=80&w=800',
                        items=['Áo mớ ba mớ bảy', 'Nón quai thao', 'Khăn mỏ quạ', 'Dải yếm đào'],
                    )
                    components.costume_block(
                        'Trang phục Liền anh',
                        'Đậm chất nam nhi Kinh Bắc với áo the đen bóng bẩy, quần lụa trắng, khăn xếp và chiếc ô đen che nghiêng - biểu tượng của sự thanh lịch.',
                        'https://images.unsplash.com/photo-1583795484071-3c453e3a7c71?auto=format&fit=crop&q=80&w=800',
                        items=['Áo the thâm', 'Khăn xếp', 'Quần lụa trắng', 'Ô đen truyền thống'],
                        reverse=True,
                    )

        with ui.element('section').classes('py-32 bg-card/40 border-t border-border w-full relative'):
            with theme.container().classes('max-w-6xl'):
                components.section_title('Dòng chảy lịch sử', 'Hành trình ngàn năm kiến tạo nên tâm hồn người Việt.')
                with ui.column().classes('mt-24 gap-0 w-full'):
                    timeline_data = [
                        ('Thế kỷ XV',   'Quan họ bắt đầu hình thành tại vùng vựa lúa Kinh Bắc, gắn liền với các lễ hội phồn thực làng xã.'),
                        ('Thế kỷ XVII-XVIII', 'Thời kỳ phát triển rực rỡ nhất với hệ thống làng Quan họ gốc được xác lập vững chắc.'),
                        ('Thế kỷ XIX',  'Trở thành biểu tượng văn hóa tiêu biểu nhất của xứ Bắc, được triều đình và dân gian coi trọng.'),
                        ('2009',       'Chính thức được UNESCO vinh danh là Di sản văn hóa phi vật thể của nhân loại tại Abu Dhabi.'),
                    ]
                    for i, (year, text) in enumerate(timeline_data):
                        components.timeline_item(year, text, index=i, total=len(timeline_data))

        with ui.element('section').classes('py-24 bg-background border-t border-border w-full'):
            with theme.container().classes('max-w-4xl text-center flex flex-col items-center'):
                components.unesco_quote(
                    'Dân ca Quan họ Bắc Ninh thể hiện tính cộng đồng, sự chia sẻ, tình yêu quê hương đất nước và lòng mến khách của người dân Việt Nam.',
                    subtitle='GIÁ TRỊ DI SẢN NHÂN LOẠI'
                )


@ui.page('/bai-hat')
async def songs_page():
    with theme.frame():
        components.page_header('Thư viện bài hát', 'Kho tàng các làn điệu Quan họ Kinh Bắc được sưu tầm và gìn giữ')

        state = type('state', (), {'search': '', 'category': 'Tất cả'})()

        @ui.refreshable
        async def songs_content():
            if state.search:
                melodies = await api_client.search_melodies(state.search)
            else:
                melodies = await api_client.get_melodies()
            
            if state.category != 'Tất cả':
                cat_map = {'Làn điệu cổ': 'co', 'Làn điệu mới': 'moi', 'Làn điệu cải biên': 'cai-bien'}
                target_cat = cat_map.get(state.category)
                melodies = [m for m in melodies if m.get('category') == target_cat]

            with ui.element('section').classes('py-20 bg-background w-full'):
                with theme.container():
                    with ui.row().classes('mb-12 w-full gap-4 items-center bg-card p-6 rounded-2xl border border-border shadow-sm'):
                        search_input = ui.input(placeholder='Tìm kiếm bài hát...', value=state.search).props('outlined dense borderless').classes('flex-1 bg-background rounded-lg px-4')
                        search_input.on('keydown.enter', lambda e: (setattr(state, 'search', e.sender.value), songs_content.refresh()))
                        
                        cat_select = ui.select(['Tất cả', 'Làn điệu cổ', 'Làn điệu mới', 'Làn điệu cải biên'], value=state.category).props('dense outlined').classes('w-48 bg-background')
                        cat_select.on('change', lambda e: (setattr(state, 'category', e.value), songs_content.refresh()))
                        
                        ui.button(icon='search', on_click=lambda: (setattr(state, 'search', search_input.value), songs_content.refresh())).props('flat round').classes('text-primary')
                        
                        # Only show 'Add Song' if admin
                        if app.storage.user.get('role') == 'admin':
                            ui.button('Thêm bài hát', icon='add', on_click=lambda: ui.navigate.to('/them-bai-hat')).props('unelevated rounded-lg').classes('bg-primary text-white font-bold ml-auto max-md:hidden')
                            ui.button(icon='add', on_click=lambda: ui.navigate.to('/them-bai-hat')).props('unelevated rounded-lg').classes('bg-primary text-white font-bold md:hidden')

                    if not melodies:
                        components.empty_state('Không tìm thấy bài hát nào.')
                    else:
                        with ui.row().classes('grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 w-full'):
                            cat_map_label = {'co': 'Làn điệu cổ', 'moi': 'Làn điệu mới', 'cai-bien': 'Làn điệu cải biên'}
                            for song in melodies:
                                components.song_card(
                                    song.get('id'),
                                    song.get('name', 'Không tiêu đề'),
                                    song.get('artist', {}).get('name', 'Nghệ nhân') if isinstance(song.get('artist'), dict) else 'Nghệ nhân',
                                    song.get('image_url') or 'https://images.unsplash.com/photo-1599908608021-b5d929aa054e?auto=format&fit=crop&q=80&w=400',
                                    melody=cat_map_label.get(song.get('category'), 'Làn điệu cổ'),
                                    duration=song.get('duration'),
                                )
        
        await songs_content()


@ui.page('/nghe-nhan')
async def artists_page():
    with theme.frame():
        components.page_header('Nghệ nhân tiêu biểu', 'Những người nắm giữ hồn cốt và trao truyền di sản cho thế hệ mai sau')

        with ui.element('section').classes('py-20 bg-background w-full'):
            with theme.container():
                with ui.row().classes('mb-8 w-full justify-end'):
                    ui.button('Thêm nghệ nhân', icon='person_add', on_click=lambda: ui.navigate.to('/them-nghe-nhan')).props('unelevated rounded-lg').classes('bg-primary text-white font-bold')

                artists_data = await api_client.get_artists()

                if not artists_data:
                    components.empty_state('Không tìm thấy dữ liệu nghệ nhân.')
                else:
                    with ui.row().classes('grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 w-full'):
                        for i, artist in enumerate(artists_data):
                            components.artist_card(
                                artist.get('id'),
                                artist.get('name', 'Nghệ nhân'),
                                artist.get('image_url', '/static/chatbot-avatar.png'),
                                artist.get('village', 'Kinh Bắc'),
                                index=i
                            )


@ui.page('/lang-quan-ho')
async def villages_page():
    with theme.frame():
        components.page_header('Làng Quan họ', 'Khai phá không gian văn hóa tại 49 làng Quan họ gốc')

        villages = await api_client.get_locations()

        # Default map shows Bac Ninh province
        map_state = {'query': 'Bắc Ninh, Việt Nam', 'lat': None, 'lng': None}

        def get_map_src():
            lat = map_state.get('lat')
            lng = map_state.get('lng')
            if lat and lng:
                q = f'{lat},{lng}'
            else:
                q = map_state.get('query', 'Bắc Ninh')
            return f'https://www.google.com/maps?q={q}&output=embed&z=14'

        with ui.element('section').classes('pt-10 pb-4 w-full'):
            with theme.container():
                map_card = ui.card().classes('w-full overflow-hidden rounded-3xl border border-border shadow-elevated p-0')
                with map_card:
                    map_iframe = ui.html(f'<iframe src="{get_map_src()}" width="100%" height="450" style="border:0;" allowfullscreen loading="lazy"></iframe>')

        with ui.element('section').classes('pb-24 w-full'):
            with theme.container():
                if not villages:
                    components.empty_state('Dữ liệu đang được cập nhật...')
                else:
                    with ui.row().classes('grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 w-full'):
                        for v in villages:
                            def make_click(village):
                                def on_click():
                                    lat = village.get('latitude')
                                    lng = village.get('longitude')
                                    name = village.get('name', 'Làng Quan họ')
                                    addr = village.get('address', '')
                                    if lat and lng:
                                        map_state['lat'] = lat
                                        map_state['lng'] = lng
                                        map_state['query'] = f'{lat},{lng}'
                                    else:
                                        search_q = f'{name} {addr} Bắc Ninh Việt Nam'.strip()
                                        map_state['lat'] = None
                                        map_state['lng'] = None
                                        map_state['query'] = search_q
                                    map_iframe.content = f'<iframe src="{get_map_src()}" width="100%" height="450" style="border:0;" allowfullscreen loading="lazy"></iframe>'
                                return on_click

                            with ui.card().classes('group overflow-hidden rounded-2xl border border-border bg-card shadow-sm hover:shadow-lg transition-all p-0 cursor-pointer').on('click', make_click(v)):
                                ui.image(v.get('image_url', 'https://images.unsplash.com/photo-1526462981764-f6cf0f4ea260?auto=format&fit=crop&q=80&w=600')).classes('h-48 w-full object-cover group-hover:scale-105 transition-transform duration-500')
                                with ui.column().classes('p-6 gap-2'):
                                    ui.label(v.get('name', 'Làng')).classes('font-display text-xl font-bold text-primary')
                                    if v.get('address'):
                                        with ui.row().classes('items-center gap-1 text-xs text-muted-foreground'):
                                            ui.icon('place', size='14px')
                                            ui.label(v.get('address', ''))
                                    ui.label(v.get('description', 'Thông tin đang cập nhật...')).classes('text-sm text-muted-foreground line-clamp-3 leading-relaxed')
                                    ui.button('Xem trên bản đồ', icon='map').props('flat rounded').classes('text-primary font-bold mt-2')


@ui.page('/tin-tuc')
async def news_page():
    with theme.frame():
        components.page_header('Tin tức & Sự kiện', 'Cập nhật dòng chảy văn hóa Quan họ đương đại')

        state = type('state', (), {'filter': 'Tất cả'})()

        @ui.refreshable
        async def news_content():
            articles = await api_client.get_articles()
            events = await api_client.get_events()
            all_news = [{**a, 'ui_type': 'Tin tức'} for a in (articles or [])] + [{**e, 'ui_type': 'Sự kiện'} for e in (events or [])]
            filtered = [n for n in all_news if state.filter == 'Tất cả' or n['ui_type'] == state.filter]

            with ui.element('section').classes('py-20 w-full'):
                with theme.container():
                    def update_filter(val):
                        state.filter = val
                        news_content.refresh()
                    
                    components.filter_pills(['Tất cả', 'Tin tức', 'Sự kiện'], state.filter, update_filter)

                    if not filtered:
                        components.empty_state('Không có dữ liệu phù hợp.')
                    else:
                        with ui.row().classes('grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 w-full'):
                            for item in filtered:
                                components.news_card(
                                    item.get('id'),
                                    item.get('title', 'Thông báo'),
                                    item.get('image_url', 'https://images.unsplash.com/photo-1599908608021-b5d929aa054e?auto=format&fit=crop&q=80&w=400'),
                                    type=item.get('ui_type', 'Tin tức'),
                                    date=(item.get('created_at') or item.get('start_date') or '--/--/----')[:10],
                                )

        await news_content()


@ui.page('/chatbot')
def chatbot_page():
    with theme.frame():
        with ui.element('section').classes('relative min-h-[90vh] py-12 bg-background w-full'):
            with theme.container().classes('max-w-4xl'):
                # Header
                with ui.row().classes('items-center gap-4 mb-8 bg-card p-6 rounded-2xl border border-border'):
                    ui.image('/static/chatbot-avatar.png').classes('w-20 h-20 rounded-full border-4 border-white shadow-sm')
                    with ui.column().classes('gap-0'):
                        ui.label('Trợ lý Quan Họ AI').classes('font-display text-2xl font-bold text-primary')
                        ui.label('Tôi có thể giúp bạn tìm hiểu về văn hóa Quan họ Kinh Bắc').classes('text-muted-foreground text-sm')

                # Chat Area
                chat_container = ui.column().classes('w-full gap-4 transition-all overflow-y-auto mb-20 p-4 bg-muted/30 rounded-2xl min-h-[400px]')
                
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
                                
                                # Automated logic
                                response = "Xin lỗi, tôi chưa hiểu ý bạn. Bạn có thể hỏi về 'trang phục', 'làng nghề' hoặc 'unesco' được không?"
                                lowered = text.lower()
                                if 'trang phục' in lowered or 'mặc' in lowered:
                                    response = "Trang phục Quan họ rất đặc trưng: Liền chị thường mặc áo mớ ba mớ bảy, nón quai thao, khăn mỏ quạ. Liền anh mặc áo the, khăn xếp, che ô đen."
                                elif 'unesco' in lowered or 'công nhận' in lowered:
                                    response = "Dân ca Quan họ Bắc Ninh đã được UNESCO chính thức ghi danh là Di sản văn hóa phi vật thể đại diện của nhân loại vào ngày 30 tháng 9 năm 2009."
                                elif 'làng' in lowered or 'đia chỉ' in lowered:
                                    response = "Vùng Kinh Bắc có 49 làng Quan họ gốc, tiêu biểu như làng Diềm (Viêm Xá), làng Lũng Giang, làng Ngang Nội..."
                                elif 'chào' in lowered:
                                    response = "Chào bạn! Chúc bạn có một ngày tìm hiểu văn hóa thật thú vị."
                                
                                await asyncio.sleep(0.5)
                                ui.chat_message(response, name='Bot', stamp='Vừa xong', avatar='/static/chatbot-avatar.png').classes('w-full')
                                ui.scroll_to(chat_container)

                        ui.button(icon='send', on_click=send_message).props('round unelevated').classes('bg-primary text-white')
                        msg_input.on('keydown.enter', send_message)


@ui.page('/bai-hat/{id}')
async def song_detail_page(id: int):
    with theme.frame():
        song_data = await api_client.get_melody(id)
        if not song_data:
            components.empty_state('Không tìm thấy bài hát này.')
            return
            
        with ui.element('section').classes('py-16 bg-background w-full'):
            with theme.container().classes('max-w-4xl'):
                with ui.link(target='/bai-hat').classes('mb-6 inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-primary no-underline'):
                    ui.icon('arrow_back', size='16px')
                    ui.label('Quay lại Thư viện')
                    
                # Video Section
                video_url = song_data.get('video_url')
                embed_url = get_embed_url(video_url)
                fallback_img = (
                    song_data.get('image_url')
                    or 'https://images.unsplash.com/photo-1599908608021-b5d929aa054e?auto=format&fit=crop&q=80&w=800'
                )
                
                with ui.column().classes('w-full items-center mb-8'):
                    # Constrain video width for "YouTube look"
                    with ui.card().classes('overflow-hidden rounded-xl border border-border bg-card shadow-elevated p-0 w-full max-w-[850px]'):
                        # CSS Checkbox Hack: Pure CSS toggle for max reliability (Works without JS/WebSockets)
                        if embed_url:
                            final_src = embed_url + ("&autoplay=1" if "?" in embed_url else "?autoplay=1")
                            ui.html(f'''
                                <style>
                                    .vid-chk:checked ~ .vid-player {{ display: block !important; }}
                                    .vid-chk:checked ~ .vid-btn-overlay {{ display: none !important; }}
                                </style>
                                <div style="position:relative; width:100%; height:0; padding-bottom:56.25%; background:#000; border-radius:12px; overflow:hidden;">
                                    <input type="checkbox" id="vid_check_{id}" class="vid-chk" style="display:none;">
                                    
                                    <iframe class="vid-player" src="{final_src}" 
                                            style="position:absolute; inset:0; width:100%; height:100%; border:none; display:none; z-index:1;" 
                                            allow="autoplay; encrypted-media" allowfullscreen></iframe>
                                    
                                    <label for="vid_check_{id}" class="vid-btn-overlay" 
                                           style="position:absolute; inset:0; z-index:2; cursor:pointer; background:url('{fallback_img}') center center / cover no-repeat; display:grid; place-items:center;">
                                        <div style="width:100%; height:100%; display:grid; place-items:center; background:rgba(0,0,0,0.4); transition:background 0.3s;" onmouseover="this.style.background='rgba(0,0,0,0.2)'" onmouseout="this.style.background='rgba(0,0,0,0.4)'">
                                            <div style="display:flex; height:84px; width:84px; align-items:center; justify-content:center; border-radius:100px; background:#b4783c; color:white; box-shadow:0 10px 30px rgba(0,0,0,0.5); transition:transform 0.2s;" onmouseover="this.style.transform='scale(1.15)'" onmouseout="this.style.transform='scale(1)'">
                                                <svg style="width:48px; height:48px;" fill="currentColor" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
                                            </div>
                                        </div>
                                    </label>
                                </div>
                            ''').classes('w-full')
                        else:
                            with ui.element('div').classes('relative w-full aspect-video bg-black/30 flex items-center justify-center'):
                                with ui.column().classes('items-center gap-2'):
                                    ui.icon('music_note', size='64px').classes('text-white opacity-60')
                                    ui.label('Chưa có video').classes('text-white text-sm opacity-70')

                    
                    with ui.column().classes('p-6 md:p-8 w-full'):
                        with ui.row().classes('items-start justify-between gap-4 w-full'):
                            with ui.column().classes('gap-1'):
                                ui.label(song_data.get('name', 'Không tên')).classes('font-display text-3xl font-bold text-foreground')
                            
                            with ui.row().classes('gap-2'):
                                if app.storage.user.get('role') == 'admin':
                                    ui.button('Sửa bài hát', icon='edit', on_click=lambda: ui.navigate.to(f'/sua-bai-hat/{id}')).props('outline rounded-lg').classes('text-primary border-primary')
                                ui.button(icon='favorite_border').props('outline round').classes('text-muted-foreground border-border hover:border-primary hover:text-primary')
                            
                        artist_name = ''
                        if isinstance(song_data.get('artist'), dict):
                            artist_name = song_data['artist'].get('name', '')
                        artist_name = artist_name or song_data.get('artist_name', '') or 'Nghệ nhân'

                        cat_map = {'co': 'Làn điệu cổ', 'moi': 'Làn điệu mới', 'cai-bien': 'Làn điệu cải biên'}
                        category_label = cat_map.get(song_data.get('category', ''), song_data.get('category', 'Khác') or 'Làn điệu cổ')

                        with ui.row().classes('mt-3 gap-4 text-sm text-muted-foreground flex-wrap'):
                            with ui.row().classes('items-center gap-1'):
                                ui.icon('person', size='16px')
                                ui.label(artist_name)
                            with ui.row().classes('items-center gap-1'):
                                ui.icon('music_note', size='16px')
                                ui.label(category_label)
                            if song_data.get('duration'):
                                with ui.row().classes('items-center gap-1'):
                                    ui.icon('schedule', size='16px')
                                    ui.label(song_data.get('duration'))
                                
                        lyrics = song_data.get('lyrics')
                        if lyrics:
                            with ui.column().classes('mt-8 w-full'):
                                ui.label('Lời bài hát').classes('font-display text-xl font-semibold text-foreground')
                                ui.label(lyrics).classes('mt-3 whitespace-pre-line leading-relaxed text-muted-foreground italic')

                        # Comment Section
                        with ui.column().classes('mt-12 pt-12 border-t border-border w-full gap-6'):
                            ui.label('Bình luận').classes('font-display text-2xl font-bold')
                            
                            @ui.refreshable
                            async def render_comments():
                                current_comments = await api_client.get_comments(melody_id=id)
                                if not current_comments:
                                    ui.label('Chưa có bình luận nào. Hãy là người đầu tiên!').classes('text-muted-foreground italic')
                                else:
                                    for c in current_comments:
                                        with ui.row().classes('gap-4 items-start w-full'):
                                            ui.icon('account_circle', size='40px').classes('text-muted-foreground')
                                            with ui.column().classes('flex-1 gap-1'):
                                                with ui.row().classes('items-center gap-2'):
                                                    ui.label(c.get('user', {}).get('name', 'Ẩn danh')).classes('font-bold text-sm')
                                                    ui.label(c.get('created_at', '')[:10]).classes('text-[10px] text-muted-foreground')
                                                ui.label(c.get('content')).classes('text-sm text-foreground bg-muted/30 p-3 rounded-lg')

                            await render_comments()

                            # Add Comment Form
                            if app.storage.user.get('is_authenticated'):
                                with ui.row().classes('w-full items-end gap-2 bg-card p-4 rounded-xl border border-border mt-4'):
                                    comment_input = ui.textarea(placeholder='Viết bình luận của bạn...').classes('flex-1').props('outlined autogrow')
                                    async def post_comment():
                                        if not comment_input.value: return
                                        res = await api_client.create_comment(content=comment_input.value, melody_id=id)
                                        if res:
                                            comment_input.value = ''
                                            render_comments.refresh()
                                            ui.notify('Đã gửi bình luận!', type='positive')
                                        else:
                                            ui.notify('Lỗi khi gửi bình luận. Vui lòng thử lại.', type='negative')
                                    ui.button(icon='send', on_click=post_comment).props('round unelevated').classes('bg-primary text-white mb-1')
                            else:
                                with ui.row().classes('w-full justify-center p-6 bg-muted/20 rounded-xl border border-dashed border-border mt-4'):
                                    ui.label('Vui lòng').classes('text-muted-foreground')
                                    ui.link('Đăng nhập', '/dang-nhap').classes('text-primary font-bold mx-1')
                                    ui.label('để gửi bình luận.').classes('text-muted-foreground')

@ui.page('/nghe-nhan/{id}')
async def artist_detail_page(id: int):
    with theme.frame():
        artist_data = await api_client.get_artist(id)
        if not artist_data:
            components.empty_state('Không tìm thấy nghệ nhân này.')
            return
            
        with ui.element('section').classes('py-16 bg-background w-full'):
            with theme.container().classes('max-w-4xl'):
                with ui.link(target='/nghe-nhan').classes('mb-6 inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-primary no-underline'):
                    ui.icon('arrow_back', size='16px')
                    ui.label('Quay lại danh sách')
                    
                with ui.card().classes('overflow-hidden rounded-xl border border-border bg-card shadow-elevated p-8 w-full'):
                    with ui.row().classes('gap-8 items-start flex-col md:flex-row w-full'):
                        img_url = artist_data.get('image_url') or '/static/chatbot-avatar.png'
                        ui.image(img_url).classes('w-48 h-48 rounded-full border-4 border-muted object-cover shadow-sm shrink-0')
                        with ui.column().classes('flex-1 gap-2 w-full'):
                            with ui.row().classes('justify-between items-start w-full'):
                                with ui.column().classes('gap-1'):
                                    generation_map = {'truyen-thong': 'Nghệ nhân truyền thống', 'the-he-moi': 'Thế hệ mới'}
                                    gen_label = generation_map.get(artist_data.get('generation', ''), 'Nghệ nhân')
                                    village = artist_data.get('village', '')
                                    label_text = f'{gen_label} • {village}' if village else gen_label
                                    ui.label(label_text).classes('text-primary font-bold tracking-widest text-xs uppercase')
                                    ui.label(artist_data.get('name', 'Tên Nghệ Nhân')).classes('font-display text-4xl font-bold text-foreground')
                                
                                if app.storage.user.get('role') == 'admin':
                                    ui.button('Sửa thông tin', icon='edit', on_click=lambda: ui.navigate.to(f'/sua-nghe-nhan/{id}')).props('outline rounded-lg').classes('text-primary border-primary')
                            with ui.row().classes('mt-2 text-muted-foreground gap-4 text-sm flex-wrap'):
                                if artist_data.get('birth_year'):
                                    with ui.row().classes('items-center gap-1'):
                                        ui.icon('cake', size='16px')
                                        ui.label(f"Sinh năm {artist_data.get('birth_year')}")
                                if artist_data.get('village'):
                                    with ui.row().classes('items-center gap-1'):
                                        ui.icon('place', size='16px')
                                        ui.label(artist_data.get('village'))
                                if artist_data.get('performances'):
                                    with ui.row().classes('items-center gap-1'):
                                        ui.icon('queue_music', size='16px')
                                        ui.label(f"{artist_data.get('performances')} biểu diễn")
                            
                            bio = artist_data.get('biography') or artist_data.get('description') or artist_data.get('bio')
                            if bio:
                                ui.label(bio).classes('mt-4 text-foreground leading-relaxed whitespace-pre-line')
                            if artist_data.get('achievements'):
                                with ui.column().classes('mt-4 gap-2'):
                                    ui.label('Thành tích').classes('font-semibold text-sm text-primary uppercase tracking-wider')
                                    ui.label(artist_data.get('achievements')).classes('text-muted-foreground leading-relaxed whitespace-pre-line')

@ui.page('/tin-tuc/{id}')
async def news_detail_page(id: int):
    with theme.frame():
        news_data = await api_client.get_article(id)
        if not news_data:
            components.empty_state('Không tìm thấy bản tin này.')
            return
            
        with ui.element('section').classes('py-16 bg-background w-full'):
            with theme.container().classes('max-w-3xl'):
                with ui.link(target='/tin-tuc').classes('mb-6 inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-primary no-underline'):
                    ui.icon('arrow_back', size='16px')
                    ui.label('Quay lại Tin tức')
                    
                ui.label('Tin tức').classes('text-primary font-bold tracking-widest text-xs uppercase mb-2 block')
                ui.label(news_data.get('title', 'Tiêu đề tin tức')).classes('font-display text-3xl md:text-4xl font-bold text-foreground leading-tight mb-4')
                date_str = (news_data.get('created_at') or '')[:10] or '--/--/----'
                ui.label(date_str).classes('text-muted-foreground text-sm mb-8 block')
                
                if news_data.get('image_url'):
                    ui.image(news_data.get('image_url')).classes('w-full aspect-video rounded-xl object-cover shadow-sm mb-8')
                    
                ui.label(news_data.get('content', 'Nội dung đang cập nhật...')).classes('text-lg text-foreground leading-relaxed whitespace-pre-line')

                # Comment Section for News
                with ui.column().classes('mt-12 pt-12 border-t border-border w-full gap-6'):
                    ui.label('Bình luận').classes('font-display text-2xl font-bold')
                    
                    @ui.refreshable
                    async def render_news_comments():
                        current_comments = await api_client.get_comments(article_id=id)
                        if not current_comments:
                            ui.label('Chưa có bình luận nào.').classes('text-muted-foreground italic')
                        else:
                            for c in current_comments:
                                with ui.row().classes('gap-4 items-start w-full'):
                                    ui.icon('account_circle', size='40px').classes('text-muted-foreground')
                                    with ui.column().classes('flex-1 gap-1'):
                                        with ui.row().classes('items-center gap-2'):
                                            ui.label(c.get('user', {}).get('name', 'Ẩn danh')).classes('font-bold text-sm')
                                            ui.label(c.get('created_at', '')[:10]).classes('text-[10px] text-muted-foreground')
                                        ui.label(c.get('content')).classes('text-sm text-foreground bg-muted/30 p-3 rounded-lg')

                    await render_news_comments()

                    if app.storage.user.get('is_authenticated'):
                        with ui.row().classes('w-full items-end gap-2 bg-card p-4 rounded-xl border border-border mt-4'):
                            comment_input = ui.textarea(placeholder='Viết bình luận...').classes('flex-1').props('outlined autogrow')
                            async def post_comment():
                                if not comment_input.value: return
                                res = await api_client.create_comment(content=comment_input.value, article_id=id)
                                if res:
                                    comment_input.value = ''
                                    render_news_comments.refresh()
                                    ui.notify('Đã gửi bình luận!', type='positive')
                            ui.button(icon='send', on_click=post_comment).props('round unelevated').classes('bg-primary text-white mb-1')
                    else:
                        with ui.row().classes('w-full justify-center p-6 bg-muted/20 rounded-xl border border-dashed border-border mt-4'):
                            ui.link('Đăng nhập để bình luận', '/dang-nhap').classes('text-primary font-bold')

@ui.page('/dang-ky')
def register_page():
    with theme.frame():
        with ui.element('section').classes('py-24 bg-background w-full flex justify-center'):
            with ui.card().classes('w-full max-w-md p-8 rounded-2xl shadow-elevated border border-border bg-card'):
                ui.label('Tạo tài khoản').classes('font-display text-3xl font-bold text-center mb-6 text-foreground')
                with ui.column().classes('gap-4 w-full'):
                    name = ui.input('Họ và tên').classes('w-full').props('outlined')
                    email = ui.input('Email').classes('w-full').props('outlined type=email')
                    password = ui.input('Mật khẩu').classes('w-full').props('outlined type=password')
                    
                    async def handle_register():
                        if not all([name.value, email.value, password.value]):
                            ui.notify('Vui lòng điền đầy đủ thông tin', type='warning')
                            return
                        res = await api_client.register(name.value, email.value, password.value)
                        if res:
                            ui.notify('Đăng ký thành công! Đang chuyển đến trang đăng nhập...', type='positive')
                            await asyncio.sleep(1.5)
                            ui.navigate.to('/dang-nhap')
                        else:
                            ui.notify('Email đã tồn tại hoặc có lỗi xảy ra', type='negative')
                            
                    ui.button('Đăng ký', on_click=handle_register).props('unelevated rounded-lg').classes('w-full bg-primary text-white font-bold py-3 mt-2')
                    ui.link('Bạn đã có tài khoản? Đăng nhập ngay', '/dang-nhap').classes('text-sm text-center w-full text-muted-foreground hover:text-primary')

@ui.page('/dang-nhap')
def login_page():
    with theme.frame():
        with ui.element('section').classes('py-24 bg-background w-full flex justify-center'):
            with ui.card().classes('w-full max-w-md p-8 rounded-2xl shadow-elevated border border-border bg-card'):
                ui.label('Đăng nhập').classes('font-display text-3xl font-bold text-center mb-6 text-foreground')
                with ui.column().classes('gap-4 w-full'):
                    email = ui.input('Email').classes('w-full').props('outlined type=email')
                    password = ui.input('Mật khẩu').classes('w-full').props('outlined type=password')
                    
                    async def handle_login():
                        success = await api_client.login(email.value, password.value)
                        if success:
                            ui.notify('Chào mừng bạn quay trở lại!', type='positive')
                            ui.navigate.to('/')
                        else:
                            ui.notify('Email hoặc mật khẩu không chính xác', type='negative')
                            
                    ui.button('Đăng nhập', on_click=handle_login).props('unelevated rounded-lg').classes('w-full bg-primary text-white font-bold py-3 mt-2')
                    ui.link('Chưa có tài khoản? Đăng ký ngay', '/dang-ky').classes('text-sm text-center w-full text-muted-foreground hover:text-primary')

@ui.page('/su-kien/{id}')
async def event_detail_page(id: int):
    with theme.frame():
        event_data = await api_client.get_event(id)
        if not event_data:
            components.empty_state('Không tìm thấy sự kiện này.')
            return
            
        with ui.element('section').classes('py-16 bg-background w-full'):
            with theme.container().classes('max-w-3xl'):
                with ui.link(target='/tin-tuc').classes('mb-6 inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-primary no-underline'):
                    ui.icon('arrow_back', size='16px')
                    ui.label('Quay lại Sự kiện')
                    
                ui.label('Sự kiện').classes('text-accent font-bold tracking-widest text-xs uppercase mb-2 block')
                ui.label(event_data.get('title', 'Tên sự kiện')).classes('font-display text-3xl md:text-4xl font-bold text-foreground leading-tight mb-4')
                
                with ui.row().classes('gap-4 text-muted-foreground text-sm mb-8'):
                    with ui.row().classes('items-center gap-1'):
                        ui.icon('event', size='16px')
                        start = event_data.get('start_date') or ''
                        ui.label(start[:10] if start else '--/--/----')
                    with ui.row().classes('items-center gap-1'):
                        ui.icon('place', size='16px')
                        ui.label(event_data.get('location', 'Bắc Ninh'))
                
                if event_data.get('image_url'):
                    ui.image(event_data.get('image_url')).classes('w-full aspect-video rounded-xl object-cover shadow-sm mb-8')
                    
                ui.label(event_data.get('description', 'Nội dung đang cập nhật...')).classes('text-lg text-foreground leading-relaxed whitespace-pre-line')

@ui.page('/ho-so')
def profile_page():
    with theme.frame():
        with ui.element('section').classes('py-16 bg-background w-full'):
            with theme.container().classes('max-w-4xl'):
                ui.label('Hồ sơ cá nhân').classes('font-display text-3xl font-bold text-foreground mb-8')
                with ui.row().classes('gap-8 w-full flex-col md:flex-row'):
                    with ui.column().classes('w-full md:w-1/3 gap-4 shrink-0'):
                        with ui.card().classes('w-full p-6 text-center rounded-2xl shadow-sm border border-border items-center'):
                            ui.image('/static/chatbot-avatar.png').classes('w-24 h-24 rounded-full border-4 border-muted mx-auto object-cover')
                            ui.label('Người Dùng').classes('font-display text-xl font-bold mt-4')
                            ui.label('user@example.com').classes('text-muted-foreground text-sm')
                            ui.button('Đăng xuất', icon='logout').props('flat').classes('text-destructive w-full mt-4')
                    with ui.column().classes('w-full md:w-2/3'):
                        with ui.card().classes('w-full p-6 rounded-2xl shadow-sm border border-border'):
                            ui.label('Bài hát yêu thích').classes('font-display text-xl font-bold mb-4')
                            components.empty_state('Chưa có bài hát yêu thích nào.', icon='favorite_border')


@ui.page('/them-nghe-nhan')
async def add_artist_page():
    # Security check
    if app.storage.user.get('role') != 'admin':
        ui.navigate.to('/')
        return

    with theme.frame():
        with ui.element('section').classes('py-24 bg-background w-full flex justify-center'):
            with ui.card().classes('w-full max-w-2xl p-8 rounded-2xl shadow-elevated border border-border bg-card'):
                ui.label('Thêm Nghệ nhân mới').classes('font-display text-3xl font-bold text-center mb-6 text-foreground')

                with ui.column().classes('gap-4 w-full'):
                    full_name = ui.input('Họ và tên *').classes('w-full').props('outlined')
                    village_input = ui.input('Làng quê').classes('w-full').props('outlined')
                    birth_year = ui.number('Năm sinh', value=1950).classes('w-full').props('outlined')
                    image_url = ui.input('Link ảnh đại diện').classes('w-full').props('outlined')
                    generation = ui.select(
                        {'truyen-thong': 'Truyền thống', 'the-he-moi': 'Thế hệ mới'},
                        label='Thế hệ', value='truyen-thong'
                    ).classes('w-full').props('outlined')
                    bio = ui.textarea('Tiểu sử / Mô tả').classes('w-full').props('outlined')

                    async def submit():
                        if not full_name.value:
                            ui.notify('Vui lòng nhập tên nghệ nhân', type='warning')
                            return
                        payload = {
                            'name': full_name.value,
                            'village': village_input.value,
                            'birth_year': int(birth_year.value) if birth_year.value else None,
                            'image_url': image_url.value or None,
                            'generation': generation.value,
                            'biography': bio.value,
                            'description': bio.value,
                        }
                        result = await api_client.create_artist(payload)
                        if result:
                            ui.notify('Đã thêm nghệ nhân thành công!', type='positive')
                            ui.navigate.to('/nghe-nhan')
                        else:
                            ui.notify('Có lỗi xảy ra khi lưu dữ liệu', type='negative')

                    ui.button('Lưu nghệ nhân', on_click=submit).props('unelevated rounded-lg').classes('w-full bg-primary text-white font-bold py-3 mt-4')

@ui.page('/sua-nghe-nhan/{id}')
async def edit_artist_page(id: int):
    # Security check
    if app.storage.user.get('role') != 'admin':
        ui.navigate.to('/')
        return

    with theme.frame():
        artist = await api_client.get_artist(id)
        if not artist:
            components.empty_state('Không tìm thấy nghệ nhân.')
            return

        with ui.element('section').classes('py-24 bg-background w-full flex justify-center'):
            with ui.card().classes('w-full max-w-2xl p-8 rounded-2xl shadow-elevated border border-border bg-card'):
                ui.label(f'Sửa: {artist.get("name")}').classes('font-display text-3xl font-bold text-center mb-6 text-foreground')

                with ui.column().classes('gap-4 w-full'):
                    name = ui.input('Họ và tên *', value=artist.get('name')).classes('w-full').props('outlined')
                    village = ui.input('Làng quê', value=artist.get('village')).classes('w-full').props('outlined')
                    birth_year = ui.number('Năm sinh', value=artist.get('birth_year')).classes('w-full').props('outlined')
                    image_url = ui.input('Link ảnh đại diện', value=artist.get('image_url')).classes('w-full').props('outlined')
                    generation = ui.select(
                        {'truyen-thong': 'Truyền thống', 'the-he-moi': 'Thế hệ mới'},
                        label='Thế hệ', 
                        value=artist.get('generation', 'truyen-thong')
                    ).classes('w-full').props('outlined')
                    bio = ui.textarea('Tiểu sử / Mô tả', value=artist.get('biography') or artist.get('description')).classes('w-full').props('outlined')

                    async def submit():
                        if not name.value:
                            ui.notify('Vui lòng nhập tên nghệ nhân', type='warning')
                            return
                        payload = {
                            'name': name.value,
                            'village': village.value,
                            'birth_year': int(birth_year.value) if birth_year.value else None,
                            'image_url': image_url.value,
                            'generation': generation.value,
                            'biography': bio.value,
                            'description': bio.value,
                        }
                        result = await api_client.update_artist(id, payload)
                        if result:
                            ui.notify('Đã cập nhật thông tin nghệ nhân!', type='positive')
                            ui.navigate.to(f'/nghe-nhan/{id}')
                        else:
                            ui.notify('Có lỗi xảy ra khi lưu dữ liệu', type='negative')

                    ui.button('Lưu thay đổi', on_click=submit).props('unelevated rounded-lg').classes('w-full bg-primary text-white font-bold py-3 mt-4')

@ui.page('/sua-bai-hat/{id}')
async def edit_song_page(id: int):
    # Security check
    if app.storage.user.get('role') != 'admin':
        ui.navigate.to('/')
        return

    with theme.frame():
        song = await api_client.get_melody(id)
        if not song:
            components.empty_state('Không tìm thấy bài hát.')
            return

        with ui.element('section').classes('py-24 bg-background w-full flex justify-center'):
            with ui.card().classes('w-full max-w-2xl p-8 rounded-2xl shadow-elevated border border-border bg-card'):
                ui.label(f'Sửa: {song.get("name")}').classes('font-display text-3xl font-bold text-center mb-6 text-foreground')
                
                artists = await api_client.get_artists()
                artist_options = {a['id']: a['name'] for a in artists} if artists else {}

                with ui.column().classes('gap-4 w-full'):
                    name = ui.input('Tên bài hát *', value=song.get('name')).classes('w-full').props('outlined')
                    artist_sel = ui.select(artist_options, label='Chọn Nghệ nhân', value=song.get('artist_id')).classes('w-full').props('outlined')
                    
                    rev_cat_map = {'co': 'Làn điệu cổ', 'moi': 'Làn điệu mới', 'cai-bien': 'Làn điệu cải biên'}
                    category = ui.select(['Làn điệu cổ', 'Làn điệu mới', 'Làn điệu cải biên'], 
                                         label='Thể loại', 
                                         value=rev_cat_map.get(song.get('category'), 'Làn điệu cổ')).classes('w-full').props('outlined')
                    
                    duration = ui.input('Thời lượng (VD: 04:30)', value=song.get('duration')).classes('w-full').props('outlined')
                    image_url = ui.input('Link ảnh minh họa (để trống nếu muốn tự lấy từ Youtube)', value=song.get('image_url')).classes('w-full').props('outlined')
                    video_url = ui.input('Link Video Youtube', value=song.get('video_url')).classes('w-full').props('outlined')
                    lyrics = ui.textarea('Lời bài hát', value=song.get('lyrics')).classes('w-full').props('outlined')

                    async def submit():
                        if not name.value:
                            ui.notify('Vui lòng nhập tên bài hát', type='warning')
                            return
                        
                        cat_map = {'Làn điệu cổ': 'co', 'Làn điệu mới': 'moi', 'Làn điệu cải biên': 'cai-bien'}
                        
                        # Auto-extract thumbnail if image_url is missing or is already a youtube thumb
                        final_image = image_url.value
                        if video_url.value and (not final_image or 'img.youtube.com' in final_image):
                            yt_match = re.search(r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})', video_url.value)
                            if yt_match:
                                final_image = f"https://img.youtube.com/vi/{yt_match.group(1)}/hqdefault.jpg"

                        payload = {
                            'name': name.value,
                            'artist_id': artist_sel.value,
                            'category': cat_map.get(category.value, 'co'),
                            'duration': duration.value,
                            'image_url': final_image,
                            'video_url': video_url.value,
                            'lyrics': lyrics.value
                        }
                        
                        result = await api_client.update_melody(id, payload)
                        if result:
                            ui.notify('Đã cập nhật bài hát thành công!', type='positive')
                            ui.navigate.to(f'/bai-hat/{id}')
                        else:
                            ui.notify('Có lỗi xảy ra khi lưu dữ liệu', type='negative')

                    ui.button('Lưu thay đổi', on_click=submit).props('unelevated rounded-lg').classes('w-full bg-primary text-white font-bold py-3 mt-4')

@ui.page('/them-bai-hat')
async def add_song_page():
    # Security check
    if app.storage.user.get('role') != 'admin':
        ui.navigate.to('/')
        return

    with theme.frame():
        with ui.element('section').classes('py-24 bg-background w-full flex justify-center'):
            with ui.card().classes('w-full max-w-2xl p-8 rounded-2xl shadow-elevated border border-border bg-card'):
                ui.label('Thêm Bài hát Quan họ').classes('font-display text-3xl font-bold text-center mb-6 text-foreground')
                
                artists = await api_client.get_artists()
                artist_options = {a['id']: a.get('name') or a.get('full_name') for a in artists} if artists else {}

                with ui.column().classes('gap-4 w-full'):
                    name = ui.input('Tên bài hát *').classes('w-full').props('outlined')
                    artist_id = ui.select(artist_options, label='Chọn Nghệ nhân').classes('w-full').props('outlined')
                    category = ui.select(['Làn điệu cổ', 'Làn điệu mới', 'Làn điệu cải biên'], label='Thể loại').classes('w-full').props('outlined')
                    duration = ui.input('Thời lượng (VD: 04:30)').classes('w-full').props('outlined')
                    image_url = ui.input('Link ảnh minh họa').classes('w-full').props('outlined')
                    video_url = ui.input('Link Video Youtube').classes('w-full').props('outlined')
                    lyrics = ui.textarea('Lời bài hát').classes('w-full').props('outlined')

                    async def submit():
                        if not name.value:
                            ui.notify('Vui lòng nhập tên bài hát', type='warning')
                            return
                        
                        cat_map = {'Làn điệu cổ': 'co', 'Làn điệu mới': 'moi', 'Làn điệu cải biên': 'cai-bien'}
                        
                        # Auto-extract thumbnail
                        final_image = image_url.value
                        if video_url.value and not final_image:
                            yt_match = re.search(r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})', video_url.value)
                            if yt_match:
                                final_image = f"https://img.youtube.com/vi/{yt_match.group(1)}/hqdefault.jpg"

                        payload = {
                            'name': name.value,
                            'artist_id': artist_id.value,
                            'category': cat_map.get(category.value, 'co'),
                            'duration': duration.value,
                            'image_url': final_image,
                            'video_url': video_url.value,
                            'lyrics': lyrics.value
                        }
                        
                        result = await api_client.create_melody(payload)
                        if result:
                            ui.notify('Đã thêm bài hát thành công!', type='positive')
                            ui.navigate.to('/bai-hat')
                        else:
                            ui.notify('Có lỗi xảy ra khi lưu dữ liệu', type='negative')

                    ui.button('Lưu bài hát', on_click=submit).props('unelevated rounded-lg').classes('w-full bg-primary text-white font-bold py-3 mt-4')

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ in {'__main__', '__mp_main__'}:
    ui.run(title='Quan Họ Bắc Ninh - Di sản văn hóa', storage_secret='quanho_secret', port=8080)