from nicegui import app, ui
import theme
import components
from api import api_client
from translation import t

import asyncio

@ui.page('/admin/edit/{et_type}/{et_id}')
async def admin_editor_page(et_type: str, et_id: int):
    if not app.storage.user.get('is_authenticated') or app.storage.user.get('role') != 'admin':
        ui.navigate.to('/dang-nhap')
        return

    # Mapping for titles and icons
    type_map = {
        'song': (t('et_song'), 'music_note'),
        'artist': (t('et_artist'), 'groups'),
        'village': (t('et_village'), 'map'),
        'news': (t('et_news'), 'article'),
        'event': (t('et_event'), 'event')
    }
    
    label, icon = type_map.get(et_type, (t('et_content'), 'edit'))
    is_edit = et_id > 0
    title_text = f"{t('edit_prefix') if is_edit else t('add_prefix')} {label}"
    
    # Fetch data if editing
    data = {}
    if is_edit:
        if et_type == 'song': data = await api_client.get_melody(et_id)
        elif et_type == 'artist': data = await api_client.get_artist(et_id)
        elif et_type == 'village': data = await api_client.get_village(et_id)
        elif et_type == 'news': data = await api_client.get_article(et_id)
        elif et_type == 'event': data = await api_client.get_event(et_id)
    
    if is_edit and not data:
        ui.notify(t('not_found'), type='negative')
        ui.navigate.to('/admin')
        return

    # Lookups for dropdowns
    artists_list = {}
    if et_type == 'song':
        all_artists = await api_client.get_artists(limit=1000)
        artists_list = {a['id']: a['name'] for a in all_artists}
    
    locations_list = {}
    if et_type == 'event':
        all_locations = await api_client.get_locations(limit=1000)
        locations_list = {l['id']: l['name'] for l in all_locations}

    with theme.frame():
        with ui.element('section').classes('pt-12 pb-24 bg-paper-texture min-h-screen animate-fade-in-up'):
            with theme.container().classes('max-w-6xl'):
                # Header with Stamp
                with ui.row().classes('w-full justify-between items-center mb-12 px-4'):
                    with ui.row().classes('items-center gap-6'):
                        with ui.element('div').classes('h-16 w-16 seal-stamped rounded-3xl flex items-center justify-center rotate-[-3deg] shadow-lg'):
                            ui.icon(icon, size='2.5rem', color='white')
                        with ui.column().classes('gap-0'):
                            ui.label(t('content_admin')).classes('text-[11px] font-black tracking-[0.4em] text-primary opacity-90 uppercase cultural-header-line')
                            ui.label(title_text).classes('text-4xl sm:text-5xl font-display font-bold text-foreground tracking-tighter mt-1')
                    
                    ui.button(on_click=lambda: ui.navigate.back()).props('flat round icon="close" color="grey"').classes('bg-white/40 backdrop-blur-md shadow-sm hover:rotate-90 transition-all duration-500 scale-125')

                fields = {}

                # Layout Grid
                with ui.row().classes('w-full grid grid-cols-1 lg:grid-cols-12 gap-8 items-start'):
                    
                    # === LEFT COLUMN: CONTENT (8 Cols) ===
                    with ui.column().classes('lg:col-span-8 gap-8 w-full'):
                        with ui.card().classes('w-full p-6 sm:p-10 rounded-3xl glass-card border-none shadow-elevated'):
                            with ui.row().classes('items-center justify-between w-full mb-6'):
                                ui.label(t('basic_info')).classes('text-2xl font-bold tracking-tight')
                                
                                with ui.row().classes('bg-muted/20 p-1 rounded-xl'):
                                    form_tabs = ui.tabs().classes('bg-transparent border-none w-auto h-10')
                                    vi_tab = ui.tab('VI').classes('rounded-lg px-6 font-bold')
                                    en_tab = ui.tab('EN').classes('rounded-lg px-6 font-bold')
                            
                            with ui.tab_panels(form_tabs, value=vi_tab).classes('w-full bg-transparent overflow-visible'):
                                # --- VIETNAMESE PANEL ---
                                with ui.tab_panel(vi_tab).classes('p-0 gap-6 flex flex-col'):
                                    is_title_based = et_type in ('news', 'event')
                                    title_key = 'title' if is_title_based else 'name'
                                    name_label = t('field_title') if is_title_based else t('field_name')
                                    fields[title_key] = ui.input(label=name_label, value=data.get('title') if is_title_based else data.get('name')).classes('w-full modern-input').props('outlined rounded-2xl')
                                    
                                    if et_type == 'song':
                                        fields['description'] = ui.textarea(t('field_description'), value=data.get('description')).classes('w-full modern-input').props('outlined rounded-2xl auto-grow')
                                        fields['lyrics'] = ui.textarea(t('field_lyrics'), value=data.get('lyrics')).classes('w-full modern-input').props('outlined rounded-2xl auto-grow')
                                    elif et_type == 'artist':
                                        fields['description'] = ui.textarea(t('field_description'), value=data.get('description')).classes('w-full modern-input').props('outlined rounded-2xl auto-grow')
                                        fields['biography'] = ui.textarea(t('field_biography'), value=data.get('biography')).classes('w-full modern-input').props('outlined rounded-2xl auto-grow')
                                        fields['contributions'] = ui.textarea(t('career_contributions'), value=data.get('contributions')).classes('w-full modern-input').props('outlined rounded-2xl auto-grow')
                                        fields['achievements'] = ui.textarea(t('awards_honors'), value=data.get('achievements')).classes('w-full modern-input').props('outlined rounded-2xl auto-grow')
                                    elif et_type == 'village':
                                        fields['description'] = ui.textarea(t('field_description'), value=data.get('description')).classes('w-full modern-input').props('outlined rounded-2xl auto-grow')
                                        fields['history'] = ui.textarea(t('village_history_title'), value=data.get('history')).classes('w-full modern-input').props('outlined rounded-2xl auto-grow')
                                        fields['culture'] = ui.textarea(t('village_culture_title'), value=data.get('culture')).classes('w-full modern-input').props('outlined rounded-2xl auto-grow')
                                    elif et_type == 'news':
                                        fields['excerpt'] = ui.textarea(t('field_description'), value=data.get('excerpt')).classes('w-full modern-input').props('outlined rounded-2xl auto-grow')
                                        fields['content'] = ui.textarea(t('field_detail_content'), value=data.get('content')).classes('w-full modern-input').props('outlined rounded-2xl auto-grow')
                                    elif et_type == 'event':
                                        fields['description'] = ui.textarea(t('field_event_desc'), value=data.get('description')).classes('w-full modern-input').props('outlined rounded-2xl auto-grow')

                                # --- ENGLISH PANEL ---
                                with ui.tab_panel(en_tab).classes('p-0 gap-6 flex flex-col'):
                                    title_key_en = 'title_en' if is_title_based else 'name_en'
                                    fields[title_key_en] = ui.input(f"{name_label} (EN)", value=data.get(title_key_en)).classes('w-full modern-input').props('outlined rounded-2xl')
                                    
                                    if et_type == 'song':
                                        fields['description_en'] = ui.textarea(f"{t('field_description')} (EN)", value=data.get('description_en')).classes('w-full modern-input').props('outlined rounded-2xl auto-grow')
                                        fields['lyrics_en'] = ui.textarea(f"{t('field_lyrics')} (EN)", value=data.get('lyrics_en')).classes('w-full modern-input').props('outlined rounded-2xl auto-grow')
                                    elif et_type == 'artist':
                                        fields['description_en'] = ui.textarea(f"{t('field_description')} (EN)", value=data.get('description_en')).classes('w-full modern-input').props('outlined rounded-2xl auto-grow')
                                        fields['biography_en'] = ui.textarea(f"{t('field_biography')} (EN)", value=data.get('biography_en')).classes('w-full modern-input').props('outlined rounded-2xl auto-grow')
                                        fields['contributions_en'] = ui.textarea(f"{t('career_contributions')} (EN)", value=data.get('contributions_en')).classes('w-full modern-input').props('outlined rounded-2xl auto-grow')
                                        fields['achievements_en'] = ui.textarea(f"{t('awards_honors')} (EN)", value=data.get('achievements_en')).classes('w-full modern-input').props('outlined rounded-2xl auto-grow')
                                    elif et_type == 'village':
                                        fields['description_en'] = ui.textarea(f"{t('field_description')} (EN)", value=data.get('description_en')).classes('w-full modern-input').props('outlined rounded-2xl auto-grow')
                                        fields['history_en'] = ui.textarea(f"{t('village_history_title')} (EN)", value=data.get('history_en')).classes('w-full modern-input').props('outlined rounded-2xl auto-grow')
                                        fields['culture_en'] = ui.textarea(f"{t('village_culture_title')} (EN)", value=data.get('culture_en')).classes('w-full modern-input').props('outlined rounded-2xl auto-grow')
                                    elif et_type == 'news':
                                        fields['excerpt_en'] = ui.textarea(f"{t('field_description')} (EN)", value=data.get('excerpt_en')).classes('w-full modern-input').props('outlined rounded-2xl auto-grow')
                                        fields['content_en'] = ui.textarea(f"{t('field_detail_content')} (EN)", value=data.get('content_en')).classes('w-full modern-input').props('outlined rounded-2xl auto-grow')
                                    elif et_type == 'event':
                                        fields['description_en'] = ui.textarea(f"{t('field_event_desc')} (EN)", value=data.get('description_en')).classes('w-full modern-input').props('outlined rounded-2xl auto-grow')

                    # === RIGHT COLUMN: META & MEDIA (4 Cols) ===
                    with ui.column().classes('lg:col-span-4 gap-8 w-full sticky top-24'):
                        
                        # Media Card
                        with ui.card().classes('w-full p-6 rounded-3xl glass-card border-none shadow-elevated'):
                            ui.label(t('field_image_url')).classes('text-xs font-black uppercase tracking-widest text-primary mb-4')
                            fields['image_url'] = ui.input(value=data.get('image_url')).classes('w-full modern-input').props('outlined rounded-2xl dense')
                            
                            placeholder = 'https://images.unsplash.com/photo-1599908608021-b5d929aa054e?auto=format&fit=crop&q=80&w=800'
                            with ui.element('div').classes('w-full aspect-video rounded-2xl overflow-hidden mt-4 border-2 border-primary/10 relative group bg-muted/20'):
                                ui.image().classes('w-full h-full object-cover transition-transform duration-700 group-hover:scale-110').bind_source_from(fields['image_url'], 'value', backward=lambda v: v if v else placeholder)
                                with ui.element('div').classes('absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center'):
                                    ui.icon('visibility', size='2rem', color='white')
                            
                            if et_type == 'song':
                                fields['audio_url'] = ui.input(t('field_audio_url'), value=data.get('audio_url')).classes('w-full modern-input mt-4').props('outlined rounded-2xl dense')
                                fields['video_url'] = ui.input(t('field_video_url'), value=data.get('video_url')).classes('w-full modern-input mt-2').props('outlined rounded-2xl dense')
                                fields['duration'] = ui.input(t('field_duration'), value=data.get('duration')).classes('w-full modern-input mt-2').props('outlined rounded-2xl dense')

                        # Classification Card
                        with ui.card().classes('w-full p-6 rounded-3xl glass-card border-none shadow-elevated'):
                            ui.label(t('classification')).classes('text-xs font-black uppercase tracking-widest text-primary mb-4')
                            
                            with ui.column().classes('w-full gap-4'):
                                if et_type == 'song':
                                    fields['category'] = ui.select({'co': t('cat_co'), 'moi': t('cat_moi'), 'cai-bien': t('cat_cai_bien')}, value=data.get('category', 'co'), label=t('field_category')).classes('w-full modern-input').props('outlined rounded-2xl')
                                    fields['difficulty'] = ui.select({'de': t('difficulty_easy'), 'trung-binh': t('difficulty_medium'), 'kho': t('difficulty_hard')}, value=data.get('difficulty', 'trung-binh'), label=t('field_difficulty')).classes('w-full modern-input').props('outlined rounded-2xl')
                                    fields['artist_id'] = ui.select(artists_list, value=data.get('artist_id'), label=t('field_artist')).classes('w-full modern-input').props('outlined rounded-2xl')
                                    fields['village'] = ui.input(t('hometown'), value=data.get('village')).classes('w-full modern-input').props('outlined rounded-2xl')
                                elif et_type == 'artist':
                                    fields['generation'] = ui.select({'truyen-thong': t('gen_traditional_full'), 'the-he-moi': t('gen_new')}, value=data.get('generation', 'truyen-thong'), label=t('field_generation')).classes('w-full modern-input').props('outlined rounded-2xl')
                                    fields['birth_year'] = ui.number(t('field_birth_year'), value=data.get('birth_year')).classes('w-full modern-input').props('outlined rounded-2xl')
                                    fields['death_year'] = ui.number(t('field_death_year'), value=data.get('death_year')).classes('w-full modern-input').props('outlined rounded-2xl')
                                    fields['performances'] = ui.number(t('field_performances'), value=data.get('performances', 0)).classes('w-full modern-input').props('outlined rounded-2xl')
                                    fields['village'] = ui.input(t('hometown'), value=data.get('village')).classes('w-full modern-input').props('outlined rounded-2xl')
                                elif et_type == 'village':
                                    fields['type'] = ui.select({'lang-quan-ho': t('type_village'), 'le-hoi': t('type_festival'), 'dien-xuong': t('type_performance')}, value=data.get('type', 'lang-quan-ho'), label=t('field_type')).classes('w-full modern-input').props('outlined rounded-2xl')
                                    fields['district'] = ui.input(t('field_district'), value=data.get('district')).classes('w-full modern-input').props('outlined rounded-2xl')
                                    fields['address'] = ui.input(t('field_address'), value=data.get('address')).classes('w-full modern-input').props('outlined rounded-2xl')
                                    fields['artist_count'] = ui.number(t('field_artist_count'), value=data.get('artist_count', 0)).classes('w-full modern-input').props('outlined rounded-2xl')
                                    fields['featured_songs'] = ui.input(t('field_featured_songs'), value=data.get('featured_songs')).classes('w-full modern-input').props('outlined rounded-2xl')
                                    fields['badges'] = ui.input(t('field_badges'), value=data.get('badges')).classes('w-full modern-input').props('outlined rounded-2xl')
                                    with ui.row().classes('w-full grid grid-cols-2 gap-2'):
                                        fields['latitude'] = ui.number(t('field_latitude'), value=data.get('latitude')).classes('w-full modern-input').props('outlined rounded-2xl dense')
                                        fields['longitude'] = ui.number(t('field_longitude'), value=data.get('longitude')).classes('w-full modern-input').props('outlined rounded-2xl dense')
                                elif et_type == 'news':
                                    fields['category'] = ui.select({'tin-tuc': t('cat_news'), 'le-hoi': t('cat_festival'), 'nghe-thuat': t('cat_art'), 'lich-su': t('cat_history')}, value=data.get('category', 'tin-tuc'), label=t('field_classification')).classes('w-full modern-input').props('outlined rounded-2xl')
                                    fields['status'] = ui.select({'draft': t('status_draft'), 'published': t('status_published')}, value=data.get('status', 'draft'), label=t('field_status')).classes('w-full modern-input').props('outlined rounded-2xl')
                                elif et_type == 'event':
                                    fields['start_date'] = ui.input(t('field_event_date'), value=data.get('start_date')[:10] if data.get('start_date') else '').classes('w-full modern-input').props('outlined rounded-2xl')
                                    fields['end_date'] = ui.input(t('field_end_date'), value=data.get('end_date')[:10] if data.get('end_date') else '').classes('w-full modern-input').props('outlined rounded-2xl')
                                    fields['status'] = ui.select({'upcoming': t('status_upcoming'), 'ongoing': t('status_ongoing'), 'finished': t('status_finished')}, value=data.get('status', 'upcoming'), label=t('field_status')).classes('w-full modern-input').props('outlined rounded-2xl')
                                    fields['location_id'] = ui.select(locations_list, value=data.get('location_id'), label=t('field_location')).classes('w-full modern-input').props('outlined rounded-2xl')
                                    fields['max_participants'] = ui.number(t('field_max_participants'), value=data.get('max_participants', 100)).classes('w-full modern-input').props('outlined rounded-2xl')

                        # Save Card
                        with ui.card().classes('w-full p-6 rounded-3xl glass-card border-none shadow-elevated bg-primary/5'):
                            async def handle_save():
                                save_btn.props('loading')
                                # Payload preparation
                                payload = {}
                                for k, v in fields.items():
                                    val = v.value if hasattr(v, 'value') else v
                                    # Clean up empty strings for optional non-string fields
                                    if val == "" or val is None:
                                        # Skip optional fields if empty, or send None
                                        # Fields that MUST be handled as None/Null (not ""):
                                        null_fields = ['start_date', 'end_date', 'birth_year', 'death_year', 'location_id', 'artist_id']
                                        if k in null_fields:
                                            payload[k] = None
                                        else:
                                            payload[k] = "" if val == "" else val
                                    else:
                                        payload[k] = val

                                # Final data type casting
                                if 'location_id' in payload and payload['location_id']:
                                    try: payload['location_id'] = int(payload['location_id'])
                                    except: payload['location_id'] = None
                                
                                if 'artist_id' in payload and payload['artist_id']:
                                    try: payload['artist_id'] = int(payload['artist_id'])
                                    except: payload['artist_id'] = None

                                # Call API...
                                if is_edit:
                                    if et_type == 'song': res = await api_client.update_melody(et_id, payload)
                                    elif et_type == 'artist': res = await api_client.update_artist(et_id, payload)
                                    elif et_type == 'village': res = await api_client.update_location(et_id, payload)
                                    elif et_type == 'news': res = await api_client.update_article(et_id, payload)
                                    elif et_type == 'event': res = await api_client.update_event(et_id, payload)
                                else:
                                    if et_type == 'song': res = await api_client.create_melody(payload)
                                    elif et_type == 'artist': res = await api_client.create_artist(payload)
                                    elif et_type == 'village': res = await api_client.create_location(payload)
                                    elif et_type == 'news': res = await api_client.create_article(payload)
                                    elif et_type == 'event': res = await api_client.create_event(payload)
                                
                                save_btn.props(remove='loading')
                                if res:
                                    ui.notify(t('edit_success') if is_edit else t('add_success'), type='positive')
                                    await asyncio.sleep(0.8)
                                    ui.navigate.back()
                                else:
                                    ui.notify(t('save_data_error_editor'), type='negative')

                            save_btn = ui.button(t('save_data'), on_click=handle_save).props('unelevated color="primary"').classes('w-full py-4 rounded-2xl font-black elevated-btn shadow-lg shadow-primary/20 text-lg')
                            ui.button(t('cancel_editor'), on_click=lambda: ui.navigate.back()).props('flat color="grey"').classes('w-full py-2 rounded-xl mt-2 font-bold font-display')
