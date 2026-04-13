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
            ui.label('Xác nhận xóa?').classes('text-2xl font-bold mb-2')
            ui.label('Hành động này sẽ xóa dữ liệu vĩnh viễn.').classes('text-muted-foreground mb-6')
            with ui.row().classes('gap-4'):
                ui.button('Hủy', on_click=dialog.close).props('flat')
                async def do_del():
                    if et_type == 'song': ok = await api_client.delete_melody(et_id)
                    elif et_type == 'artist': ok = await api_client.delete_artist(et_id)
                    elif et_type == 'village': ok = await api_client.delete_location(et_id)
                    elif et_type == 'news': ok = await api_client.delete_article(et_id)
                    
                    if ok:
                        ui.notify('Đã xóa thành công', type='positive')
                        ui.navigate.reload()
                    else:
                        ui.notify('Lỗi khi xóa', type='negative')
                ui.button('Xóa', on_click=do_del).props('unelevated color=negative').classes('rounded-xl px-6')
        dialog.open()

    with ui.row().classes('absolute right-2 bottom-2 z-20 gap-1 opacity-0 group-hover:opacity-100 transition-opacity bg-background/80 backdrop-blur-sm p-1 rounded-xl shadow-lg border border-border/50'):
        ui.button(icon='edit', on_click=lambda: ui.navigate.to(f'/admin/edit/{et_type}/{et_id}')).props('flat round size=sm').classes('text-primary hover:bg-primary/10')
        ui.button(icon='delete', on_click=confirm_delete).props('flat round size=sm').classes('text-negative hover:bg-negative/10')

def song_card(id, title, artist, image_url, melody=None, duration=None):
    with ui.element('div').classes('relative group cursor-pointer'):
        # Admin controls (Integrated)
        _admin_controls('song', id)
        
        with ui.element('div').classes('w-full').on('click', lambda id=id: ui.navigate.to(f'/bai-hat/{id}')):
            # Favorite button
            with ui.element('div').classes(
                'absolute left-3 top-3 z-10 flex h-8 w-8 items-center justify-center rounded-full '
                'bg-background/80 text-muted-foreground backdrop-blur-sm cursor-pointer '
                'hover:bg-primary hover:text-white transition-all shadow-sm'
            ):
                ui.icon('favorite_border', size='18px')
                
            with ui.card().classes(
                'group overflow-hidden rounded-lg border border-border bg-card shadow-card '
                'hover:shadow-elevated transition-all p-0'
            ):
                # Thumbnail
                with ui.element('div').classes('relative aspect-[4/3] w-full overflow-hidden'):
                    ui.image(image_url or 'https://images.unsplash.com/photo-1543163521-1bf539c55dd2').classes('h-full w-full object-cover transition-transform duration-500 group-hover:scale-110')
                    # Play overlay
                    with ui.element('div').classes(
                        'absolute inset-0 flex items-center justify-center bg-black/0 '
                        'group-hover:bg-black/30 transition-all'
                    ):
                        with ui.element('div').classes(
                            'flex h-12 w-12 scale-0 items-center justify-center rounded-full '
                            'bg-primary text-white transition-transform group-hover:scale-100 shadow-lg'
                        ):
                            ui.icon('play_arrow', size='24px')
                
                # Info
                with ui.column().classes('p-5 gap-1'):
                    ui.label(title).classes('font-display text-base font-bold text-foreground line-clamp-1 group-hover:text-primary transition-colors')
                    ui.label(artist).classes('text-sm text-muted-foreground font-medium')
                    
                    with ui.row().classes('mt-3 flex items-center gap-4 text-[11px] text-muted-foreground font-medium'):
                        with ui.row().classes('items-center gap-1'):
                            ui.icon('music_note', size='14px').classes('text-primary/70')
                            ui.label(melody or t('card_melody_old'))
                        with ui.row().classes('items-center gap-1'):
                            ui.icon('schedule', size='14px').classes('text-primary/70')
                            ui.label(duration or '03:45')

def artist_card(id, name, photo_url, title, index=0):
    with ui.element('div').classes('relative group'):
        _admin_controls('artist', id)
        
        with ui.card().classes(
            'group overflow-hidden rounded-lg border border-border bg-card shadow-card '
            'hover:shadow-elevated transition-all p-0 cursor-pointer w-full'
        ).on('click', lambda: ui.navigate.to(f'/nghe-nhan/{id}')):
            with ui.element('div').classes('relative aspect-square w-full overflow-hidden'):
                ui.image(photo_url).classes('h-full w-full object-cover transition-transform duration-500 group-hover:scale-105')
                with ui.element('div').classes('absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 to-transparent p-4'):
                    ui.label(name).classes('font-display text-lg font-bold text-white')
            
            with ui.column().classes('p-4 gap-2'):
                with ui.row().classes('items-center gap-2 text-sm text-muted-foreground'):
                    ui.icon('place', size='16px').classes('text-primary')
                    ui.label(f'{t("villages")} {title or "Kinh Bắc"}')
                with ui.row().classes('items-center gap-2 text-sm text-muted-foreground'):
                    ui.icon('workspace_premium', size='16px').classes('text-gold')
                    ui.label(f'{12 + index} {t("card_songs")}')

def news_card(id, title, image_url, type=None, date='--/--/----'):
    type_label = t('card_news') if type != 'Sự kiện' else t('card_event')
    target = f'/su-kien/{id}' if type == 'Sự kiện' else f'/tin-tuc/{id}'
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
                ui.image(item.get('image_url') or 'https://images.unsplash.com/photo-1526462981764-f6cf0f4ea260?auto=format&fit=crop&q=80&w=600').classes('h-full w-full object-cover transition-transform duration-500 group-hover:scale-105')
                
                # Badges overlay
                badges = item.get('badges')
                if badges:
                    with ui.row().classes('absolute top-3 left-3 gap-2'):
                        for badge in badges.split(','):
                            ui.label(badge.strip()).classes('bg-primary/90 text-white text-[10px] font-bold px-2 py-1 rounded shadow-sm backdrop-blur-sm')

            # Content
            with ui.column().classes('p-4 gap-2 flex-1'):
                with ui.column().classes('gap-1'):
                    ui.label(item.get('name', 'Làng Quan họ')).classes('font-display text-lg font-bold text-foreground group-hover:text-primary transition-colors cursor-pointer').on('click', lambda id=item.get('id'): ui.navigate.to(f'/lang-quan-ho/{id}'))
                    with ui.row().classes('items-center gap-1.5 text-xs text-muted-foreground'):
                        ui.icon('place', size='14px').classes('text-primary')
                        ui.label(f"Huyện {item.get('district') or 'Kinh Bắc'}")

                ui.label(item.get('description', '')).classes('text-xs text-muted-foreground line-clamp-2 leading-relaxed')

                # Stats & Info
                with ui.row().classes('w-full justify-between items-center bg-muted/30 p-2 rounded-lg border border-border/50'):
                    with ui.column().classes('items-center gap-0'):
                        ui.label(str(item.get('artist_count', 0))).classes('text-base font-bold text-primary')
                        ui.label(t('artists')).classes('text-[9px] uppercase font-bold text-muted-foreground')
                    
                    ui.element('div').classes('w-[1px] h-6 bg-border')
                    
                    with ui.column().classes('flex-1 px-3 gap-0'):
                        ui.label('Làn điệu đặc trưng').classes('text-[9px] uppercase font-bold text-muted-foreground mb-0.5')
                        songs = item.get('featured_songs', 'Đang cập nhật')
                        ui.label(songs).classes('text-[10px] font-medium text-foreground line-clamp-1')

                # Action
                with ui.row().classes('w-full mt-auto pt-1 gap-2'):
                    ui.button(t('card_view_detail'), on_click=lambda id=item.get('id'): ui.navigate.to(f'/lang-quan-ho/{id}')).props('outline color="primary" rounded dense').classes('flex-1 text-[10px] font-bold')
                    if on_map_click:
                        ui.button(t('card_map'), icon='map', on_click=on_map_click).props('unelevated color="primary" rounded dense').classes('flex-1 text-[10px] font-bold')

def news_grid_card(item):
    with ui.element('div').classes('relative group h-full'):
        _admin_controls('news', item.get('id'))
        
        with ui.card().classes('w-full p-0 flex flex-col overflow-hidden hover:shadow-elevated transition-all duration-300 cursor-pointer bg-card border border-border h-full').on('click', lambda id=item.get('id'): ui.navigate.to(f'/tin-tuc/{id}')):
            with ui.element('div').classes('relative w-full aspect-[16/10] overflow-hidden'):
                ui.image(item.get('image_url') or 'https://images.unsplash.com/photo-1599908608021-b5d929aa054e?auto=format&fit=crop&w=800&q=80').classes('w-full h-full object-cover transition-transform duration-700 group-hover:scale-105')
                ui.element('div').classes('absolute inset-0 bg-gradient-to-t from-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none')
                
            with ui.column().classes('p-4 sm:p-5 flex-grow w-full gap-0'):
                with ui.row().classes('justify-between items-center w-full mb-2'):
                    ui.label(item.get('category', 'Tin tức')).classes('text-[9px] font-bold text-primary uppercase tracking-wider bg-primary/10 px-2 py-0.5 rounded-sm')
                    date_str = (item.get('created_at') or '--/--/----')[:10]
                    with ui.row().classes('items-center gap-1 text-muted-foreground'):
                        ui.icon('calendar_today', size='11px')
                        ui.label(date_str).classes('text-[10px] font-medium')
                        
                ui.label(item.get('title', 'Không có tiêu đề')).classes('text-base font-bold font-display line-clamp-2 mb-2 group-hover:text-primary transition-colors leading-snug')
                ui.label(item.get('excerpt') or item.get('description') or 'Đang cập nhật...').classes('text-xs text-muted-foreground line-clamp-2 mb-3 flex-grow')
                
                with ui.row().classes('items-center text-primary mt-auto gap-1 text-sm font-bold opacity-0 -translate-x-2 transition-all duration-300 group-hover:opacity-100 group-hover:translate-x-0'):
                    ui.label('Đọc thêm')
                    ui.icon('arrow_forward', size='16px')

def event_grid_card(item, on_register=None):
    with ui.element('div').classes('relative group h-full'):
        _admin_controls('news', item.get('id'))
        
        with ui.card().classes('w-full p-0 flex flex-col overflow-hidden hover:shadow-elevated transition-all duration-300 bg-card border border-border h-full'):
            with ui.element('div').classes('relative w-full aspect-[16/10] overflow-hidden cursor-pointer').on('click', lambda id=item.get('id'): ui.navigate.to(f'/su-kien/{id}')):
                ui.image(item.get('image_url') or 'https://images.unsplash.com/photo-1526462981764-f6cf0f4ea260?auto=format&fit=crop&w=800&q=80').classes('w-full h-full object-cover transition-transform duration-700 group-hover:scale-105')
                ui.element('div').classes('absolute inset-0 bg-gradient-to-t from-black/50 to-transparent')
                ui.label('Sự kiện').classes('absolute top-3 left-3 text-[10px] font-bold text-white uppercase tracking-wider bg-primary px-2.5 py-1 rounded-sm shadow-md z-10')
                
                # Date overlay
                date_str = (item.get('start_date') or '--/--/----')[:10]
                with ui.row().classes('absolute bottom-3 left-3 items-center gap-1.5 text-white z-10'):
                    ui.icon('event', size='16px')
                    ui.label(date_str).classes('text-sm font-medium drop-shadow-md')

            with ui.column().classes('p-4 sm:p-5 flex-grow w-full gap-0 relative'):
                ui.label(item.get('title', 'Không có tiêu đề')).classes('text-base font-bold font-display line-clamp-2 mb-2 hover:text-primary transition-colors cursor-pointer leading-snug').on('click', lambda id=item.get('id'): ui.navigate.to(f'/su-kien/{id}'))
                
                # Countdown timer
                with ui.row().classes('items-center gap-2 mb-4 bg-primary/5 px-3 py-1.5 rounded-full border border-primary/10 w-fit'):
                    ui.icon('timer', size='14px').classes('text-primary')
                    countdown_label = ui.label('Đang tính toán...').classes('text-[11px] font-bold text-primary uppercase tracking-tighter')
                    
                    def update_countdown(target_date_str=item.get('start_date'), label=countdown_label):
                        if not target_date_str:
                            label.text = "Chưa rõ ngày"
                            return
                        try:
                            # Handle simple date or isoformat
                            if ' ' in target_date_str: target_date_str = target_date_str.split(' ')[0]
                            target_date = datetime.strptime(target_date_str[:10], "%Y-%m-%d")
                            now = datetime.now()
                            diff = target_date - now
                            if diff.total_seconds() <= 0:
                                label.text = "Đang diễn ra"
                            else:
                                d = diff.days
                                h, rem = divmod(diff.seconds, 3600)
                                m, s = divmod(rem, 60)
                                label.text = f"Còn {d}N {h:02}:{m:02}:{s:02}"
                        except:
                            label.text = "Sắp diễn ra"
                    
                    ui.timer(1.0, update_countdown)

                ui.label(item.get('description', '')).classes('text-xs text-muted-foreground line-clamp-2 mb-3')
                
                with ui.column().classes('w-full gap-2 mb-4 bg-muted/30 p-3 rounded-xl border border-border/50'):
                    with ui.row().classes('items-start gap-2 text-xs text-foreground flex-nowrap'):
                        ui.icon('place', size='16px').classes('text-primary mt-0.5 shrink-0')
                        ui.label(item.get('location', 'Tại địa phương')).classes('line-clamp-1 font-medium leading-tight')
                    with ui.row().classes('items-center gap-2 text-xs text-foreground'):
                        ui.icon('group', size='16px').classes('text-primary shrink-0')
                        # Fallback to max_participants if available_slots not provided
                        slots = item.get('available_slots')
                        if slots is None: slots = item.get('max_participants', 100)
                        ui.label(f"Số lượng: Còn {slots} chỗ").classes('font-medium')
                
                is_registered = item.get('is_registered', False)
                btn_text = 'Đã đăng ký' if is_registered else 'Đăng ký tham gia'
                
                btn = ui.button(btn_text, icon='how_to_reg' if not is_registered else 'check_circle').classes('w-full mt-auto py-2.5 rounded-lg font-bold tracking-wide shadow-sm').props(f'color="{"grey" if is_registered else "primary"}" {"disable" if is_registered else ""} unelevated')
                if on_register:
                    btn.on('click', lambda e: on_register(item, btn))

