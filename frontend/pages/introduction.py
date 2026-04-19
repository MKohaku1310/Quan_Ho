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
            'relative min-h-[50vh] md:min-h-[60vh] lg:min-h-[65vh] flex items-center justify-center overflow-hidden w-full'
        ):
            ui.image('/static/home/hero-banner.jpg').classes('absolute inset-0 h-full w-full object-cover object-bottom scale-100')
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
            ui.image('/static/common/lotus-ornament.png').classes(
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
        with ui.element('section').classes('py-36 bg-card w-full relative border-y border-border shadow-inner min-h-[650px]'):
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

                # Horizontal Timeline Layout
                with ui.element('div').classes('relative mt-16 w-full max-w-7xl mx-auto'):
                    # Scrollable Container (Increased bottom padding to ensure no clipping)
                    with ui.element('div').classes('flex flex-row overflow-x-auto gap-0 pb-24 pt-16 px-4 snap-x snap-mandatory hide-scrollbar relative w-full flex-nowrap items-start'):
                        # 1. The Horizontal Axis Line (Fixed relative to the container)
                        ui.element('div').classes('absolute left-0 right-0 top-[48px] h-1 bg-gradient-to-r from-primary/5 via-primary/30 to-primary/5 z-0 min-w-[2000px]')
                        
                        for i, (year, period, text) in enumerate(timeline_data):
                            with ui.element('div').classes('flex-shrink-0 w-[280px] md:w-[340px] snap-center flex flex-col items-center gap-6 relative z-10'):
                                # Dot on line
                                with ui.element('div').classes('w-10 h-10 rounded-full bg-background border-[4px] border-primary/20 flex items-center justify-center shadow-md relative shrink-0'):
                                    ui.element('div').classes('w-3 h-3 rounded-full bg-primary shadow-[0_0_15px_rgba(var(--primary),0.5)]')
                                    ui.element('div').classes('absolute inset-0 rounded-full border border-primary animate-ping opacity-20')
                                
                                # Compact Content Card
                                with ui.card().classes('w-[90%] p-6 bg-card border border-border rounded-3xl shadow-sm hover:shadow-elevated transition-all text-center flex flex-col items-center group relative h-auto min-h-[180px]'):
                                    # Badge for period
                                    ui.label(period).classes('text-[9px] font-bold uppercase tracking-[0.2em] text-muted-foreground mb-3 bg-muted px-3 py-1 rounded-full border border-border/50')
                                    
                                    # Year
                                    ui.label(year).classes('text-2xl font-black text-primary leading-tight mb-2 group-hover:scale-105 transition-transform')
                                    
                                    # Description
                                    ui.label(text).classes('text-xs leading-relaxed text-muted-foreground/80 font-medium whitespace-normal text-justify')
                    
                    # Gradient fades for scroll indication
                    ui.element('div').classes('absolute left-0 top-0 bottom-0 w-24 bg-gradient-to-r from-card via-card/50 to-transparent pointer-events-none z-20')
                    ui.element('div').classes('absolute right-0 top-0 bottom-0 w-24 bg-gradient-to-l from-card via-card/50 to-transparent pointer-events-none z-20')

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
            ui.label(t('costume_tradition')).classes(
                'absolute -right-20 top-20 text-[12vw] font-black text-primary/5 select-none pointer-events-none uppercase'
            )
            with theme.container():
                components.section_title(t('intro_costume'), t('intro_costume_subtitle'))
                with ui.column().classes('mt-12 gap-12 w-full'):
                    components.costume_block(
                        t('costume_lien_chi_title'),
                        t('costume_lien_chi_desc'),
                        '/static/intro/costume_lien_chi.png',
                        items=[t('costume_lien_chi_item1'), t('costume_lien_chi_item2'), t('costume_lien_chi_item3')],
                    )
                    components.costume_block(
                        t('costume_lien_anh_title'),
                        t('costume_lien_anh_desc'),
                        '/static/intro/costume_lien_anh.png',
                        items=[t('costume_lien_anh_item1'), t('costume_lien_anh_item2'), t('costume_lien_anh_item3')],
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
                            ui.image('/static/news/hoi_lim.png').classes('w-full h-full object-cover transition-transform duration-700 group-hover:scale-105')
                        with ui.column().classes('p-6 gap-3'):
                            ui.label(t('intro_hoi_lim_title')).classes('font-display text-2xl font-bold text-foreground group-hover:text-primary transition-colors')
                            ui.label(t('intro_hoi_lim_desc')).classes('text-sm text-muted-foreground leading-relaxed line-clamp-3')

                    # Boating Card
                    with ui.card().classes('group overflow-hidden rounded-2xl border border-border bg-card shadow-sm hover:shadow-elevated transition-all p-0'):
                        with ui.element('div').classes('relative aspect-video w-full overflow-hidden'):
                            ui.image('/static/news/hat_tren_thuyen.png').classes('w-full h-full object-cover transition-transform duration-700 group-hover:scale-105')
                        with ui.column().classes('p-6 gap-3'):
                            ui.label(t('intro_boating_title')).classes('font-display text-2xl font-bold text-foreground group-hover:text-primary transition-colors')
                            ui.label(t('intro_boating_desc')).classes('text-sm text-muted-foreground leading-relaxed line-clamp-3')

        # ── 7. Thư viện ảnh (Masonry + Lightbox) (REFINED) ────────────────────
        with ui.element('section').classes('py-24 bg-card w-full shadow-inner overflow-hidden'):
            with theme.container():
                components.section_title(t('intro_gallery'), t('intro_gallery_subtitle'))
                
                gallery_images = [
                    '/static/gallery/gallery_1.png',
                    '/static/gallery/gallery_2.png',
                    '/static/gallery/gallery_3.png',
                    '/static/gallery/gallery_4.png',
                    '/static/gallery/gallery_5.png',
                    '/static/gallery/gallery_6.png',
                    '/static/gallery/gallery_7.png',
                    '/static/gallery/gallery_8.png'
                ]

                # Bento Grid Layout
                with ui.element('div').classes('mt-12 grid grid-cols-2 md:grid-cols-4 gap-3 sm:gap-4 w-full auto-rows-[150px] md:auto-rows-[200px]'):
                    # Custom spans for a mosaic effect
                    spans = [
                        'col-span-2 row-span-2', # 1
                        'col-span-1 row-span-1', # 2
                        'col-span-1 row-span-2', # 3
                        'col-span-1 row-span-1', # 4
                        'col-span-2 row-span-1', # 5
                        'col-span-1 row-span-1', # 6
                        'col-span-1 row-span-1', # 7
                        'col-span-1 row-span-1', # 8
                    ]
                    
                    for idx, img_url in enumerate(gallery_images):
                        span_class = spans[idx] if idx < len(spans) else 'col-span-1'
                        with ui.element('div').classes(f'{span_class} relative overflow-hidden rounded-2xl cursor-pointer group shadow-sm transition-all hover:shadow-xl').on('click', lambda _, i=idx: open_lightbox(i)):
                            ui.image(img_url).classes('w-full h-full object-cover transition-transform duration-700 group-hover:scale-110')
                            # Glass Overlay
                            with ui.element('div').classes('absolute inset-0 bg-black/40 backdrop-blur-[2px] opacity-0 group-hover:opacity-100 transition-all flex items-center justify-center'):
                                with ui.element('div').classes('p-3 rounded-full bg-white/20 backdrop-blur-md border border-white/30 scale-50 group-hover:scale-100 transition-transform duration-300'):
                                    ui.icon('zoom_in', size='2rem').classes('text-white')

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