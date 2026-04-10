from nicegui import app, ui
import theme
import components
from api import api_client
import asyncio
import os

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
                        for song in featured_melodies:
                            components.song_card(
                                song.get('name', 'Không tiêu đề'),
                                song.get('artist', {}).get('name', 'Nghệ nhân') if isinstance(song.get('artist'), dict) else 'Nghệ nhân',
                                song.get('image_url', 'https://images.unsplash.com/photo-1599908608021-b5d929aa054e?auto=format&fit=crop&q=80&w=400'),
                                melody=song.get('category'),
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
                                artist.get('full_name', 'Nghệ nhân'),
                                artist.get('avatar_url', '/static/chatbot-avatar.png'),
                                artist.get('title', 'Kinh Bắc'),
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
                                item.get('title', 'Thông báo mới'),
                                item.get('image_url', 'https://images.unsplash.com/photo-1526462981764-f6cf0f4ea260?auto=format&fit=crop&q=80&w=400'),
                                type='Sự kiện' if 'start_date' in item else 'Tin tức',
                                date=item.get('created_at', '--/--/----')[:10],
                            )

                    with ui.row().classes('mt-12 w-full justify-center'):
                        with ui.link(target='/tin-tuc').classes('no-underline flex items-center gap-2 text-primary font-bold cursor-pointer group'):
                            ui.label('Xem thêm tin tức').classes('text-sm uppercase tracking-widest')
                            ui.icon('arrow_forward', size='20px').classes('group-hover:translate-x-1 transition-transform')


@ui.page('/gioi-thieu')
def introduction_page():
    with theme.frame():
        with ui.element('section').classes('relative min-h-[60vh] flex items-center justify-center overflow-hidden w-full'):
            ui.image('/static/hero-banner.jpg').classes('absolute inset-0 h-full w-full object-cover')
            ui.element('div').classes('absolute inset-0 bg-hero-gradient opacity-80')
            with ui.column().classes('relative z-10 text-center items-center px-4 gap-4'):
                ui.label('LỊCH SỬ VÀ GIÁ TRỊ VĂN HÓA').classes('text-xs font-bold tracking-[0.4em] text-gold-light uppercase animate-fade-in')
                with ui.column().classes('gap-0 animate-fade-in-up'):
                    ui.label('Giới thiệu').classes('font-display text-5xl md:text-7xl font-bold text-white')
                    ui.label('Quan Họ Bắc Ninh').classes('font-display text-5xl md:text-7xl font-bold text-gradient-gold')

        with ui.element('section').classes('py-24 bg-background w-full'):
            with theme.container():
                components.section_title('Quan họ là gì?')
                with ui.column().classes('max-w-4xl mx-auto text-center items-center gap-6 text-muted-foreground text-lg leading-relaxed'):
                    ui.label('Dân ca Quan họ Bắc Ninh là một hình thức hát giao duyên đối đáp giữa nam (liền anh) và nữ (liền chị), phổ biến tại vùng Kinh Bắc xưa, nay là tỉnh Bắc Ninh và Bắc Giang.')
                    ui.label('Năm 2009, Quan họ được UNESCO vinh danh là Di sản Văn hóa Phi vật thể đại diện của Nhân loại, khẳng định sức sống mãnh liệt và giá trị nhân văn sâu sắc của thể loại âm nhạc này.')

        with ui.element('section').classes('py-24 bg-card/50 border-y border-border w-full'):
            with theme.container():
                components.section_title('Bản Sắc Nghệ Thuật', 'Khám phá những nét đặc trưng làm nên linh hồn của dân ca Quan họ.')
                with ui.row().classes('grid gap-8 md:grid-cols-3 mt-8 w-full'):
                    components.intro_feature_card('music_note', 'Lề lối giao duyên', 'Lối hát đối đáp nam nữ với kỹ thuật "Vang, Rền, Nền, Nảy" điêu luyện.')
                    components.intro_feature_card('groups', 'Tục kết chạ', 'Sự gắn kết thiêng liêng giữa các làng Quan họ, tạo nên cộng đồng gắn bó bền chặt.')
                    components.intro_feature_card('favorite', 'Liền anh, Liền chị', 'Cách xưng hô đầy trân trọng, thanh lịch thể hiện nét văn hóa ứng xử Kinh Bắc.')

        with ui.element('section').classes('py-24 bg-background w-full'):
            with theme.container():
                components.section_title('Trang Phục Truyền Thống', 'Mỗi bộ trang phục là một tác phẩm nghệ thuật mang đậm dấu ấn dân gian.')
                with ui.column().classes('mt-12 gap-20 w-full'):
                    components.costume_block(
                        'Trang phục Liền chị',
                        'Nổi bật với chiếc áo mớ ba mớ bảy rực rỡ, vuông mỏ quạ đội đầu, nón quai thao và dải lụa đào thướt tha.',
                        'https://vanchuongphuongnam.vn/wp-content/uploads/2019/04/l-3.jpg',
                        items=['Áo mớ ba mớ bảy', 'Nón quai thao', 'Khăn mỏ quạ'],
                    )
                    components.costume_block(
                        'Trang phục Liền anh',
                        'Đậm chất nam nhi Kinh Bắc với áo the đen, quần lụa, khăn xếp và ô đen thanh lịch.',
                        'https://media.baodantoc.vn/baodantoc/image/files/hoangmai/2022/07/21/ao-dai-2009.jpg',
                        reverse=True,
                    )

        with ui.element('section').classes('bg-card py-24 border-t border-border w-full'):
            with theme.container().classes('max-w-5xl'):
                components.section_title('Dòng chảy lịch sử')
                with ui.column().classes('mt-16 gap-0 w-full'):
                    timeline_data = [
                        ('Thế kỷ 15',  'Quan họ bắt đầu hình thành tại vùng Kinh Bắc, gắn liền với đời sống làng xã.'),
                        ('Thế kỷ 17-18', 'Thời kỳ phát triển rực rỡ nhất với hệ thống làng Quan họ gốc được xác lập.'),
                        ('Thế kỷ 19',  'Trở thành biểu tượng văn hóa được ghi chép và nghiên cứu sâu rộng.'),
                        ('2009',       'UNESCO công nhận là Di sản Văn hóa Phi vật thể đại diện của Nhân loại.'),
                    ]
                    for i, (year, text) in enumerate(timeline_data):
                        components.timeline_item(year, text, is_last=(i == len(timeline_data) - 1))

        with ui.element('section').classes('py-24 bg-background border-t border-border w-full'):
            with theme.container().classes('max-w-3xl text-center flex flex-col items-center'):
                components.unesco_quote(
                    'Dân ca Quan họ Bắc Ninh thể hiện tính cộng đồng, sự chia sẻ, tình yêu quê hương đất nước và lòng mến khách của người dân Việt Nam.',
                    subtitle='GIÁ TRỊ DI SẢN UNESCO'
                )


@ui.page('/bai-hat')
async def songs_page():
    with theme.frame():
        components.page_header('Thư viện bài hát', 'Kho tàng các làn điệu Quan họ Kinh Bắc được sưu tầm và gìn giữ')

        with ui.element('section').classes('py-20 bg-background w-full'):
            with theme.container():
                with ui.row().classes('mb-12 w-full gap-4 items-center bg-card p-6 rounded-2xl border border-border shadow-sm'):
                    ui.input(placeholder='Tìm kiếm bài hát...').props('outlined dense borderless').classes('flex-1 bg-background rounded-lg px-4')
                    ui.select(['Tất cả', 'Làn điệu cổ', 'Làn điệu mới']).props('dense outlined').classes('w-48 bg-background')
                    ui.button(icon='filter_list').props('flat round').classes('text-muted-foreground')

                melodies = await api_client.get_melodies()

                if not melodies:
                    components.empty_state('Không tìm thấy bài hát nào.')
                else:
                    with ui.row().classes('grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 w-full'):
                        for song in melodies:
                            components.song_card(
                                song.get('name', 'Không tiêu đề'),
                                song.get('artist', {}).get('name', 'Nghệ nhân') if isinstance(song.get('artist'), dict) else 'Nghệ nhân',
                                song.get('image_url', 'https://images.unsplash.com/photo-1599908608021-b5d929aa054e?auto=format&fit=crop&q=80&w=400'),
                                melody=song.get('category'),
                                duration=song.get('duration'),
                            )


@ui.page('/nghe-nhan')
async def artists_page():
    with theme.frame():
        components.page_header('Nghệ nhân tiêu biểu', 'Những người nắm giữ hồn cốt và trao truyền di sản cho thế hệ mai sau')

        with ui.element('section').classes('py-20 bg-background w-full'):
            with theme.container():
                artists_data = await api_client.get_artists()

                if not artists_data:
                    components.empty_state('Không tìm thấy dữ liệu nghệ nhân.')
                else:
                    with ui.row().classes('grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 w-full'):
                        for i, artist in enumerate(artists_data):
                            components.artist_card(
                                artist.get('full_name', 'Nghệ nhân'),
                                artist.get('avatar_url', '/static/chatbot-avatar.png'),
                                artist.get('title', 'Kinh Bắc'),
                                index=i
                            )


@ui.page('/lang-quan-ho')
async def villages_page():
    with theme.frame():
        components.page_header('Làng Quan họ', 'Khai phá không gian văn hóa tại 49 làng Quan họ gốc')

        with ui.element('section').classes('pt-10 pb-20 w-full'):
            with theme.container():
                with ui.card().classes('w-full overflow-hidden rounded-3xl border border-border shadow-elevated p-0'):
                    ui.html('<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d59528.45524584!2d106.0371915!3d21.1712015!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x31350edae82a9313%3A0x6b49048f76662!2zQuG6r2MgTmluaC,Vmnhu4d0IE5hbQ!5e0!3m2!1svi!2s!4v1650000000000!5m2!1svi!2s" width="100%" height="450" style="border:0;" allowfullscreen="" loading="lazy"></iframe>')

        with ui.element('section').classes('pb-24 w-full'):
            with theme.container():
                villages = await api_client.get_locations()

                if not villages:
                    components.empty_state('Dữ liệu đang được cập nhật...')
                else:
                    with ui.row().classes('grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 w-full'):
                        for v in villages:
                            with ui.card().classes('group overflow-hidden rounded-2xl border border-border bg-card shadow-sm hover:shadow-lg transition-all p-0'):
                                ui.image(v.get('image_url', 'https://images.unsplash.com/photo-1526462981764-f6cf0f4ea260?auto=format&fit=crop&q=80&w=600')).classes('h-48 w-full object-cover group-hover:scale-105 transition-transform duration-500')
                                with ui.column().classes('p-6 gap-2'):
                                    ui.label(v.get('name', 'Làng')).classes('font-display text-xl font-bold text-primary')
                                    ui.label(v.get('description', 'Thông tin đang cập nhật...')).classes('text-sm text-muted-foreground line-clamp-3 leading-relaxed')
                                    ui.button('Khám phá', icon='explore').props('flat rounded').classes('text-primary font-bold mt-2')


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
                                    item.get('title', 'Thông báo'),
                                    item.get('image_url', 'https://images.unsplash.com/photo-1599908608021-b5d929aa054e?auto=format&fit=crop&q=80&w=400'),
                                    type=item.get('ui_type', 'Tin tức'),
                                    date=item.get('created_at', '--/--/----')[:10],
                                )

        await news_content()


@ui.page('/chatbot')
def chatbot_page():
    with theme.frame():
        with ui.element('section').classes('relative min-h-[80vh] flex items-center justify-center w-full bg-warm-gradient'):
            with theme.container().classes('flex flex-col items-center gap-6 text-center'):
                ui.image('/static/chatbot-avatar.png').classes('w-32 h-32 rounded-full border-8 border-white shadow-elevated mb-4')
                ui.label('ChatBot Quan Họ').classes('font-display text-4xl md:text-5xl font-black text-primary uppercase tracking-tight')
                ui.label('Trí tuệ nhân tạo đồng hành cùng bạn khám phá di sản văn hóa.').classes('text-muted-foreground text-lg max-w-xl')
                ui.label('Tính năng đang được phát triển...').classes('bg-white/50 px-6 py-2 rounded-full border border-border italic text-primary font-medium')


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ in {'__main__', '__mp_main__'}:
    ui.run(title='Quan Họ Bắc Ninh - Di sản văn hóa', storage_secret='quanho_secret', port=8080)