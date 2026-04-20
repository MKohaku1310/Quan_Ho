from nicegui import app, ui
import theme
import components
from api import api_client
from utils import get_embed_url
from translation import t, tc
import re
import asyncio

@ui.page('/bai-hat', response_timeout=60.0)
async def songs_page():
    with theme.frame():
        components.page_header(t('songs_library_title'), t('songs_library_subtitle'))

        if app.storage.user.get('is_authenticated'):
            favorites = await api_client.get_favorites()
            app.storage.user['favorite_ids'] = [f.get('melody_id') for f in favorites if f.get('melody_id') is not None]
        else:
            app.storage.user['favorite_ids'] = []

        class SongState:
            def __init__(self):
                self.search = ''
                self.category = t('all_categories')
                self.page = 1
                self.items_per_page = 12
                self.total_count = 0
        
        state = SongState()
        
        with ui.element('section').classes('pt-6 pb-12 bg-background w-full'):
            with theme.container():
                @ui.refreshable
                async def songs_content():
                    skip = (state.page - 1) * state.items_per_page
                    limit = state.items_per_page
                    
                    # Determine category for API filter
                    cat_map = {t('cat_co'): 'co', t('cat_moi'): 'moi', t('cat_cai_bien'): 'cai-bien'}
                    target_cat = cat_map.get(state.category)

                    if state.search:
                        # Search API does not support pagination/filtering on backend yet
                        results = await api_client.search_melodies(state.search)
                        if target_cat:
                            results = [m for m in results if m.get('category') == target_cat]
                        
                        state.total_count = len(results)
                        melodies = results[skip : skip + limit]
                    else:
                        state.total_count = await api_client.get_melodies_count(category=target_cat)
                        melodies = await api_client.get_melodies(skip=skip, limit=limit, category=target_cat)

                    # Compact Modern Search & Filter Bar (Single Row)
                    with ui.element('div').classes('modern-search-card mb-6 w-full p-2 sm:p-3 rounded-xl flex items-center gap-2 sm:gap-4'):
                        # Search Part
                        search_input = ui.input(
                            placeholder=t('search_songs'),
                            on_change=lambda e: (setattr(state, 'search', e.value or ''), setattr(state, 'page', 1), songs_content.refresh())
                        ).props('outlined dense clearable debounce=500 icon=search').classes('modern-input flex-1 bg-background rounded-lg')
                        
                        # Filter Part (Compact)
                        cats = [t('all_categories'), t('cat_co'), t('cat_moi'), t('cat_cai_bien')]
                        cat_select = ui.select(
                            cats, 
                            value=state.category,
                            on_change=lambda e: (setattr(state, 'category', e.value or t('all_categories')), setattr(state, 'page', 1), songs_content.refresh())
                        ).props('dense outlined rounded-lg options-dense').classes('modern-select w-32 sm:w-48 bg-background')
                        
                        if app.storage.user.get('role') == 'admin':
                            ui.button(icon='add').on('click.stop', lambda: ui.navigate.to('/admin/edit/song/0')).props('unelevated round size=md').classes('bg-primary text-white shadow-md hover:scale-110 transition-transform shrink-0 cursor-pointer pointer-events-auto z-50')

                    if not melodies:
                        components.empty_state(t('no_songs_found'))
                    else:
                        with ui.row().classes('grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 md:gap-8 w-full px-2'):
                            cat_map_label = {'co': t('cat_co'), 'moi': t('cat_moi'), 'cai-bien': t('cat_cai_bien')}
                            for song in melodies:
                                components.song_card(
                                    song.get('id'),
                                    tc(song, 'name'),
                                    tc(song.get('artist') or {}, 'name') or t('card_artist_default'),
                                    song.get('image_url'),
                                    melody=cat_map_label.get(song.get('category'), t('cat_co')),
                                    duration=song.get('duration'),
                                    video_url=song.get('video_url')
                                )
                        
                        # Use generic pagination component
                        components.pagination_controls(state, state.total_count, songs_content)
                
                await songs_content()

@ui.page('/bai-hat/{id}', response_timeout=60.0)
async def song_detail_page(id: int):
    with theme.frame():
        song_data = await api_client.get_melody(id)
        if not song_data:
            components.empty_state(t('no_songs_found'))
            return

        # Helper to get high-quality YouTube thumbnail
        def get_youtube_thumb(video_url):
            embed = get_embed_url(video_url)
            if embed and 'youtube' in embed:
                video_id = embed.split('/')[-1].split('?')[0]
                return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
            return None

        with ui.element('section').classes('w-full bg-paper-texture min-h-screen animate-fade-in'):
            # --- TOP NAV & BREADCRUMBS ---
            with theme.container().classes('pt-24 pb-12'):
                with ui.row().classes('items-center justify-between w-full mb-8'):
                    with ui.link(target='/bai-hat').classes('flex items-center gap-2 text-primary font-bold no-underline group'):
                        ui.icon('arrow_back', size='20px').classes('group-hover:-translate-x-1 transition-transform')
                        ui.label(t('back_to_library')).classes('text-xs uppercase tracking-widest')
                    
                    if app.storage.user.get('role') == 'admin':
                        ui.button(t('edit_song'), icon='edit', on_click=lambda: ui.navigate.to(f'/admin/edit/song/{id}')).props('unelevated rounded-lg').classes('bg-primary text-white shadow-md transform hover:scale-105 transition-all')

            # --- MAIN STUDIO CONTENT ---
            with theme.container().classes('pb-24'):
                with ui.row().classes('grid grid-cols-1 lg:grid-cols-12 gap-12 w-full'):
                    
                    # LEFT: PLAYER & LYRICS (8 Cols)
                    with ui.column().classes('lg:col-span-8 gap-10'):
                        # Video Player Section (Direct YouTube Link)
                        video_link = song_data.get('video_url')
                        thumb = song_data.get('image_url') or get_youtube_thumb(video_link) or 'https://images.unsplash.com/photo-1599908608021-b5d929aa054e?auto=format&fit=crop&q=80&w=800'
                        
                        if video_link:
                            with ui.element('div').classes('w-full relative aspect-video bg-black cursor-pointer group/video overflow-hidden rounded-[2rem] shadow-elevated').on('click', lambda: ui.run_javascript(f'window.open("{video_link}", "_blank")')):
                                # Background Thumbnail
                                ui.image(thumb).classes('absolute inset-0 w-full h-full object-cover transition-transform duration-1000 group-hover/video:scale-110 opacity-70')
                                
                                # Overlay & Play Button
                                with ui.element('div').classes('absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent flex items-center justify-center transition-opacity group-hover/video:bg-black/40'):
                                    with ui.element('div').classes('flex h-24 w-24 items-center justify-center rounded-full bg-primary/90 text-white shadow-2xl transition-all duration-500 group-hover/video:scale-110 group-hover/video:rotate-12 border-4 border-white/20'):
                                        ui.icon('play_arrow', size='54px')
                                    
                                    # Text Prompt
                                    ui.label(t('click_to_watch')).classes('absolute bottom-8 text-white font-black tracking-[0.4em] uppercase text-xs opacity-60 group-hover/video:opacity-100 transition-opacity')
                        else:
                            # Fallback if no video
                            with ui.element('div').classes('w-full h-[450px] bg-black/40 flex flex-col items-center justify-center gap-4 rounded-[2rem]'):
                                ui.icon('music_off', size='64px').classes('text-white opacity-40')
                                ui.label(t('no_video_available')).classes('text-white font-bold opacity-60 tracking-widest')

                        # Song Title & Basic Info
                        with ui.column().classes('gap-2'):
                            ui.label(tc(song_data, 'name')).classes('font-display text-4xl md:text-6xl font-black text-foreground tracking-tight leading-none mb-2')
                            with ui.row().classes('items-center gap-4'):
                                ui.label(tc(song_data.get('artist') or {}, 'name') or t('card_artist_default')).classes('text-xl font-bold text-primary italic')
                                ui.element('div').classes('h-4 w-[1px] bg-primary/20')
                                cat_label = {'co': t('cat_co'), 'moi': t('cat_moi'), 'cai-bien': t('cat_cai_bien')}.get(song_data.get('category'), t('cat_co'))
                                ui.label(cat_label).classes('text-xs font-black uppercase tracking-widest text-muted-foreground bg-muted/30 px-3 py-1 rounded-full')

                        # Lyrics Component
                        with ui.card().classes('w-full p-10 rounded-[2.5rem] glass-card border-none shadow-elevated relative overflow-hidden'):
                            # Lotus Watermark
                            ui.image('/static/common/lotus-ornament.png').classes('absolute -bottom-12 -left-12 w-48 opacity-[0.04] pointer-events-none rotate-12')
                            
                            with ui.row().classes('items-center gap-3 mb-8'):
                                ui.icon('auto_stories', size='28px', color='primary')
                                ui.label(t('lyrics_title')).classes('text-2xl font-display font-black tracking-tight')
                            
                            lyrics_text = tc(song_data, 'lyrics') or t('updating')
                            ui.html(lyrics_text).classes('text-lg leading-[2] text-foreground/80 italic font-light')

                    # RIGHT: SIDEBAR (4 Cols)
                    with ui.column().classes('lg:col-span-4 gap-8'):
                        # Song Details Card
                        with ui.card().classes('w-full p-8 rounded-[2rem] glass-card border-none shadow-elevated'):
                            ui.label(t('songs_info_title')).classes('text-xs font-black uppercase tracking-[0.3em] text-primary/60 mb-6')
                            
                            details = [
                                (t('duration_label'), song_data.get('duration') or '--:--', 'schedule'),
                                (t('category_label'), cat_label, 'category'),
                                (t('origin_village'), song_data.get('village') or t('heritage_kinh_bac'), 'place')
                            ]
                            
                            for label, value, icon in details:
                                with ui.row().classes('items-center gap-4 mb-5 last:mb-0'):
                                    with ui.element('div').classes('p-2.5 bg-primary/10 rounded-xl'):
                                        ui.icon(icon, size='20px').classes('text-primary')
                                    with ui.column().classes('gap-0'):
                                        ui.label(label).classes('text-[10px] font-black uppercase opacity-60 tracking-widest')
                                        ui.label(value).classes('font-bold text-foreground text-sm')

                        # Comments Section (Inside Sidebar or Bottom)
                        with ui.column().classes('w-full gap-6 mt-4'):
                            with ui.row().classes('items-center justify-between w-full'):
                                ui.label(t('comments_title')).classes('text-xl font-display font-black')
                                ui.icon('forum', size='24px').classes('text-primary/30')
                            
                            @ui.refreshable
                            async def render_comments():
                                current_comments = await api_client.get_comments(melody_id=id)
                                if not current_comments:
                                    with ui.card().classes('w-full p-8 rounded-2xl border-dashed border-primary/10 bg-transparent flex flex-col items-center'):
                                        ui.label(t('no_comments')).classes('text-muted-foreground italic text-xs')
                                else:
                                    for c in current_comments:
                                        with ui.column().classes('w-full p-4 rounded-2xl bg-white/40 border border-primary/5 mb-3 last:mb-0'):
                                            with ui.row().classes('items-center justify-between w-full mb-2'):
                                                with ui.row().classes('items-center gap-2'):
                                                    ui.avatar(icon='person', size='24px', color='primary').classes('text-white')
                                                    ui.label((c.get('user') or {}).get('name', t('anonymous'))).classes('font-bold text-xs')
                                                ui.label(c.get('created_at', '')[:10]).classes('text-[9px] font-black opacity-30')
                                            ui.label(c.get('content')).classes('text-sm text-foreground/80 leading-relaxed')

                            await render_comments()

                            # Comment Input Group
                            if app.storage.user.get('is_authenticated'):
                                with ui.column().classes('w-full mt-4'):
                                    comment_input = ui.input(placeholder=t('comment_placeholder')).props('rounded-2xl outlined').classes('w-full modern-input bg-white/60 flex items-center')
                                    async def post_comment():
                                        if not comment_input.value.strip(): return
                                        if await api_client.create_comment(content=comment_input.value, melody_id=id):
                                            comment_input.value = ''
                                            render_comments.refresh()
                                            ui.notify(t('comment_success'), type='positive')
                                    comment_input.on('keydown.enter', post_comment)
                                    ui.button(t('post_comment'), on_click=post_comment).props('unelevated rounded-lg').classes('w-full bg-primary text-white font-bold py-2 shadow-md')
                            else:
                                ui.button(t('login_to_comment'), on_click=lambda: ui.navigate.to('/dang-nhap')).props('outline rounded-lg color=primary').classes('w-full font-bold text-xs py-2')

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
                ui.label(t('edit_add_song') if is_edit else t('add_song')).classes('font-display text-3xl font-bold text-center mb-6')
                
                artists = await api_client.get_artists()
                artist_options = {a['id']: a.get('name') for a in artists} if artists else {}

                with ui.column().classes('gap-4 w-full'):
                    name = ui.input(t('song_name'), value=song.get('name')).classes('w-full').props('outlined')
                    artist_id = ui.select(artist_options, label=t('select_artist'), value=song.get('artist_id')).classes('w-full').props('outlined')
                    
                    rev_cat_map = {'co': t('cat_co'), 'moi': t('cat_moi'), 'cai-bien': t('cat_cai_bien')}
                    category = ui.select([t('cat_co'), t('cat_moi'), t('cat_cai_bien')], 
                                         label=t('category_label'), value=rev_cat_map.get(song.get('category'), t('cat_co'))).classes('w-full').props('outlined')
                    
                    duration = ui.input(t('duration_label'), value=song.get('duration')).classes('w-full').props('outlined')
                    image_url = ui.input(t('link_image'), value=song.get('image_url')).classes('w-full').props('outlined')
                    video_url = ui.input(t('link_video'), value=song.get('video_url')).classes('w-full').props('outlined')
                    lyrics = ui.textarea(t('lyrics_title'), value=song.get('lyrics')).classes('w-full').props('outlined')

                    async def submit():
                        if not name.value:
                            ui.notify(t('song_name_required'), type='warning')
                            return
                        
                        cat_map = {t('cat_co'): 'co', t('cat_moi'): 'moi', t('cat_cai_bien'): 'cai-bien'}
                        
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
                            ui.notify(t('save_success'), type='positive')
                            ui.navigate.to('/bai-hat')
                        else:
                            ui.notify(t('save_error'), type='negative')

                    ui.button(t('save_song'), on_click=submit).props('unelevated rounded-lg').classes('w-full bg-primary text-white font-bold py-3 mt-4')
