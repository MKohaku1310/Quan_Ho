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
        
        artists_data = await api_client.get_artists()
        # Mock fallback
        if not artists_data:
            artists_data = [
                {'id': 1, 'name': 'Nghệ nhân Nguyễn Thị Diềm', 'village': 'Làng Diềm', 'image_url': '/static/quan_ho_teaching_children_1775935150468.png'},
                {'id': 2, 'name': 'Nghệ nhân Trần Văn Lim', 'village': 'Làng Lim', 'image_url': '/static/quan_ho_festival_boat_1775935130553.png'},
                {'id': 3, 'name': 'Nghệ nhân Lê Thị Bịu', 'village': 'Làng Bịu', 'image_url': '/static/village_diem_ancient_gate_1775935115741.png'}
            ]
            
        state = ArtistState(artists_data)

        def apply_filters():
            q = state.search_query.lower()
            state.filtered_artists = [a for a in state.all_artists if q in a.get('name','').lower() or q in a.get('village','').lower()]
            artists_content.refresh()

        @ui.refreshable
        def artists_content():
            if not state.filtered_artists:
                components.empty_state('Không tìm thấy nghệ nhân phù hợp.')
            else:
                with ui.row().classes('grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 w-full px-2'):
                    for i, artist in enumerate(state.filtered_artists):
                        components.artist_card(
                            artist.get('id'),
                            artist.get('name', 'Nghệ nhân'),
                            artist.get('image_url', '/static/chatbot-avatar.png'),
                            artist.get('village', 'Kinh Bắc'),
                            index=i
                        )

        with ui.element('section').classes('py-12 md:py-20 bg-background w-full'):
            with theme.container():
                # Responsive Search Bar
                with ui.element('div').classes('mb-10 w-full bg-card p-4 sm:p-6 rounded-2xl border border-border shadow-sm flex flex-col sm:flex-row gap-4 items-center'):
                    search = ui.input(placeholder='Tìm kiếm nghệ nhân, làng quê...').classes('flex-1 w-full bg-background rounded-lg').props('outlined dense clearable icon="search"')
                    search.on('update:model-value', lambda e: (setattr(state, 'search_query', e or ''), apply_filters()))
                    
                    if app.storage.user.get('role') == 'admin':
                        ui.button('Thêm nghệ nhân', icon='person_add', on_click=lambda: ui.navigate.to('/them-nghe-nhan')).props('unelevated rounded-lg').classes('bg-primary text-white font-bold h-11 px-6 w-full sm:w-auto')

                artists_content()

@ui.page('/nghe-nhan/{id}', response_timeout=60.0)

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
                                ui.label(artist_data.get('name', 'Tên Nghệ Nhân')).classes('font-display text-4xl font-bold text-foreground')
                                if app.storage.user.get('role') == 'admin':
                                    ui.button('Sửa thông tin', icon='edit', on_click=lambda: ui.navigate.to(f'/sua-nghe-nhan/{id}')).props('outline rounded-lg').classes('text-primary border-primary')
                            
                            bio = artist_data.get('biography') or artist_data.get('description') or artist_data.get('bio')
                            if bio:
                                ui.label(bio).classes('mt-4 text-foreground leading-relaxed whitespace-pre-line')

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
            with ui.card().classes('w-full max-w-2xl p-8 rounded-2xl shadow-elevated border border-border'):
                ui.label('Sửa Nghệ nhân' if is_edit else 'Thêm Nghệ nhân mới').classes('font-display text-3xl font-bold text-center mb-6')

                with ui.column().classes('gap-4 w-full'):
                    name = ui.input('Họ và tên *', value=artist.get('name')).classes('w-full').props('outlined')
                    village = ui.input('Làng quê', value=artist.get('village')).classes('w-full').props('outlined')
                    birth_year = ui.number('Năm sinh', value=artist.get('birth_year')).classes('w-full').props('outlined')
                    image_url = ui.input('Link ảnh', value=artist.get('image_url')).classes('w-full').props('outlined')
                    generation = ui.select({'truyen-thong': 'Truyền thống', 'the-he-moi': 'Thế hệ mới'}, 
                                          label='Thế hệ', value=artist.get('generation', 'truyen-thong')).classes('w-full').props('outlined')
                    bio = ui.textarea('Tiểu sử', value=artist.get('biography') or artist.get('description')).classes('w-full').props('outlined')

                    async def submit():
                        if not name.value:
                            ui.notify('Vui lòng nhập tên', type='warning')
                            return
                        payload = {
                            'name': name.value, 'village': village.value, 'birth_year': int(birth_year.value) if birth_year.value else None,
                            'image_url': image_url.value, 'generation': generation.value, 'biography': bio.value, 'description': bio.value
                        }
                        result = await api_client.update_artist(id, payload) if is_edit else await api_client.create_artist(payload)
                        if result:
                            ui.notify('Thành công!', type='positive')
                            ui.navigate.to('/nghe-nhan')
                        else:
                            ui.notify('Có lỗi xảy ra', type='negative')

                    ui.button('Lưu nghệ nhân', on_click=submit).props('unelevated rounded-lg').classes('w-full bg-primary text-white font-bold py-3 mt-4')
