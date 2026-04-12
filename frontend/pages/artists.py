from nicegui import app, ui
import theme
import components
from api import api_client

@ui.page('/nghe-nhan', response_timeout=60.0)

async def artists_page():
    with theme.frame():
        components.page_header('Nghệ nhân tiêu biểu', 'Những người nắm giữ hồn cốt và trao truyền di sản cho thế hệ mai sau')

        # Shared state for filtering
        class ArtistState:
            def __init__(self, artists):
                self.all_artists = artists
                self.filtered_artists = artists
                self.search_query = ''
                self.page = 1
                self.items_per_page = 8
        
        artists_data = await api_client.get_artists()
        
        state = ArtistState(artists_data)

        def apply_filters():
            q = state.search_query.lower()
            state.filtered_artists = [a for a in state.all_artists if q in a.get('name','').lower() or q in a.get('village','').lower()]
            state.page = 1
            artists_content.refresh()

        @ui.refreshable
        def artists_content():
            if not state.filtered_artists:
                components.empty_state('Không tìm thấy nghệ nhân phù hợp.')
            else:
                start = (state.page - 1) * state.items_per_page
                end = start + state.items_per_page
                page_items = state.filtered_artists[start:end]
                
                with ui.row().classes('grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 w-full px-2'):
                    for i, artist in enumerate(page_items):
                        components.artist_card(
                            artist.get('id'),
                            artist.get('name', 'Nghệ nhân'),
                            artist.get('image_url', '/static/common/chatbot-avatar.png'),
                            artist.get('village', 'Kinh Bắc'),
                            index=i + start
                        )
                
                # Pagination UI
                total_pages = (len(state.filtered_artists) + state.items_per_page - 1) // state.items_per_page
                if total_pages > 1:
                    with ui.row().classes('w-full justify-center mt-12 gap-2'):
                        ui.button(icon='chevron_left', on_click=lambda: (setattr(state, 'page', max(1, state.page-1)), artists_content.refresh())).props('flat round dense').classes('text-primary')
                        for p in range(1, total_pages + 1):
                            ui.button(str(p), on_click=lambda p=p: (setattr(state, 'page', p), artists_content.refresh())).props(f'flat round dense {"color=primary shadow-md bg-primary/10" if p == state.page else "color=grey"}').classes('font-bold text-sm')
                        ui.button(icon='chevron_right', on_click=lambda: (setattr(state, 'page', min(total_pages, state.page+1)), artists_content.refresh())).props('flat round dense').classes('text-primary')

        with ui.element('section').classes('pt-6 pb-16 bg-background w-full'):
            with theme.container():
                # Modern Search Bar (Single Row)
                with ui.element('div').classes('modern-search-card mb-6 w-full p-2 sm:p-3 rounded-xl flex items-center gap-2 sm:gap-4'):
                    search = ui.input(placeholder='Tìm kiếm nghệ nhân, làng quê...').classes('modern-input flex-1 bg-background rounded-lg').props('outlined dense clearable debounce=500 icon=search')
                    search.on('update:model-value', lambda e: (setattr(state, 'search_query', e or ''), apply_filters()))
                    
                    if app.storage.user.get('role') == 'admin':
                        ui.button(icon='person_add', on_click=lambda: ui.navigate.to('/admin/edit/artist/0')).props('unelevated round size=md').classes('bg-primary text-white shadow-md hover:scale-110 transition-transform shrink-0')

                artists_content()

@ui.page('/nghe-nhan/{id}', response_timeout=60.0)
async def artist_detail_page(id: int):
    # Authentic Fallback Data for iconic artists
    FALLBACK_ARTISTS = {
        1: {
            'name': 'NSND Thúy Cải',
            'village': 'Tiên Du, Bắc Ninh',
            'birth_year': 1953,
            'image_url': 'https://vov.gov.vn/Uploads/Images/2021/01/21/nsnd-thuy-cai.jpg',
            'biography': 'NSND Thúy Cải sinh năm 1953 tại xã Liên Bão, Tiên Du, Bắc Ninh. Bà là "cánh chim đầu đàn" của Dân ca Quan họ Bắc Ninh thời kỳ đổi mới. Với giọng hát "vang, rền, nền, nảy" mẫu mực, bà đã dành trọn cuộc đời cho việc biểu diễn và cống hiến cho quê hương dân ca.',
            'contributions': 'Nguyên Giám đốc Đoàn dân ca Quan họ Bắc Ninh. Bà có công lớn trong việc đào tạo, dìu dắt các thế hệ nghệ sĩ trẻ và xây dựng Nhà hát Dân ca Quan họ Bắc Ninh phát triển rực rỡ như ngày nay.',
            'achievements': 'Danh hiệu Nghệ sĩ Nhân dân (1997). Huân chương Lao động hạng Ba. Nhiều Huy chương Vàng tại các hội diễn văn nghệ chuyên nghiệp toàn quốc.'
        },
        2: {
            'name': 'NSND Quý Tráng',
            'village': 'Làng Diềm, Bắc Ninh',
            'birth_year': 1955,
            'image_url': 'https://vnn-imgs-f.vgcloud.vn/2019/08/29/18/nsnd-quy-trang.jpg',
            'biography': 'NSND Quý Tráng sinh ra tại làng Diềm - cái nôi của Quan họ cổ. Ông sở hữu giọng hát nam trầm ấm, hào sảng nhưng cũng đầy trữ tình, biểu tượng cho phong thái lịch lãm của các "liền anh" Kinh Bắc.',
            'contributions': 'Nguyên Giám đốc Nhà hát Dân ca Quan họ Bắc Ninh. Ông là người có công đầu trong việc tổ chức các tour diễn quốc tế, đưa Quan họ vươn tầm thế giới và được UNESCO công nhận là di sản văn hóa phi vật thể đại diện của nhân loại.',
            'achievements': 'Danh hiệu Nghệ sĩ Nhân dân (2012). Giải thưởng Nhà nước về Văn học Nghệ thuật. Nhiều bằng khen cao quý từ Bộ Văn hóa, Thể thao và Du lịch.'
        },
        3: {
            'name': 'NSND Tự Lẫm',
            'village': 'Bắc Ninh',
            'birth_year': 1940,
            'image_url': 'https://static.vov-production.vov.vn/w850/sites/default/files/styles/video_poster_default/public/2021-04/tu_lam_1.jpg',
            'biography': 'NSND Tự Lẫm là một trong những nghệ sĩ gạo cội nhất, người giữ lửa cho lối hát Quan họ cổ lề lối. Ông nổi tiếng không chỉ qua giọng hát mà còn qua vai chính trong bộ phim kinh điển "Đến hẹn lại lên" (vai anh lái xe kiêm liền anh Quan họ).',
            'contributions': 'Cống hiến cả cuộc đời cho việc điền dã, sưu tầm các làn điệu cổ có nguy cơ mai một. Ông là "pho từ điển sống" về văn hóa chơi Quan họ và các nghi thức kết chạ cổ xưa.',
            'achievements': 'Danh hiệu Nghệ sĩ Nhân dân. Giải thưởng tại các liên hoan điện ảnh quốc tế. Huy chương Vì sự nghiệp Văn hóa.'
        },
        4: {
            'name': 'NSƯT Xuân Mùi',
            'village': 'Bắc Ninh',
            'birth_year': 1950,
            'image_url': 'https://vov.gov.vn/Uploads/Images/2021/04/01/nsut-xuan-mui.jpg',
            'biography': 'NSƯT Xuân Mùi là một nghệ sĩ kiêm nhà nghiên cứu văn hóa sâu sắc. Ông không chỉ sở hữu kỹ thuật hát điêu luyện mà còn có khả năng ký âm, phân tích âm luật của các làn điệu cổ một cách khoa học.',
            'contributions': 'Nguyên Phó Giám đốc Đoàn Dân ca Quan họ Bắc Ninh. Ông là tác giả của nhiều công trình nghiên cứu, sách chuyên khảo về Quan họ, góp phần quan trọng trong việc chuẩn hóa việc truyền dạy di sản trong trường học.',
            'achievements': 'Danh hiệu Nghệ sĩ Ưu tú. Nhiều huy chương Vàng, Bạc tại các hội diễn ca múa nhạc toàn quốc. Giải thưởng xuất sắc về nghiên cứu văn hóa dân gian.'
        }
    }

    with theme.frame():
        artist_data = await api_client.get_artist(id)
        # Fallback to authentic data for the first 4 IDs if backend has no bio
        if artist_data and id in FALLBACK_ARTISTS and not artist_data.get('biography'):
            artist_data.update(FALLBACK_ARTISTS[id])
        elif not artist_data:
            artist_data = FALLBACK_ARTISTS.get(id)
            
        if not artist_data:
            components.empty_state('Không tìm thấy nghệ nhân này.')
            return
            
        with ui.element('section').classes('py-24 bg-background min-h-screen'):
            with theme.container().classes('max-w-5xl'):
                # Back link
                with ui.link(target='/nghe-nhan').classes('mb-10 inline-flex items-center gap-2 text-sm font-bold text-primary no-underline hover:opacity-70 transition-opacity'):
                    ui.icon('arrow_back', size='18px')
                    ui.label('QUAY LẠI DANH SÁCH')

                # Header Profile Card
                with ui.card().classes('w-full border border-border bg-card shadow-elevated rounded-3xl p-6 md:p-10 mb-8 overflow-hidden'):
                    with ui.row().classes('gap-10 items-center md:items-start flex-col md:flex-row w-full'):
                        # Avatar with frame
                        with ui.element('div').classes('relative shrink-0'):
                            ui.image(artist_data.get('image_url') or '/static/common/chatbot-avatar.png').classes('w-48 h-48 md:w-56 md:h-56 rounded-full border-4 border-muted object-cover shadow-lg')
                            ui.label('LEGEND').classes('absolute -bottom-2 left-1/2 -translate-x-1/2 bg-primary text-white text-[10px] font-black px-4 py-1 rounded-full shadow-md tracking-[0.2em]')
                        
                        # Basic Info
                        with ui.column().classes('flex-1 gap-4 items-center md:items-start text-center md:text-left'):
                            with ui.column().classes('gap-1'):
                                ui.label(artist_data.get('name', 'Nghệ nhân')).classes('font-display text-4xl md:text-5xl font-black text-foreground')
                                ui.label(f"Làng quê: {artist_data.get('village', 'Kinh Bắc')}").classes('text-lg text-primary font-medium italic')
                                
                            with ui.row().classes('gap-4 mt-2'):
                                with ui.row().classes('items-center gap-1.5 bg-muted px-4 py-1.5 rounded-full border border-border'):
                                    ui.icon('cake', size='16px').classes('text-muted-foreground')
                                    ui.label(f"Sinh năm: {artist_data.get('birth_year', '----')}").classes('text-xs font-bold text-muted-foreground')
                                with ui.row().classes('items-center gap-1.5 bg-primary/5 px-4 py-1.5 rounded-full border border-primary/20'):
                                    ui.icon('verified', size='16px').classes('text-primary')
                                    gen = 'Truyền thống' if artist_data.get('generation') == 'truyen-thong' else 'Thế hệ mới'
                                    ui.label(gen).classes('text-xs font-bold text-primary')

                            if app.storage.user.get('role') == 'admin':
                                ui.button('Sửa nghệ nhân', icon='edit_note', on_click=lambda: ui.navigate.to(f'/sua-nghe-nhan/{id}')).props('unelevated rounded-lg color=primary').classes('mt-4 font-bold px-6 shadow-md shadow-primary/20')

                # Content Tabs
                with ui.tabs().classes('w-full border-b border-border mb-8 shadow-sm rounded-t-xl bg-card') as tabs:
                    bio_tab = ui.tab('TIỂU SỬ', icon='history_edu').classes('px-8 font-bold text-xs tracking-widest')
                    cont_tab = ui.tab('CỐNG HIẾN', icon='stars').classes('px-8 font-bold text-xs tracking-widest')
                    ach_tab = ui.tab('GIẢI THƯỞNG', icon='workspace_premium').classes('px-8 font-bold text-xs tracking-widest')

                with ui.tab_panels(tabs, value=bio_tab).classes('w-full bg-transparent overflow-visible') as panels:
                    with ui.tab_panel(bio_tab).classes('p-0'):
                        ui.label(artist_data.get('biography') or 'Đang cập nhật tiểu sử...').classes('text-lg leading-loose text-foreground/80 whitespace-pre-line text-justify p-4 md:p-8 bg-card rounded-2xl border border-border')

                    with ui.tab_panel(cont_tab).classes('p-0'):
                        with ui.column().classes('gap-6 p-4 md:p-8 bg-card rounded-2xl border border-border'):
                            ui.label('Những đóng góp lớn cho di sản').classes('text-2xl font-display font-bold text-primary mb-2')
                            ui.label(artist_data.get('contributions', artist_data.get('description')) or 'Đang cập nhật thông tin cống hiến...').classes('text-lg leading-relaxed text-foreground/80 whitespace-pre-line')

                    with ui.tab_panel(ach_tab).classes('p-0'):
                        with ui.column().classes('gap-6 p-4 md:p-8 bg-card rounded-2xl border border-border'):
                            ui.label('Danh hiệu và giải thưởng cao quý').classes('text-2xl font-display font-bold text-primary mb-2')
                            ui.label(artist_data.get('achievements') or 'Đang cập nhật giải thưởng...').classes('text-lg leading-relaxed text-foreground/80 whitespace-pre-line')

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
                ui.label('Quản lý thông tin Nghệ nhân' if is_edit else 'Thêm Nghệ nhân mới').classes('font-display text-3xl font-bold text-center mb-8')

                with ui.column().classes('gap-6 w-full'):
                    with ui.column().classes('gap-2 w-full'):
                        ui.label('Thông tin cơ bản').classes('text-xs font-black text-primary tracking-widest uppercase')
                        with ui.row().classes('grid grid-cols-1 md:grid-cols-2 gap-4 w-full'):
                            name = ui.input('Họ và tên *', value=artist.get('name')).classes('w-full').props('outlined rounded-lg')
                            village = ui.input('Làng quê', value=artist.get('village')).classes('w-full').props('outlined rounded-lg')
                            birth_year = ui.number('Năm sinh', value=artist.get('birth_year')).classes('w-full').props('outlined rounded-lg')
                            image_url = ui.input('Link ảnh đại diện', value=artist.get('image_url')).classes('w-full').props('outlined rounded-lg')
                    
                    generation = ui.select({'truyen-thong': 'Truyền thống', 'the-he-moi': 'Thế hệ mới'}, 
                                          label='Thế hệ nghệ nhân', value=artist.get('generation', 'truyen-thong')).classes('w-full').props('outlined rounded-lg')
                    
                    with ui.column().classes('gap-2 w-full'):
                        ui.label('Nội dung chi tiết (Sẽ hiển thị trong các Tab)').classes('text-xs font-black text-primary tracking-widest uppercase')
                        biography = ui.textarea('Tiểu sử chi tiết', value=artist.get('biography')).classes('w-full h-32').props('outlined rounded-xl')
                        contributions = ui.textarea('Cống hiến & Sự nghiệp', value=artist.get('contributions')).classes('w-full h-32').props('outlined rounded-xl')
                        achievements = ui.textarea('Giải thưởng & Danh hiệu', value=artist.get('achievements')).classes('w-full h-32').props('outlined rounded-xl')

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
                            'biography': biography.value,
                            'contributions': contributions.value,
                            'achievements': achievements.value,
                            'description': biography.value[:200] if biography.value else "" # Summary
                        }
                        result = await api_client.update_artist(id, payload) if is_edit else await api_client.create_artist(payload)
                        if result:
                            ui.notify('Lưu thông tin thành công!', type='positive', color='primary')
                            ui.navigate.to(f'/nghe-nhan/{id}' if is_edit else '/nghe-nhan')
                        else:
                            ui.notify('Có lỗi xảy ra khi lưu dữ liệu', type='negative')

                    ui.button('Lưu nghệ nhân', on_click=submit).props('unelevated rounded-xl size=lg color=primary').classes('w-full font-bold py-4 mt-6 shadow-lg shadow-primary/20')

