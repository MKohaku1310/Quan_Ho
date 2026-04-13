from nicegui import app, ui
import theme
import components
from api import api_client
from utils import get_embed_url
import re
import asyncio

@ui.page('/bai-hat', response_timeout=60.0)
async def songs_page():
    with theme.frame():
        components.page_header('Thư viện bài hát', 'Kho tàng các làn điệu Quan họ Kinh Bắc được sưu tầm và gìn giữ')

        class SongState:
            def __init__(self):
                self.search = ''
                self.category = 'Tất cả'
                self.page = 1
                self.items_per_page = 12
        
        state = SongState()
        
        with ui.element('section').classes('pt-6 pb-12 bg-background w-full'):
            with theme.container():
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

                    # Compact Modern Search & Filter Bar (Single Row)
                    with ui.element('div').classes('modern-search-card mb-6 w-full p-2 sm:p-3 rounded-xl flex items-center gap-2 sm:gap-4'):
                        # Search Part
                        search_input = ui.input(placeholder='Tìm kiếm bài hát...').props('outlined dense clearable debounce=500 icon=search').classes('modern-input flex-1 bg-background rounded-lg')
                        search_input.on('update:model-value', lambda e: (setattr(state, 'search', e or ''), setattr(state, 'page', 1), songs_content.refresh()))
                        
                        # Filter Part (Compact)
                        cat_select = ui.select(['Tất cả', 'Làn điệu cổ', 'Làn điệu mới', 'Làn điệu cải biên'], value=state.category).props('dense outlined rounded-lg options-dense').classes('modern-select w-32 sm:w-48 bg-background')
                        cat_select.on('update:model-value', lambda e: (setattr(state, 'category', e or 'Tất cả'), setattr(state, 'page', 1), songs_content.refresh()))
                        
                        if app.storage.user.get('role') == 'admin':
                            ui.button(icon='add', on_click=lambda: ui.navigate.to('/admin/edit/song/0')).props('unelevated round size=md').classes('bg-primary text-white shadow-md hover:scale-110 transition-transform shrink-0')

                    if not melodies:
                        components.empty_state('Không tìm thấy bài hát nào.')
                    else:
                        start = (state.page - 1) * state.items_per_page
                        end = start + state.items_per_page
                        page_items = melodies[start:end]
                        
                        with ui.row().classes('grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 md:gap-8 w-full px-2'):
                            cat_map_label = {'co': 'Làn điệu cổ', 'moi': 'Làn điệu mới', 'cai-bien': 'Làn điệu cải biên'}
                            for song in page_items:
                                components.song_card(
                                    song.get('id'),
                                    song.get('name', 'Không tiêu đề'),
                                    song.get('artist', {}).get('name', 'Nghệ nhân') if isinstance(song.get('artist'), dict) else 'Nghệ nhân',
                                    song.get('image_url') or 'https://images.unsplash.com/photo-1599908608021-b5d929aa054e?auto=format&fit=crop&q=80&w=400',
                                    melody=cat_map_label.get(song.get('category'), 'Làn điệu cổ'),
                                    duration=song.get('duration'),
                                )
                        
                        # Pagination UI
                        total_pages = (len(melodies) + state.items_per_page - 1) // state.items_per_page
                        if total_pages > 1:
                            with ui.row().classes('w-full justify-center mt-12 gap-2'):
                                ui.button(icon='chevron_left', on_click=lambda: (setattr(state, 'page', max(1, state.page-1)), songs_content.refresh())).props('flat round dense').classes('text-primary')
                                for p in range(1, total_pages + 1):
                                    ui.button(str(p), on_click=lambda p=p: (setattr(state, 'page', p), songs_content.refresh())).props(f'flat round dense {"color=primary shadow-md bg-primary/10" if p == state.page else "color=grey"}').classes('font-bold text-sm')
                                ui.button(icon='chevron_right', on_click=lambda: (setattr(state, 'page', min(total_pages, state.page+1)), songs_content.refresh())).props('flat round dense').classes('text-primary')
                
                await songs_content()

@ui.page('/bai-hat/{id}', response_timeout=60.0)

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
                    
                embed_url = get_embed_url(song_data.get('video_url'))
                fallback_img = (song_data.get('image_url') or 'https://images.unsplash.com/photo-1599908608021-b5d929aa054e?auto=format&fit=crop&q=80&w=800')
                
                with ui.column().classes('w-full items-center mb-8'):
                    with ui.card().classes('overflow-hidden rounded-xl border border-border bg-card shadow-elevated p-0 w-full max-w-[850px]'):
                        video_url_raw = song_data.get('video_url', '')
                        if video_url_raw:
                            # Show thumbnail with Play button that opens YouTube in new tab
                            with ui.element('div').classes('relative w-full aspect-video cursor-pointer group').on(
                                'click', lambda: ui.run_javascript(f'window.open("{video_url_raw}", "_blank")')
                            ):
                                ui.image(fallback_img).classes(
                                    'w-full h-full object-cover transition-transform duration-700 group-hover:scale-105'
                                )
                                # Dark overlay
                                with ui.element('div').classes(
                                    'absolute inset-0 flex flex-col items-center justify-center gap-4 '
                                    'bg-black/40 group-hover:bg-black/30 transition-colors'
                                ):
                                    # Play button
                                    with ui.element('div').classes(
                                        'flex h-20 w-20 items-center justify-center rounded-full '
                                        'bg-[#b4783c] text-white shadow-[0_10px_30px_rgba(0,0,0,0.5)] '
                                        'transition-transform group-hover:scale-110'
                                    ):
                                        ui.icon('play_arrow', size='48px')
                                    ui.label('Nhấn để xem trên YouTube').classes(
                                        'text-white/80 text-sm font-medium tracking-wide'
                                    )
                        else:
                            with ui.element('div').classes('w-full aspect-video bg-black/30 flex items-center justify-center'):
                                ui.icon('music_note', size='64px').classes('text-white opacity-60')

                    with ui.column().classes('p-6 md:p-8 w-full'):
                        with ui.row().classes('items-start justify-between gap-4 w-full'):
                            ui.label(song_data.get('name', 'Không tên')).classes('font-display text-3xl font-bold text-foreground')
                            if app.storage.user.get('role') == 'admin':
                                ui.button('Sửa bài hát', icon='edit', on_click=lambda: ui.navigate.to(f'/sua-bai-hat/{id}')).props('outline rounded-lg').classes('text-primary border-primary')
                            
                        artist_name = (song_data.get('artist', {}).get('name') if isinstance(song_data.get('artist'), dict) else (song_data.get('artist_name') or 'Nghệ nhân'))
                        category_label = {'co': 'Làn điệu cổ', 'moi': 'Làn điệu mới', 'cai-bien': 'Làn điệu cải biên'}.get(song_data.get('category'), 'Làn điệu cổ')

                        with ui.row().classes('mt-3 gap-4 text-sm text-muted-foreground'):
                            ui.label(f"Nghệ nhân: {artist_name}")
                            ui.label(f"Thể loại: {category_label}")
                            if song_data.get('duration'):
                                ui.label(f"Thời lượng: {song_data.get('duration')}")
                                
                        if song_data.get('lyrics'):
                            with ui.column().classes('mt-8 w-full'):
                                ui.label('Lời bài hát').classes('font-display text-xl font-semibold')
                                ui.label(song_data.get('lyrics')).classes('mt-3 whitespace-pre-line leading-relaxed text-muted-foreground italic')

                        # Comment Section
                        with ui.column().classes('mt-12 pt-12 border-t border-border w-full gap-6'):
                            ui.label('Bình luận').classes('font-display text-2xl font-bold')
                            
                            @ui.refreshable
                            async def render_comments():
                                current_comments = await api_client.get_comments(melody_id=id)
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

                            await render_comments()

                            if app.storage.user.get('is_authenticated'):
                                with ui.element('div').classes('w-full mt-10 p-0 sm:p-2'):
                                    with ui.row().classes('w-full items-start gap-3 sm:gap-4 no-wrap'):
                                        # User Avatar
                                        user_name = app.storage.user.get('user_name', 'U')
                                        ui.avatar(icon='account_circle', color='primary', text_color='white').classes('shadow-sm hover:scale-110 transition-transform cursor-pointer shrink-0')
                                        
                                        # Modern Input Card
                                        with ui.card().classes('flex-1 p-0 bg-white/40 backdrop-blur-md border border-border/50 rounded-2xl shadow-sm hover:shadow-md transition-all group'):
                                            with ui.column().classes('w-full p-3 sm:p-4 gap-2'):
                                                comment_input = ui.textarea(placeholder='Bạn đang nghĩ gì về làn điệu này?').classes('flex-1 w-full bg-transparent border-none text-base').props('borderless autogrow counter maxLength=500 dense')
                                                
                                                with ui.row().classes('w-full justify-end items-center mt-1'):
                                                    async def post_comment(e=None):
                                                        if not comment_input.value.strip():
                                                            ui.notify('Vui lòng nhập nội dung bình luận', type='warning')
                                                            return
                                                        res = await api_client.create_comment(content=comment_input.value, melody_id=id)
                                                        if res:
                                                            comment_input.value = ''
                                                            ui.notify('Bình luận của bạn đã được gửi! Đang cập nhật...', icon='check_circle', color='positive')
                                                            await asyncio.sleep(1.0)
                                                            ui.navigate.reload()
                                                        else:
                                                            ui.notify('Gửi bình luận thất bại', icon='error', color='negative')
                                                    
                                                    ui.button('GỬI', icon='send', on_click=post_comment).props('unelevated rounded-lg').classes('bg-primary text-white font-bold px-6 py-2 shadow-sm hover:scale-105 transition-all')
                            else:
                                with ui.card().classes('w-full p-8 border border-dashed border-border flex flex-col items-center gap-4 bg-muted/20 opacity-80 mt-8'):
                                    ui.icon('login', size='32px', color='muted')
                                    ui.label('Vui lòng đăng nhập để gửi bình luận hâm mộ các nghệ sĩ.').classes('text-muted-foreground italic text-center')
                                    ui.button(t('login'), on_click=lambda: ui.navigate.to('/dang-nhap')).props('unelevated rounded-lg color=primary').classes('px-8 font-bold')

@ui.page('/them-bai-hat', response_timeout=60.0)
@ui.page('/sua-bai-hat/{id}', response_timeout=60.0)

async def song_form_page(id: int = None):
    if app.storage.user.get('role') != 'admin':
        ui.navigate.to('/')
        return

    is_edit = id is not None
    song = await api_client.get_melody(id) if is_edit else {}
    
    with theme.frame():
        with ui.element('section').classes('py-24 bg-background w-full flex justify-center'):
            with ui.card().classes('w-full max-w-2xl p-8 rounded-2xl shadow-elevated border border-border'):
                ui.label('Sửa Bài hát' if is_edit else 'Thêm Bài hát Quan họ').classes('font-display text-3xl font-bold text-center mb-6')
                
                artists = await api_client.get_artists()
                artist_options = {a['id']: a.get('name') for a in artists} if artists else {}

                with ui.column().classes('gap-4 w-full'):
                    name = ui.input('Tên bài hát *', value=song.get('name')).classes('w-full').props('outlined')
                    artist_id = ui.select(artist_options, label='Chọn Nghệ nhân', value=song.get('artist_id')).classes('w-full').props('outlined')
                    
                    rev_cat_map = {'co': 'Làn điệu cổ', 'moi': 'Làn điệu mới', 'cai-bien': 'Làn điệu cải biên'}
                    category = ui.select(['Làn điệu cổ', 'Làn điệu mới', 'Làn điệu cải biên'], 
                                         label='Thể loại', value=rev_cat_map.get(song.get('category'), 'Làn điệu cổ')).classes('w-full').props('outlined')
                    
                    duration = ui.input('Thời lượng', value=song.get('duration')).classes('w-full').props('outlined')
                    image_url = ui.input('Link ảnh', value=song.get('image_url')).classes('w-full').props('outlined')
                    video_url = ui.input('Link Video Youtube', value=song.get('video_url')).classes('w-full').props('outlined')
                    lyrics = ui.textarea('Lời bài hát', value=song.get('lyrics')).classes('w-full').props('outlined')

                    async def submit():
                        if not name.value:
                            ui.notify('Vui lòng nhập tên bài hát', type='warning')
                            return
                        
                        cat_map = {'Làn điệu cổ': 'co', 'Làn điệu mới': 'moi', 'Làn điệu cải biên': 'cai-bien'}
                        
                        final_image = image_url.value
                        if video_url.value and not final_image:
                            yt_match = re.search(r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})', video_url.value)
                            if yt_match: final_image = f"https://img.youtube.com/vi/{yt_match.group(1)}/hqdefault.jpg"

                        payload = {
                            'name': name.value, 'artist_id': artist_id.value, 'category': cat_map.get(category.value, 'co'),
                            'duration': duration.value, 'image_url': final_image, 'video_url': video_url.value, 'lyrics': lyrics.value
                        }
                        
                        result = await api_client.update_melody(id, payload) if is_edit else await api_client.create_melody(payload)
                        if result:
                            ui.notify('Thành công!', type='positive')
                            ui.navigate.to('/bai-hat')
                        else:
                            ui.notify('Có lỗi xảy ra', type='negative')

                    ui.button('Lưu bài hát', on_click=submit).props('unelevated rounded-lg').classes('w-full bg-primary text-white font-bold py-3 mt-4')
