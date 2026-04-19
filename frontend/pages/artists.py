from nicegui import app, ui
import theme
import components
from api import api_client
from translation import t, tc

@ui.page('/nghe-nhan', response_timeout=60.0)

async def artists_page():
    with theme.frame():
        components.page_header(t('home_featured_artists'), t('home_artists_subtitle'))

        # Shared state for filtering
        class ArtistState:
            def __init__(self):
                self.search_query = ''
                self.page = 1
                self.items_per_page = 8
                self.total_count = 0
                self.artists = []
        
        state = ArtistState()

        @ui.refreshable
        async def artists_content():
            state.total_count = await api_client.get_artists_count()
            skip = (state.page - 1) * state.items_per_page
            state.artists = await api_client.get_artists(skip=skip, limit=state.items_per_page)

            if not state.artists:
                components.empty_state(t('searching_artists'))
            else:
                with ui.row().classes('grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 w-full px-2'):
                    for i, artist in enumerate(state.artists):
                        components.artist_card(
                            artist.get('id'),
                            tc(artist, 'name'),
                            artist.get('image_url', '/static/common/chatbot-avatar.png'),
                            tc(artist, 'village'),
                            index=i + ((state.page - 1) * state.items_per_page)
                        )
                
                # Use generic pagination component
                components.pagination_controls(state, state.total_count, artists_content)

        with ui.element('section').classes('pt-6 pb-16 bg-background w-full'):
            with theme.container():
                # Modern Search Bar (Single Row)
                with ui.element('div').classes('modern-search-card mb-6 w-full p-2 sm:p-3 rounded-xl flex items-center gap-2 sm:gap-4'):
                    search = ui.input(
                        placeholder=t('search_songs'),
                        on_change=lambda e: (setattr(state, 'search_query', e.value or ''), setattr(state, 'page', 1), artists_content.refresh())
                    ).classes('modern-input flex-1 bg-background rounded-lg').props('outlined dense clearable debounce=500 icon=search')
                    
                    if app.storage.user.get('role') == 'admin':
                        ui.button(icon='person_add').on('click.stop', lambda: ui.navigate.to('/admin/edit/artist/0')).props('unelevated round size=md').classes('bg-primary text-white shadow-md hover:scale-110 transition-transform shrink-0 cursor-pointer pointer-events-auto z-50')

                await artists_content()

@ui.page('/nghe-nhan/{id}', response_timeout=60.0)
async def artist_detail_page(id: int):
    # Authentic Fallback Data for iconic artists
    FALLBACK_ARTISTS = {
        1: {
            'name': 'NSND Thúy Cải',
            'village': 'Tiên Du, Bắc Ninh',
            'birth_year': 1953,
            'image_url': '/static/artists/ThuyCai.png',
            'biography': 'NSND Thúy Cải sinh năm 1953 tại xã Liên Bão, Tiên Du, Bắc Ninh. Bà là "cánh chim đầu đàn" của Dân ca Quan họ Bắc Ninh thời kỳ đổi mới. Với giọng hát "vang, rền, nền, nảy" mẫu mực, bà đã dành trọn cuộc đời cho việc biểu diễn và cống hiến cho quê hương dân ca.',
            'contributions': 'Nguyên Giám đốc Đoàn dân ca Quan họ Bắc Ninh (nay là Nhà hát Dân ca Quan họ Bắc Ninh). Bà có công lớn trong việc đào tạo, dìu dắt các thế hệ nghệ sĩ trẻ và xây dựng Nhà hát Dân ca Quan họ Bắc Ninh phát triển rực rỡ.',
            'achievements': 'Danh hiệu Nghệ sĩ Nhân dân (1997). Huân chương Lao động hạng Ba. Nhiều Huy chương Vàng tại các hội diễn văn nghệ chuyên nghiệp toàn quốc.'
        },
        2: {
            'name': 'NSƯT Thanh Quý',
            'village': 'Bắc Ninh',
            'birth_year': 1958,
            'image_url': '/static/artists/ThanhQuy.png',
            'biography': 'NSƯT Thanh Quý là một trong những giọng ca "vang, rền, nền, nảy" tiêu biểu của Nhà hát Dân ca Quan họ Bắc Ninh. Bà nổi tiếng với lối hát tinh tế, giàu cảm xúc và là một trong những nghệ sĩ nòng cốt đưa dân ca Quan họ đến gần hơn với công chúng.',
            'contributions': 'Có đóng góp quan trọng trong việc truyền dạy lối hát Quan họ cổ cho thế hệ trẻ. Bà thường xuyên tham gia các chương trình biểu diễn lớn trong và ngoài nước, góp phần quảng bá hình ảnh văn hóa Kinh Bắc.',
            'achievements': 'Danh hiệu Nghệ sĩ Ưu tú. Nhiều huy chương Vàng tại các kỳ liên hoan âm nhạc dân tộc toàn quốc.'
        },
        3: {
            'name': 'NSƯT Minh Thùy',
            'village': 'Bắc Ninh',
            'year': 1960,
            'image_url': '/static/artists/MinhThuy.png',
            'biography': 'NSƯT Minh Thùy là một "liền chị" nổi danh with chất giọng mượt mà, đằm thắm. Bà cùng với các cộng sự tại Nhà hát Dân ca Quan họ Bắc Ninh đã dành nhiều tâm huyết cho việc phục dựng và bảo tồn các làn điệu Quan họ cổ lề lối.',
            'contributions': 'Chuyên gia trong việc hướng dẫn kỹ thuật hát Quan họ truyền thống. Bà đã có hàng ngàn buổi biểu diễn phục vụ nhân dân và đón tiếp các đoàn khách quốc tế, giới thiệu vẻ đẹp của di sản văn hóa phi vật thể.',
            'achievements': 'Danh hiệu Nghệ sĩ Ưu tú. Huy chương Vì sự nghiệp văn hóa thông tin.'
        },
        4: {
            'name': 'NSND Xuân Mùi',
            'village': 'Bắc Ninh',
            'birth_year': 1950,
            'image_url': '/static/artists/XuanMui.png',
            'biography': 'NSND Xuân Mùi (Nguyễn Xuân Mùi) là một nghệ sĩ, nhà nghiên cứu văn hóa sâu sắc về Quan họ. Ông không chỉ sở hữu giọng hát điêu luyện mà còn có khả năng ký âm, phân tích âm luật của các làn điệu cổ một cách khoa học.',
            'contributions': 'Nguyên Giám đốc Nhà hát Dân ca Quan họ Bắc Ninh. Ông là tác giả của nhiều công trình nghiên cứu, sách chuyên khảo về Quan họ, góp phần quan trọng trong việc chuẩn hóa việc truyền dạy di sản trong cộng đồng.',
            'achievements': 'Danh hiệu Nghệ sĩ Nhân dân. Giải thưởng xuất sắc về nghiên cứu văn hóa dân gian. Nhiều huy chương Vàng tại các kỳ hội diễn toàn quốc.'
        }
    }

    with theme.frame():
        artist_data = await api_client.get_artist(id)
        # Fallback to authentic data if needed
        if artist_data and id in FALLBACK_ARTISTS and not artist_data.get('biography'):
            artist_data.update(FALLBACK_ARTISTS[id])
        elif not artist_data:
            artist_data = FALLBACK_ARTISTS.get(id)
            
        if not artist_data:
            components.empty_state(t('searching_artists'))
            return
            
        with ui.element('section').classes('relative py-12 md:py-20 bg-background bg-paper-texture min-h-screen overflow-hidden'):
            # Cultural decoration
            ui.image('/static/common/lotus-pattern.png').classes('absolute -right-20 -top-20 w-80 opacity-5 pointer-events-none rotate-12')
            ui.image('/static/common/lotus-pattern.png').classes('absolute -left-20 bottom-20 w-64 opacity-5 pointer-events-none -rotate-12')

            with theme.container().classes('max-w-5xl relative z-10'):
                # Breadcrumbs
                with ui.row().classes('items-center gap-2 mb-8 text-xs font-black tracking-widest uppercase text-muted-foreground/60'):
                    ui.link(t('nav_home'), '/').classes('hover:text-primary transition-colors no-underline')
                    ui.label('/')
                    ui.link(t('home_featured_artists'), '/nghe-nhan').classes('hover:text-primary transition-colors no-underline')
                    ui.label('/')
                    ui.label(tc(artist_data, 'name')).classes('text-primary')

                # Main Hero Card (Glassmorphism)
                with ui.element('div').classes('relative w-full mb-12'):
                    # Decorative Silk Ribbon
                    ui.element('div').classes('absolute -left-4 top-8 h-10 w-48 bg-hero-gradient rotate-[-3deg] transform z-20 shadow-lg rounded-r-lg')

                    with ui.card().classes('w-full border border-white/40 bg-white/50 backdrop-blur-xl shadow-elevated rounded-[40px] p-8 md:p-14 overflow-hidden'):
                        with ui.row().classes('gap-12 items-center flex-col md:flex-row w-full'):
                            # Artist Avatar with High-Fidelity Frame
                            with ui.element('div').classes('relative shrink-0 group'):
                                # Outer glow/pulse
                                ui.element('div').classes('absolute inset-0 bg-primary/20 rounded-full blur-2xl group-hover:bg-primary/30 transition-all duration-700')
                                # Image container
                                with ui.element('div').classes('relative w-56 h-56 md:w-64 md:h-64 rounded-full p-2 bg-gradient-to-tr from-primary/30 via-white to-secondary/30 shadow-2xl'):
                                    ui.image(artist_data.get('image_url') or '/static/common/chatbot-avatar.png').classes('w-full h-full rounded-full object-cover border-4 border-white transform transition-transform duration-700 group-hover:scale-105')
                                # Badge
                                ui.label(t('legend_badge')).classes('absolute -bottom-2 left-1/2 -translate-x-1/2 bg-primary text-white text-[10px] font-black px-6 py-2 rounded-full shadow-xl tracking-[0.3em] z-30')
                            
                            # Content Area
                            with ui.column().classes('flex-1 gap-6 items-center md:items-start text-center md:text-left'):
                                with ui.column().classes('gap-1'):
                                    ui.label(tc(artist_data, 'name')).classes('font-display text-5xl md:text-7xl font-black text-foreground drop-shadow-sm tracking-tighter')
                                    with ui.row().classes('items-center gap-2'):
                                        ui.icon('place', color='primary', size='20px')
                                        ui.label(tc(artist_data, 'village')).classes('text-xl text-primary font-bold italic opacity-80')
                                
                                # Status Badges
                                with ui.row().classes('gap-4 mt-2'):
                                    with ui.row().classes('items-center gap-2 bg-white/60 px-5 py-2 rounded-full border border-border shadow-sm'):
                                        ui.icon('cake', size='18px', color='muted-foreground')
                                        ui.label(f"{t('birth_year')}: {artist_data.get('birth_year', '----')}").classes('text-xs font-black uppercase text-muted-foreground')
                                    
                                    gen_val = artist_data.get('generation', 'truyen-thong')
                                    gen_text = t('gen_traditional') if gen_val == 'truyen-thong' else t('gen_new')
                                    with ui.row().classes('items-center gap-2 bg-primary/10 px-5 py-2 rounded-full border border-primary/20 shadow-sm'):
                                        ui.icon('verified', size='18px', color='primary')
                                        ui.label(gen_text).classes('text-xs font-black uppercase text-primary')

                                if app.storage.user.get('role') == 'admin':
                                    ui.button(t('edit_artist'), icon='edit_note', on_click=lambda: ui.navigate.to(f'/admin/edit/artist/{id}')).props('unelevated rounded-xl color=primary').classes('mt-4 font-extrabold px-8 py-2 shadow-lg shadow-primary/30 hover:scale-105 transition-transform')

                # Detailed Content (Studio Style)
                with ui.element('div').classes('grid grid-cols-1 md:grid-cols-12 gap-8'):
                    # Sidebar / Metadata
                    with ui.column().classes('md:col-span-4 gap-6'):
                        with ui.card().classes('p-6 rounded-3xl border border-border bg-card/60 backdrop-blur-md shadow-sm'):
                            ui.label(t('contributions_title')).classes('text-sm font-black uppercase tracking-widest text-primary mb-4 border-b border-primary/10 pb-2')
                            ui.html(tc(artist_data, 'contributions') or t('contributions_updating')).classes('text-sm leading-relaxed text-muted-foreground italic')

                        with ui.card().classes('p-6 rounded-3xl border border-border bg-card/60 backdrop-blur-md shadow-sm'):
                            ui.label(t('achievements_title')).classes('text-sm font-black uppercase tracking-widest text-primary mb-4 border-b border-primary/10 pb-2')
                            ui.html(tc(artist_data, 'achievements') or t('achievements_updating')).classes('text-sm leading-relaxed text-muted-foreground')

                    # Main Biography
                    with ui.column().classes('md:col-span-8'):
                        with ui.card().classes('w-full p-8 md:p-12 rounded-[32px] border border-border bg-card shadow-sm relative overflow-hidden'):
                            # Subtle watermark
                            ui.icon('history_edu', size='12rem').classes('absolute -right-10 -bottom-10 opacity-[0.03] text-primary rotate-12')
                            
                            ui.label(t('biography_detail')).classes('text-2xl font-display font-black text-foreground mb-6 flex items-center gap-3')
                            
                            # Content text with improved readability
                            with ui.element('div').classes('prose prose-primary max-w-none'):
                                ui.html(tc(artist_data, 'biography') or t('updating')).classes('text-lg leading-[2] text-foreground/80 text-justify')
                                
                            # Signature divider
                            with ui.row().classes('w-full justify-center mt-12 opacity-20'):
                                ui.image('/static/common/lotus-pattern.png').classes('w-12 h-12')

@ui.page('/them-nghe-nhan', response_timeout=60.0)
@ui.page('/sua-nghe-nhan/{id}', response_timeout=60.0)
async def artist_form_page(id: int = None):
    if app.storage.user.get('role') != 'admin':
        ui.navigate.to('/')
        return

    is_edit = id is not None
    artist = await api_client.get_artist(id) if is_edit else {}

    with theme.frame():
        with ui.element('section').classes('py-24 bg-background w-full flex justify-center'):
            with ui.card().classes('w-full max-w-3xl p-8 rounded-3xl shadow-elevated border border-border'):
                ui.label(t('manage_artist_info') if is_edit else t('add_new_artist')).classes('font-display text-3xl font-bold text-center mb-8')

                with ui.column().classes('gap-6 w-full'):
                    with ui.column().classes('gap-2 w-full'):
                        ui.label(t('basic_info')).classes('text-xs font-black text-primary tracking-widest uppercase')
                        with ui.row().classes('grid grid-cols-1 md:grid-cols-2 gap-4 w-full'):
                            name = ui.input(t('full_name'), value=artist.get('name')).classes('w-full').props('outlined rounded-lg')
                            village = ui.input(t('hometown'), value=artist.get('village')).classes('w-full').props('outlined rounded-lg')
                            birth_year = ui.number(t('birth_year'), value=artist.get('birth_year')).classes('w-full').props('outlined rounded-lg')
                            image_url = ui.input(t('avatar_link'), value=artist.get('image_url')).classes('w-full').props('outlined rounded-lg')
                    
                    generation = ui.select({'truyen-thong': t('gen_traditional'), 'the-he-moi': t('gen_new')}, 
                                          label=t('artist_generation'), value=artist.get('generation', 'truyen-thong')).classes('w-full').props('outlined rounded-lg')
                    
                    with ui.column().classes('gap-2 w-full'):
                        ui.label(t('detail_content_tabs')).classes('text-xs font-black text-primary tracking-widest uppercase')
                        biography = ui.textarea(t('biography_detail'), value=artist.get('biography')).classes('w-full h-32').props('outlined rounded-xl')
                        contributions = ui.textarea(t('career_contributions'), value=artist.get('contributions')).classes('w-full h-32').props('outlined rounded-xl')
                        achievements = ui.textarea(t('awards_honors'), value=artist.get('achievements')).classes('w-full h-32').props('outlined rounded-xl')

                    async def submit():
                        if not name.value:
                            ui.notify(t('artist_name_required'), type='warning')
                            return
                        payload = {
                            'name': name.value, 
                            'village': village.value, 
                            'birth_year': int(birth_year.value) if birth_year.value else None,
                            'image_url': image_url.value, 
                            'generation': generation.value, 
                            'biography': biography.value,
                            'contributions': contributions.value,
                            'achievements': achievements.value,
                            'description': biography.value[:200] if biography.value else "" # Summary
                        }
                        result = await api_client.update_artist(id, payload) if is_edit else await api_client.create_artist(payload)
                        if result:
                            ui.notify(t('save_info_success'), type='positive', color='primary')
                            ui.navigate.to(f'/nghe-nhan/{id}' if is_edit else '/nghe-nhan')
                        else:
                            ui.notify(t('save_data_error'), type='negative')

                    ui.button(t('save_artist'), on_click=submit).props('unelevated rounded-xl size=lg color=primary').classes('w-full font-bold py-4 mt-6 shadow-lg shadow-primary/20')

