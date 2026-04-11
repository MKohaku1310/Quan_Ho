from nicegui import ui
import theme

def song_card(id, title, artist, image_url, melody=None, duration=None):
    with ui.element('div').classes('relative group cursor-pointer').on('click', lambda: ui.navigate.to(f'/bai-hat/{id}')):
        # Favorite button
        with ui.element('div').classes(
            'absolute right-3 top-3 z-10 flex h-8 w-8 items-center justify-center rounded-full '
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
                ui.image(image_url).classes('h-full w-full object-cover transition-transform duration-500 group-hover:scale-110')
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
                        ui.label(melody or 'Làn điệu cổ')
                    with ui.row().classes('items-center gap-1'):
                        ui.icon('schedule', size='14px').classes('text-primary/70')
                        ui.label(duration or '03:45')

def artist_card(id, name, photo_url, title, index=0):
    with ui.card().classes(
        'group overflow-hidden rounded-lg border border-border bg-card shadow-card '
        'hover:shadow-elevated transition-all p-0 cursor-pointer'
    ).on('click', lambda: ui.navigate.to(f'/nghe-nhan/{id}')):
        with ui.element('div').classes('relative aspect-square w-full overflow-hidden'):
            ui.image(photo_url).classes('h-full w-full object-cover transition-transform duration-500 group-hover:scale-105')
            with ui.element('div').classes('absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 to-transparent p-4'):
                ui.label(name).classes('font-display text-lg font-bold text-white')
        
        with ui.column().classes('p-4 gap-2'):
            with ui.row().classes('items-center gap-2 text-sm text-muted-foreground'):
                ui.icon('place', size='16px').classes('text-primary')
                ui.label(f'Làng {title or "Kinh Bắc"}')
            with ui.row().classes('items-center gap-2 text-sm text-muted-foreground'):
                ui.icon('workspace_premium', size='16px').classes('text-gold')
                ui.label(f'{12 + index} bài hát')

def news_card(id, title, image_url, type='Tin tức', date='--/--/----'):
    target = f'/su-kien/{id}' if type == 'Sự kiện' else f'/tin-tuc/{id}'
    with ui.element('div').classes('group relative overflow-hidden'):
        with ui.link(target=target).classes(
            'flex gap-4 rounded-lg border border-border bg-background p-4 shadow-card '
            'transition-all hover:shadow-elevated hover:border-primary/50 no-underline'
        ):
            ui.image(image_url).classes('h-24 w-24 flex-shrink-0 rounded-md object-cover transition-transform duration-500 group-hover:scale-105')
            
            with ui.column().classes('min-w-0 flex-1'):
                ui.label(type).classes('inline-block rounded bg-primary/10 px-2 py-0.5 text-[10px] font-bold text-primary uppercase tracking-wider')
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
        ui.image('/static/lotus-ornament.png').classes(
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
