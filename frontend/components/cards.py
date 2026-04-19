from nicegui import app, ui
from datetime import datetime
import theme
from translation import t
from api import api_client

def _admin_controls(et_type, et_id):
    """Helper to render Edit/Delete buttons for admins."""
    if app.storage.user.get('role') != 'admin':
        return
        
    async def confirm_delete():
        with ui.dialog() as dialog, ui.card().classes('p-8 rounded-3xl items-center text-center'):
            ui.icon('warning', size='4rem', color='negative').classes('mb-4')
            ui.label(t('confirm_delete')).classes('text-2xl font-bold mb-2')
            ui.label(t('delete_confirm_msg')).classes('text-muted-foreground mb-6')
            with ui.row().classes('gap-4'):
                ui.button(t('cancel_btn'), on_click=dialog.close).props('flat')
                async def do_del():
                    ok = False
                    if et_type == 'song': ok = await api_client.delete_melody(et_id)
                    elif et_type == 'artist': ok = await api_client.delete_artist(et_id)
                    elif et_type == 'village': ok = await api_client.delete_location(et_id)
                    elif et_type == 'news': ok = await api_client.delete_article(et_id)
                    elif et_type == 'event': ok = await api_client.delete_event(et_id)
                    
                    if ok:
                        ui.notify(t('delete_success'), type='positive')
                        ui.navigate.reload()
                    else:
                        ui.notify(t('delete_error'), type='negative')
                ui.button(t('delete_btn'), on_click=do_del).props('unelevated color=negative').classes('rounded-xl px-6')
        dialog.open()

    with ui.row().classes('absolute right-2 bottom-2 z-20 gap-1 opacity-0 group-hover:opacity-100 transition-opacity bg-background/80 backdrop-blur-sm p-1 rounded-xl shadow-lg border border-border/50'):
        ui.button(icon='edit', on_click=lambda: ui.navigate.to(f'/admin/edit/{et_type}/{et_id}')).props('flat round size=sm').classes('text-primary hover:bg-primary/10')
        ui.button(icon='delete', on_click=confirm_delete).props('flat round size=sm').classes('text-negative hover:bg-negative/10')

def song_card(id, title, artist, image_url, melody=None, duration=None, video_url=None):
    from utils import get_embed_url
    
    # Resolve thumbnail: prioritize database image_url, fallback to YouTube HQ thumb
    final_image = image_url
    if not final_image and video_url:
        embed = get_embed_url(video_url)
        if embed and 'youtube' in embed:
            video_id = embed.split('/')[-1].split('?')[0]
            final_image = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
    
    if not final_image:
        final_image = 'https://images.unsplash.com/photo-1599908608021-b5d929aa054e?auto=format&fit=crop&q=80&w=400'

    with ui.element('div').classes('relative group cursor-pointer'):
        # Admin controls (Integrated)
        _admin_controls('song', id)
        
        # Clickable area
        with ui.element('div').classes('w-full').on('click', lambda id=id: ui.navigate.to(f'/bai-hat/{id}')):
            # Favorite button
            favorite_ids = set(app.storage.user.get('favorite_ids', []))
            is_favorite = id in favorite_ids

            async def toggle_favorite(e=None):
                if not app.storage.user.get('is_authenticated'):
                    ui.notify(t('login_to_favorite'), type='warning')
                    return
                fav_ids = set(app.storage.user.get('favorite_ids', []))
                if id in fav_ids:
                    ok = await api_client.remove_favorite(id)
                    if ok:
                        fav_ids.discard(id)
                        fav_icon.name = 'favorite_border'
                        ui.notify(t('unfavorited'), type='positive')
                else:
                    ok = await api_client.add_favorite(id)
                    if ok:
                        fav_ids.add(id)
                        fav_icon.name = 'favorite'
                        ui.notify(t('added_to_favorite'), type='positive')
                app.storage.user['favorite_ids'] = list(fav_ids)

            with ui.element('div').classes(
                'absolute left-3 top-3 z-30 flex h-9 w-9 items-center justify-center rounded-full '
                'bg-white/60 text-muted-foreground backdrop-blur-md cursor-pointer '
                'hover:bg-primary hover:text-white transition-all shadow-sm group-hover:scale-110'
            ).on('click.stop', toggle_favorite):
                fav_icon = ui.icon('favorite' if is_favorite else 'favorite_border', size='20px')
                
            with ui.card().classes(
                'group overflow-hidden rounded-2xl border border-border/50 bg-card shadow-sm '
                'hover:shadow-elevated hover:border-primary/30 transition-all duration-500 p-0 relative'
            ):
                # Cultural Silk Ribbon (Visible on hover)
                ui.element('div').classes('absolute -right-12 top-6 h-6 w-40 bg-hero-gradient rotate-45 transform opacity-0 group-hover:opacity-100 transition-opacity duration-700 pointer-events-none z-10 shadow-md')

                # Thumbnail
                with ui.element('div').classes('relative aspect-[5/4] w-full overflow-hidden'):
                    ui.image(final_image).classes('absolute inset-0 h-full w-full object-cover transition-transform duration-700 group-hover:scale-110 group-hover:rotate-1')
                    # Play overlay
                    with ui.element('div').classes('absolute inset-0 bg-black/0 group-hover:bg-black/30 transition-all flex items-center justify-center'):
                        with ui.element('div').classes('flex h-14 w-14 scale-0 items-center justify-center rounded-full bg-primary/90 text-white transition-transform duration-500 group-hover:scale-100 shadow-xl border-2 border-white/20'):
                            ui.icon('play_arrow', size='32px')
                
                # Info
                with ui.column().classes('p-6 gap-1 w-full bg-paper-texture/10'):
                    ui.label(title).classes('font-display text-lg font-bold text-foreground line-clamp-1 group-hover:text-primary transition-colors tracking-tight')
                    ui.label(artist).classes('text-sm text-muted-foreground font-semibold leading-none mb-2')
                    
                    with ui.row().classes('mt-4 pt-3 flex items-center justify-between w-full border-t border-border/40'):
                        with ui.row().classes('items-center gap-1.5'):
                            ui.icon('music_note', size='16px').classes('text-primary/60')
                            ui.label(melody or t('card_melody_old')).classes('text-[11px] font-bold uppercase tracking-wider text-muted-foreground')
                        with ui.row().classes('items-center gap-1.5'):
                            ui.icon('schedule', size='16px').classes('text-primary/60')
                            ui.label(duration or '03:45').classes('text-[11px] font-black text-muted-foreground')

def artist_card(id, name, photo_url, title, index=0):
    with ui.element('div').classes('relative group h-full'):
        _admin_controls('artist', id)
        
        with ui.card().classes(
            'group overflow-hidden rounded-2xl border border-border/50 bg-card shadow-sm '
            'hover:shadow-elevated hover:border-primary/30 transition-all duration-500 p-0 cursor-pointer w-full h-full'
        ).on('click', lambda: ui.navigate.to(f'/nghe-nhan/{id}')):
            # Header Image with Gradient
            with ui.element('div').classes('relative aspect-square w-full overflow-hidden'):
                ui.image(photo_url).classes('absolute inset-0 h-full w-full object-cover transition-transform duration-700 group-hover:scale-110')
                with ui.element('div').classes('absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent opacity-60 group-hover:opacity-100 transition-opacity'):
                    pass
                with ui.element('div').classes('absolute bottom-0 left-0 right-0 p-5 z-10'):
                    ui.label(name).classes('font-display text-2xl font-bold text-white leading-tight drop-shadow-lg')
                    with ui.row().classes('items-center gap-2 mt-1'):
                        ui.icon('verified', size='16px', color='primary').classes('text-white/80')
                        ui.label(t('heritage_kinh_bac')).classes('text-white/70 text-[10px] font-bold uppercase tracking-widest')
            
            # Info Content with Texture
            with ui.column().classes('p-6 gap-3 bg-paper-texture/10 w-full relative h-[110px]'):
                # Background Ornament
                with ui.element('div').classes('absolute -right-2 -bottom-2 opacity-[0.03] group-hover:opacity-[0.07] transition-opacity'):
                    ui.icon('history_edu', size='5rem')

                with ui.row().classes('items-center gap-2.5 text-sm font-black text-foreground/80 tracking-tight'):
                    ui.icon('place', size='20px', color='primary').classes('drop-shadow-sm')
                    ui.label(f'{t("villages")} {title or t("heritage_kinh_bac")}').classes('line-clamp-1 italic')
                
                with ui.row().classes('items-center gap-2.5 text-xs font-black uppercase text-primary tracking-widest'):
                    ui.icon('verified', size='16px', color='primary')
                    ui.label(f'{12 + index} {t("card_songs")}').classes('drop-shadow-sm')

def news_card(id, title, image_url, type=None, date='--/--/----', category=None):
    # Determine the label to show (Priority: Category translated, then Type fallback)
    if category:
        type_label = t(f'cat_{category.replace("-", "_")}')
    else:
        type_label = t('card_news') if type != t('event_label') else t('card_event')
        
    target = f'/su-kien/{id}' if type == t('event_label') else f'/tin-tuc/{id}'
    with ui.element('div').classes('group relative overflow-hidden'):
        _admin_controls('news', id)
        
        with ui.link(target=target).classes(
            'flex gap-4 rounded-lg border border-border bg-background p-4 shadow-card '
            'transition-all hover:shadow-elevated hover:border-primary/50 no-underline'
        ):
            ui.image(image_url).classes('h-24 w-24 flex-shrink-0 rounded-md object-cover transition-transform duration-500 group-hover:scale-105')
            
            with ui.column().classes('min-w-0 flex-1'):
                ui.label(type_label).classes('inline-block rounded bg-primary/10 px-2 py-0.5 text-[10px] font-bold text-primary uppercase tracking-wider')
                ui.label(title).classes('mt-1 line-clamp-2 font-display text-sm font-bold text-foreground group-hover:text-primary transition-colors leading-snug')
                with ui.row().classes('mt-2 items-center gap-1 text-[11px] text-muted-foreground'):
                    ui.icon('calendar_today', size='12px')
                    ui.label(date)

def intro_feature_card(icon_name, title, desc):
    with ui.card().classes(
        'group relative overflow-hidden rounded-2xl border-none p-8 '
        'shadow-sm transition-all duration-500 hover:-translate-y-2 hover:shadow-2xl '
        'h-full flex flex-col bg-paper-texture'
    ).style('box-shadow: 0 10px 30px -10px rgba(139, 0, 0, 0.1);'):
        
        # Decorative dual-line border (Ancient style)
        ui.element('div').classes('absolute inset-2 border border-[#d4af37]/20 pointer-events-none rounded-xl')
        
        # Decorative background ornament (Lotus chìm)
        ui.image('/static/common/lotus-ornament.png').classes(
            'absolute -right-8 -top-8 h-32 w-32 opacity-[0.03] transition-transform '
            'duration-700 group-hover:scale-150 group-hover:opacity-[0.06] pointer-events-none'
        )
        
        with ui.element('div').classes(
            'mb-6 inline-flex h-14 w-14 items-center justify-center rounded-xl '
            'bg-primary/5 text-primary border border-primary/10 transition-all duration-300 '
            'group-hover:bg-primary group-hover:shadow-lg group-hover:shadow-primary/30'
        ):
            ui.icon(icon_name, size='28px').classes('transition-colors group-hover:text-white')
            
        ui.label(title).classes(
            'mb-4 font-display text-2xl font-bold text-foreground transition-colors group-hover:text-primary'
        )
        ui.label(desc).classes('text-muted-foreground leading-relaxed flex-1 text-sm font-light')
        
        # Bottom accent
        ui.element('div').classes(
            'w-0 group-hover:w-12 h-0.5 bg-primary transition-all duration-500 mt-4'
        )

def village_grid_card(item, on_map_click=None):
    with ui.element('div').classes('relative group h-full'):
        _admin_controls('village', item.get('id'))
        
        with ui.card().classes(
            'overflow-hidden rounded-2xl border border-border bg-card shadow-sm '
            'hover:shadow-elevated transition-all p-0 flex flex-col h-full'
        ):
            # Image
            with ui.element('div').classes('relative aspect-[16/10] w-full overflow-hidden cursor-pointer').on('click', lambda id=item.get('id'): ui.navigate.to(f'/lang-quan-ho/{id}')):
                ui.image(item.get('image_url') or 'https://images.unsplash.com/photo-1526462981764-f6cf0f4ea260?auto=format&fit=crop&q=80&w=600').classes('absolute inset-0 h-full w-full object-cover transition-transform duration-500 group-hover:scale-105')
                
                # Badges overlay
                badges = item.get('badges')
                if badges:
                    with ui.row().classes('absolute top-3 left-3 gap-2'):
                        for badge in badges.split(','):
                            ui.label(badge.strip()).classes('bg-primary/90 text-white text-[10px] font-bold px-2 py-1 rounded shadow-sm backdrop-blur-sm')

            # Content
            with ui.column().classes('p-5 gap-3 flex-1 bg-paper-texture/5 relative'):
                # Background Ornament
                with ui.element('div').classes('absolute -right-4 -bottom-4 opacity-5'):
                    ui.icon('lotus', size='6rem')

                with ui.column().classes('gap-1'):
                    ui.label(item.get('name', t('village_name_default'))).classes('font-display text-xl font-bold text-foreground group-hover:text-primary transition-colors cursor-pointer leading-tight').on('click', lambda id=item.get('id'): ui.navigate.to(f'/lang-quan-ho/{id}'))
                    with ui.row().classes('items-center gap-1.5 text-xs font-bold text-primary tracking-wide'):
                        ui.icon('location_on', size='16px')
                        ui.label(f"{t('village_district_prefix')} {item.get('district') or t('heritage_kinh_bac')}").classes('uppercase')

                ui.label(item.get('description', '')).classes('text-sm text-muted-foreground line-clamp-2 leading-relaxed')

                # Stats Glass Card
                with ui.row().classes('w-full justify-between items-center bg-white/40 backdrop-blur-md p-3 rounded-2xl border border-white/50 shadow-sm mt-2'):
                    with ui.column().classes('items-center gap-0'):
                        ui.label(str(item.get('artist_count', 0))).classes('text-lg font-black text-primary')
                        ui.label(t('artists')).classes('text-[8px] uppercase font-black text-muted-foreground mt-[-2px]')
                    
                    ui.element('div').classes('w-[1px] h-8 bg-primary/10')
                    
                    with ui.column().classes('flex-1 px-4 gap-0'):
                        ui.label(t('featured_melodies_label')).classes('text-[8px] uppercase font-black text-muted-foreground mb-0.5 tracking-tighter')
                        songs = item.get('featured_songs', t('updating'))
                        ui.label(songs).classes('text-[10px] font-bold text-foreground line-clamp-1 italic')

            # Action
            with ui.row().classes('w-full mt-auto pt-1 gap-2 p-5 pt-0'):
                ui.button(t('card_view_detail'), on_click=lambda id=item.get('id'): ui.navigate.to(f'/lang-quan-ho/{id}')).props('outline color="primary" rounded dense').classes('flex-1 text-[10px] font-bold')
                if on_map_click:
                    ui.button(t('card_map'), icon='map', on_click=on_map_click).props('unelevated color="primary" rounded dense').classes('flex-1 text-[10px] font-bold')

def news_grid_card(item):
    with ui.element('div').classes('relative group h-full'):
        _admin_controls('news', item.get('id'))
        
        with ui.card().classes('w-full p-0 flex flex-col overflow-hidden hover:shadow-2xl transition-all duration-500 cursor-pointer bg-card border border-border/50 h-full rounded-2xl group').on('click', lambda id=item.get('id'): ui.navigate.to(f'/tin-tuc/{id}')):
            with ui.element('div').classes('relative w-full aspect-[16/10] overflow-hidden'):
                ui.image(item.get('image_url') or 'https://images.unsplash.com/photo-1599908608021-b5d929aa054e?auto=format&fit=crop&w=800&q=80').classes('absolute inset-0 w-full h-full object-cover transition-transform duration-1000 group-hover:scale-110')
                ui.element('div').classes('absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none')
                
                # Cultural ornament in corner
                with ui.element('div').classes('absolute bottom-2 right-2 opacity-10 group-hover:opacity-30 transition-opacity'):
                    ui.icon('lotus', size='3rem', color='white')

            with ui.column().classes('p-6 flex-grow w-full gap-2 relative bg-paper-texture/10 backdrop-blur-sm'):
                # Background Ornament
                with ui.element('div').classes('absolute -right-4 -bottom-4 opacity-[0.03] group-hover:opacity-[0.06] transition-opacity'):
                    ui.icon('lotus', size='6rem')

                with ui.row().classes('justify-between items-center w-full mb-1'):
                    cat_key = item.get('category', 'news').replace('-', '_')
                    cat_label = t(f'cat_{cat_key}')
                    if cat_label == f'cat_{cat_key}': cat_label = t('news_label')
                    
                    ui.label(cat_label).classes('text-[10px] font-black text-primary uppercase tracking-[0.2em] bg-primary/10 px-3 py-1 rounded-sm border border-primary/20')
                    date_str = (item.get('created_at') or '--/--/----')[:10]
                    with ui.row().classes('items-center gap-1.5 text-muted-foreground'):
                        ui.icon('schedule', size='14px').classes('text-primary/50')
                        ui.label(date_str).classes('text-[10px] font-black tracking-widest')
                        
                ui.label(item.get('title', t('no_title'))).classes('text-lg font-black font-display line-clamp-2 mb-1 group-hover:text-primary transition-colors leading-tight tracking-tight')
                ui.label(item.get('excerpt') or item.get('description') or t('updating')).classes('text-xs text-muted-foreground line-clamp-2 mb-4 flex-grow font-medium leading-relaxed italic')
                
                with ui.row().classes('items-center text-primary mt-auto gap-2 text-sm font-black opacity-0 -translate-x-4 transition-all duration-500 group-hover:opacity-100 group-hover:translate-x-0'):
                    ui.label(t('read_more').upper()).classes('tracking-[0.3em] text-[10px]')
                    ui.icon('arrow_right_alt', size='20px')

def event_grid_card(item, on_register=None):
    with ui.element('div').classes('relative group h-full'):
        _admin_controls('event', item.get('id'))
        
        with ui.card().classes('w-full p-0 flex flex-col overflow-hidden hover:shadow-elevated transition-all duration-300 bg-card border border-border h-full'):
            with ui.element('div').classes('relative w-full aspect-[16/10] overflow-hidden cursor-pointer').on('click', lambda id=item.get('id'): ui.navigate.to(f'/su-kien/{id}')):
                ui.image(item.get('image_url') or 'https://images.unsplash.com/photo-1526462981764-f6cf0f4ea260?auto=format&fit=crop&w=800&q=80').classes('absolute inset-0 w-full h-full object-cover transition-transform duration-700 group-hover:scale-105')
                ui.element('div').classes('absolute inset-0 bg-gradient-to-t from-black/50 to-transparent')
                ui.label(t('event_badge')).classes('absolute top-3 left-3 text-[10px] font-bold text-white uppercase tracking-wider bg-primary px-2.5 py-1 rounded-sm shadow-md z-10')
                
                # Date overlay
                date_str = (item.get('start_date') or '--/--/----')[:10]
                with ui.row().classes('absolute bottom-3 left-3 items-center gap-1.5 text-white z-10'):
                    ui.icon('event', size='16px')
                    ui.label(date_str).classes('text-sm font-medium drop-shadow-md')

            with ui.column().classes('p-4 sm:p-5 flex-grow w-full gap-0 relative'):
                ui.label(item.get('title', t('no_title'))).classes('text-base font-bold font-display line-clamp-2 mb-2 hover:text-primary transition-colors cursor-pointer leading-snug').on('click', lambda id=item.get('id'): ui.navigate.to(f'/su-kien/{id}'))
                
                # Countdown timer
                with ui.row().classes('items-center gap-2 mb-4 bg-primary/5 px-3 py-1.5 rounded-full border border-primary/10 w-fit'):
                    ui.icon('timer', size='14px').classes('text-primary')
                    countdown_label = ui.label(t('calculating')).classes('text-[11px] font-bold text-primary uppercase tracking-tighter')
                    
                    def update_countdown(target_date_str=item.get('start_date'), label=countdown_label):
                        if not target_date_str:
                            label.text = t('unknown_date')
                            return
                        try:
                            # Handle simple date or isoformat
                            if ' ' in target_date_str: target_date_str = target_date_str.split(' ')[0]
                            target_date = datetime.strptime(target_date_str[:10], "%Y-%m-%d")
                            now = datetime.now()
                            diff = target_date - now
                            if diff.total_seconds() <= 0:
                                label.text = t('ongoing')
                            else:
                                d = diff.days
                                h, rem = divmod(diff.seconds, 3600)
                                m, s = divmod(rem, 60)
                                label.text = t('countdown_format').format(days=d, time=f"{h:02}:{m:02}:{s:02}")
                        except:
                            label.text = t('coming_soon')
                    
                    ui.timer(1.0, update_countdown)

                ui.label(item.get('description', '')).classes('text-xs text-muted-foreground line-clamp-2 mb-3')
                
                with ui.column().classes('w-full gap-2 mb-4 bg-muted/30 p-3 rounded-xl border border-border/50'):
                    with ui.row().classes('items-start gap-2 text-xs text-foreground flex-nowrap'):
                        ui.icon('place', size='16px').classes('text-primary mt-0.5 shrink-0')
                        ui.label(item.get('location', t('at_local'))).classes('line-clamp-1 font-medium leading-tight')
                    with ui.row().classes('items-center gap-2 text-xs text-foreground'):
                        ui.icon('group', size='16px').classes('text-primary shrink-0')
                        # Fallback to max_participants if available_slots not provided
                        slots = item.get('available_slots')
                        if slots is None: slots = item.get('max_participants', 100)
                        ui.label(t('slots_remaining').format(slots=slots)).classes('font-medium')
                
                is_registered = item.get('is_registered', False)
                btn_text = t('registered_btn') if is_registered else t('register_participate')
                
                btn = ui.button(btn_text, icon='how_to_reg' if not is_registered else 'check_circle').classes('w-full mt-auto py-2.5 rounded-lg font-bold tracking-wide shadow-sm').props(f'color="{"grey" if is_registered else "primary"}" {"disable" if is_registered else ""} unelevated')
                if on_register:
                    btn.on('click', lambda e: on_register(item, btn))
