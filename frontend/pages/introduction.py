from nicegui import ui, app
import theme
import components
from translation import t
import asyncio

@ui.page('/gioi-thieu')
def introduction_page():
    with theme.frame():

        # ── 1. Hero Section ────────────────────────────────────────────────────
        with ui.element('section').classes(
            'relative min-h-[70vh] md:min-h-[85vh] flex items-center justify-center overflow-hidden w-full'
        ).style('padding-top: 56px;'):
            ui.image('/static/hero-banner.jpg').classes('absolute inset-0 h-full w-full object-cover object-center scale-100 animate-slow-zoom')
            ui.element('div').classes('absolute inset-0 bg-hero-gradient opacity-60')
            with ui.column().classes('relative z-10 text-center items-center px-4 gap-4'):
                ui.label(t('intro_hero_desc')).classes(
                    'text-[10px] md:text-sm font-bold tracking-[0.5em] text-gold-light uppercase animate-fade-in'
                )
                with ui.column().classes('gap-1 animate-fade-in-up'):
                    ui.label(t('intro_title')).classes('font-display text-2xl md:text-3xl font-medium text-white/80')
                    ui.label(t('intro_subtitle')).classes('font-display text-5xl md:text-8xl font-black text-gradient-gold drop-shadow-2xl mb-4')
                ui.button(t('explore_now'), on_click=lambda: ui.run_javascript('window.scrollTo({top: window.innerHeight, behavior: "smooth"})')).props('unelevated rounded-full').classes('bg-primary text-white font-bold px-8 py-3 shadow-lg hover:bg-crimson-light transition-all')

        # ── 2. About + Features Section (KEPT FROM ORIGINAL) ───────────────────
        with ui.element('section').classes('py-20 bg-background w-full relative overflow-hidden'):
            ui.image('/static/lotus-ornament.png').classes(
                'absolute -left-20 -top-20 w-64 h-64 opacity-[0.03] rotate-12 pointer-events-none'
            )
            with theme.container():
                components.section_title(t('intro_what_is'))
                with ui.column().classes('max-w-4xl mx-auto text-center items-center gap-6 mb-16'):
                    ui.label(t('intro_desc_1')).classes('text-muted-foreground text-base md:text-lg leading-relaxed font-light')
                    ui.label(t('intro_desc_2')).classes('bg-primary/5 px-4 py-3 rounded-xl border border-primary/10 text-foreground italic text-xs md:text-sm')

                with ui.row().classes('grid gap-6 md:grid-cols-3 w-full items-stretch'):
                    components.intro_feature_card('music_note', t('intro_feature_1_title'), t('intro_feature_1_desc'))
                    components.intro_feature_card('groups', t('intro_feature_2_title'), t('intro_feature_2_desc'))
                    components.intro_feature_card('favorite', t('intro_feature_3_title'), t('intro_feature_3_desc'))

        # ── 3. Nguồn gốc lịch sử (NEW ENHANCED TIMELINE) ───────────────────────
        with ui.element('section').classes('py-24 bg-card w-full relative overflow-hidden border-y border-border shadow-inner'):
            ui.label('HISTORY').classes('absolute -left-20 top-20 text-[15vw] font-black text-primary/[0.03] select-none pointer-events-none uppercase')
            with theme.container():
                components.section_title(t('intro_history'), t('intro_history_subtitle'))
                
                timeline_data = [
                    (t('intro_timeline_1_year'), t('intro_timeline_1_period'), t('intro_timeline_1_text')),
                    (t('intro_timeline_2_year'), t('intro_timeline_2_period'), t('intro_timeline_2_text')),
                    (t('intro_timeline_3_year'), t('intro_timeline_3_period'), t('intro_timeline_3_text')),
                    (t('intro_timeline_4_year'), t('intro_timeline_4_period'), t('intro_timeline_4_text')),
                    (t('intro_timeline_5_year'), t('intro_timeline_5_period'), t('intro_timeline_5_text'))
                ]

                with ui.element('div').classes('relative mt-12 w-full max-w-5xl mx-auto'):
                    # 1. The Central Axis Line
                    ui.element('div').classes('absolute left-1/2 -translate-x-1/2 top-0 bottom-0 w-1 bg-primary/30 z-0 hidden md:block')
                    
                    for i, (year, period, text) in enumerate(timeline_data):
                        # Side logic: 0, 2 -> Left; 1, 3 -> Right
                        is_left = (i % 2 == 0)
                        
                        with ui.element('div').classes('grid grid-cols-1 md:grid-cols-[1fr_80px_1fr] items-center mb-0 w-full relative z-10'):
                            if is_left:
                                # Row i (Even): Card in Col 1, Dot in Col 2, Spacer in Col 3
                                with ui.element('div').classes('flex justify-end pr-8 md:pr-4'):
                                    with ui.card().classes('w-full md:max-w-[380px] p-4 bg-card border border-border rounded-xl shadow-sm hover:shadow-md transition-all text-right items-end'):
                                        ui.label(year).classes('text-lg font-black text-primary leading-tight')
                                        ui.label(period).classes('text-[8px] font-bold uppercase tracking-widest text-muted-foreground mb-1 bg-muted px-2 py-0.5 rounded')
                                        ui.label(text).classes('text-xs leading-relaxed text-muted-foreground/90')
                                
                                with ui.element('div').classes('hidden md:flex justify-center items-center'):
                                    with ui.element('div').classes('w-8 h-8 rounded-full bg-background border-[3px] border-primary flex items-center justify-center shadow-sm'):
                                        ui.element('div').classes('w-1.5 h-1.5 rounded-full bg-primary animate-pulse')
                                
                                ui.element('div').classes('hidden md:block')
                            else:
                                # Row i (Odd): Spacer in Col 1, Dot in Col 2, Card in Col 3
                                ui.element('div').classes('hidden md:block')
                                
                                with ui.element('div').classes('hidden md:flex justify-center items-center'):
                                    with ui.element('div').classes('w-8 h-8 rounded-full bg-background border-[3px] border-primary flex items-center justify-center shadow-sm'):
                                        ui.element('div').classes('w-1.5 h-1.5 rounded-full bg-primary animate-pulse')
                                
                                with ui.element('div').classes('flex justify-start pl-8 md:pl-4'):
                                    with ui.card().classes('w-full md:max-w-[380px] p-4 bg-card border border-border rounded-xl shadow-sm hover:shadow-md transition-all text-left items-start'):
                                        ui.label(year).classes('text-lg font-black text-primary leading-tight')
                                        ui.label(period).classes('text-[8px] font-bold uppercase tracking-widest text-muted-foreground mb-1 bg-muted px-2 py-0.5 rounded')
                                        ui.label(text).classes('text-xs leading-relaxed text-muted-foreground/90')

        # ── 4. Đặc trưng nghệ thuật (NEW ACCORDION) ───────────────────────────
        with ui.element('section').classes('py-24 bg-background w-full'):
            with theme.container():
                components.section_title(t('intro_arts'), t('intro_arts_subtitle'))
                
                with ui.column().classes('max-w-4xl mx-auto mt-12 gap-4 w-full'):
                    with ui.expansion(t('intro_art_1_title'), icon='mic_external_on').classes('w-full bg-card border border-border rounded-2xl overflow-hidden shadow-sm'):
                        with ui.column().classes('p-6 gap-4'):
                            with ui.row().classes('grid grid-cols-1 md:grid-cols-2 gap-6'):
                                with ui.column().classes('gap-2'):
                                    ui.label(t('intro_art_1_vang_ren_title')).classes('font-bold text-primary text-xs tracking-widest uppercase')
                                    ui.label(t('intro_art_1_vang_ren_desc')).classes('text-sm text-muted-foreground')
                                with ui.column().classes('gap-2'):
                                    ui.label(t('intro_art_1_nen_nay_title')).classes('font-bold text-primary text-xs tracking-widest uppercase')
                                    ui.label(t('intro_art_1_nen_nay_desc')).classes('text-sm text-muted-foreground')

                    with ui.expansion(t('intro_art_2_title'), icon='groups_3').classes('w-full bg-card border border-border rounded-2xl overflow-hidden shadow-sm'):
                        ui.label(t('intro_art_2_desc')).classes('p-6 text-sm text-muted-foreground leading-relaxed')

                    with ui.expansion(t('intro_art_3_title'), icon='handshake').classes('w-full bg-card border border-border rounded-2xl overflow-hidden shadow-sm'):
                        ui.label(t('intro_art_3_desc')).classes('p-6 text-sm text-muted-foreground leading-relaxed')

        # ── 5. Costume Section (KEPT FROM ORIGINAL) ───────────────────────────
        with ui.element('section').classes('py-24 bg-card/50 border-y border-border w-full relative overflow-hidden'):
            ui.label('TRUYỀN THỐNG').classes(
                'absolute -right-20 top-20 text-[12vw] font-black text-primary/5 select-none pointer-events-none uppercase'
            )
            with theme.container():
                components.section_title(t('intro_costume'), 'Nét đặc trưng làm nên linh hồn của dân ca Quan họ.')
                with ui.column().classes('mt-12 gap-12 w-full'):
                    components.costume_block(
                        t('Trang phục Liền chị'),
                        t('Nổi bật với áo mớ ba mớ bảy, nón quai thao thắt dải lụa thướt tha mang vẻ đẹp dịu dàng kiêu sa đặc trưng của người con gái Kinh Bắc.'),
                        '/static/costume_lien_chi.png',
                        items=[t('Áo mớ ba mớ bảy (Silk layers)'), t('Nón quai thao (Palm hat)'), t('Khăn mỏ quạ (Headscarf)')],
                    )
                    components.costume_block(
                        t('Trang phục Liền anh'),
                        t('Đậm chất nam nhi Kinh Bắc với áo the đen, quần lụa trắng, khăn xếp và chiếc ô đen che nghiêng thể hiện phong thái thanh lịch.'),
                        '/static/costume_lien_anh.png',
                        items=[t('Áo the thâm (Black robe)'), t('Khăn xếp (Layered wrap)'), t('Ô đen (Traditional umbrella)')],
                        reverse=True,
                    )

        # ── 6. Không gian văn hóa (REFINED GRID) ──────────────────────────────
        with ui.element('section').classes('py-24 bg-background w-full overflow-hidden'):
            with theme.container():
                components.section_title(t('intro_spaces'), t('intro_spaces_desc'))
                
                with ui.element('div').classes('mt-12 grid grid-cols-1 md:grid-cols-2 gap-8 w-full'):
                    # Hoi Lim Card
                    with ui.card().classes('group overflow-hidden rounded-2xl border border-border bg-card shadow-sm hover:shadow-elevated transition-all p-0'):
                        with ui.element('div').classes('relative aspect-video w-full overflow-hidden'):
                            ui.image('/static/hoi_lim.png').classes('w-full h-full object-cover transition-transform duration-700 group-hover:scale-105')
                        with ui.column().classes('p-6 gap-3'):
                            ui.label(t('intro_hoi_lim_title')).classes('font-display text-2xl font-bold text-foreground group-hover:text-primary transition-colors')
                            ui.label(t('intro_hoi_lim_desc')).classes('text-sm text-muted-foreground leading-relaxed line-clamp-3')

                    # Boating Card
                    with ui.card().classes('group overflow-hidden rounded-2xl border border-border bg-card shadow-sm hover:shadow-elevated transition-all p-0'):
                        with ui.element('div').classes('relative aspect-video w-full overflow-hidden'):
                            ui.image('/static/hat_tren_thuyen.png').classes('w-full h-full object-cover transition-transform duration-700 group-hover:scale-105')
                        with ui.column().classes('p-6 gap-3'):
                            ui.label(t('intro_boating_title')).classes('font-display text-2xl font-bold text-foreground group-hover:text-primary transition-colors')
                            ui.label(t('intro_boating_desc')).classes('text-sm text-muted-foreground leading-relaxed line-clamp-3')

        # ── 7. Thư viện ảnh (Masonry + Lightbox) (REFINED) ────────────────────
        with ui.element('section').classes('py-24 bg-card w-full shadow-inner overflow-hidden'):
            with theme.container():
                components.section_title(t('intro_gallery'), t('intro_gallery_subtitle'))
                
                gallery_images = [
                    '/static/gallery_1.png',
                    '/static/gallery_2.png',
                    '/static/gallery_3.png',
                    '/static/gallery_4.png',
                    '/static/gallery_5.png',
                    '/static/gallery_6.png',
                    '/static/gallery_7.png',
                    '/static/gallery_8.png'
                ]

                with ui.element('div').classes('mt-12 w-full columns-2 md:columns-3 lg:columns-4 xl:columns-5 gap-4 space-y-4'):
                    for idx, img_url in enumerate(gallery_images):
                        with ui.element('div').classes('break-inside-avoid relative overflow-hidden rounded-2xl cursor-pointer group shadow-sm').on('click', lambda _, i=idx: open_lightbox(i)):
                            ui.image(img_url).classes('w-full h-auto object-cover transition-transform duration-500 group-hover:scale-110')
                            with ui.element('div').classes('absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center'):
                                ui.icon('zoom_in', size='3rem').classes('text-white')

        # Lightbox State (Simplified to avoid next_index error in some NiceGUI versions)
        state = {'index': 0}

        @ui.refreshable
        def lightbox_content():
            ui.image(gallery_images[state['index']]).classes('max-w-full max-h-[85vh] object-contain shadow-2xl animate-fade-in')

        with ui.dialog().classes('w-full h-full max-w-none') as lightbox:
            with ui.element('div').classes('fixed inset-0 bg-black/95 flex items-center justify-center p-4 md:p-12'):
                ui.button(icon='chevron_left', on_click=lambda: open_lightbox((state['index'] - 1) % len(gallery_images))).props('flat round size="2rem"').classes('absolute left-4 md:left-12 text-white z-50 hover:bg-white/10')
                lightbox_content()
                ui.button(icon='chevron_right', on_click=lambda: open_lightbox((state['index'] + 1) % len(gallery_images))).props('flat round size="2rem"').classes('absolute right-4 md:right-12 text-white z-50 hover:bg-white/10')
                ui.button(icon='close', on_click=lightbox.close).props('flat round size="2rem"').classes('absolute top-4 right-4 md:top-12 md:right-12 text-white hover:bg-white/10 z-50')
                
                # Counter label that updates on refresh
                with ui.element('div').classes('absolute bottom-8 left-1/2 -translate-x-1/2 text-white/50 text-sm font-bold tracking-widest uppercase'):
                    ui.label(f"{state['index'] + 1} / {len(gallery_images)}")

        def open_lightbox(index):
            state['index'] = index
            lightbox_content.refresh()
            lightbox.open()

        # ── 8. Video Section (SONG STYLE) ───────────────────────────────────
        with ui.element('section').classes('py-24 bg-background w-full overflow-hidden'):
            with theme.container():
                components.section_title(t('intro_videos'), t('intro_videos_desc'))
                
                videos = [
                    {
                        'title': t('intro_vid_1_title'),
                        'url': 'https://www.youtube.com/watch?v=5U7z0Zc8B2A',
                        'thumb': 'https://img.youtube.com/vi/5U7z0Zc8B2A/hqdefault.jpg'
                    },
                    {
                        'title': t('intro_vid_2_title'),
                        'url': 'https://www.youtube.com/watch?v=9NfB8kbeUyk',
                        'thumb': 'https://img.youtube.com/vi/9NfB8kbeUyk/hqdefault.jpg'
                    }
                ]

                with ui.row().classes('grid grid-cols-1 lg:grid-cols-2 gap-8 mt-12 w-full'):
                    for vid in videos:
                        with ui.card().classes('overflow-hidden rounded-xl border border-border bg-card shadow-lg p-0 w-full group cursor-pointer').on(
                            'click', lambda v=vid['url']: ui.run_javascript(f'window.open("{v}", "_blank")')
                        ):
                            with ui.element('div').classes('relative w-full aspect-video'):
                                ui.image(vid['thumb']).classes('w-full h-full object-cover transition-transform duration-700 group-hover:scale-105')
                                # Play overlay
                                with ui.element('div').classes('absolute inset-0 flex flex-col items-center justify-center gap-4 bg-black/40 group-hover:bg-black/30 transition-colors'):
                                    with ui.element('div').classes('flex h-16 w-16 items-center justify-center rounded-full bg-primary text-white shadow-xl transition-transform group-hover:scale-110'):
                                        ui.icon('play_arrow', size='36px')
                                    ui.label(vid['title']).classes('text-white text-sm font-bold drop-shadow-md')

        # ── 9. Quote Section (UNESCO) ────────────────────────────────────────
        with ui.element('section').classes('py-24 bg-card border-t border-border w-full relative overflow-hidden'):
            with theme.container().classes('max-w-4xl text-center items-center relative z-10'):
                components.unesco_quote(
                    t('intro_quote'),
                    subtitle=t('intro_quote_sub')
                )