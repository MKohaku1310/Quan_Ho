from nicegui import ui, app
import theme
import components
from api import api_client
import asyncio
from translation import t, tc

@ui.page('/lang-quan-ho', response_timeout=60.0)
async def villages_page():
    with theme.frame():
        components.page_header(t('villages_title'), t('villages_subtitle'))

        class State:
            def __init__(self):
                self.search_query = ''
                self.district_filter = ''
                self.page = 1
                self.items_per_page = 12
                self.total_count = 0
                self.villages = []
        
        state = State()

        @ui.refreshable
        async def village_list():
            state.total_count = await api_client.get_locations_count(type='lang-quan-ho', district=state.district_filter, search=state.search_query)
            skip = (state.page - 1) * state.items_per_page
            state.villages = await api_client.get_locations(skip=skip, limit=state.items_per_page, type='lang-quan-ho', district=state.district_filter, search=state.search_query)

            if not state.villages:
                components.empty_state(t('no_villages_found'))
                return
            
            with ui.row().classes('grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 w-full'):
                for item in state.villages:
                    components.village_grid_card(item, on_map_click=None)
            
            # Use generic pagination component
            components.pagination_controls(state, state.total_count, village_list)

        with ui.element('section').classes('pt-6 pb-16 bg-background w-full min-h-screen'):
            with theme.container():
                with ui.column().classes('w-full gap-6 mb-8'):
                    with ui.element('div').classes('modern-search-card p-3 gap-4 w-full flex flex-col md:flex-row items-center rounded-2xl border border-border bg-card shadow-sm'):
                        with ui.row().classes('flex-1 w-full items-center gap-4'):
                            search_input = ui.input(
                                placeholder=t('search_village'),
                                on_change=lambda e: (setattr(state, 'search_query', e.value or ''), setattr(state, 'page', 1), village_list.refresh())
                            ).classes('modern-input flex-1 bg-background rounded-lg').props('outlined clearable debounce=500 icon=search')
                            
                            districts = ['All', 'Tiên Du', 'Từ Sơn', 'Yên Phong', 'TP Bắc Ninh']
                            ui.select(
                                {d: (t('all_categories') if d == 'All' else d) for d in districts}, 
                                value='All',
                                on_change=lambda e: (setattr(state, 'district_filter', e.value if e.value != 'All' else ''), setattr(state, 'page', 1), village_list.refresh())
                            ).classes('modern-select w-44 bg-background').props('outlined rounded-lg options-dense')
                        
                        if app.storage.user.get('role') == 'admin':
                            ui.button(t('add_village'), icon='add_location').on('click.stop', lambda: ui.navigate.to('/admin/edit/village/0')).props('unelevated rounded color=primary').classes('font-bold shadow-md shadow-primary/20 whitespace-nowrap px-6 cursor-pointer pointer-events-auto z-50')

                    await village_list()


@ui.page('/lang-quan-ho/{id}')
async def village_detail_page(id: int):
    with theme.frame():
        village = await api_client.get_village(id)
        if not village:
            components.empty_state(t('updating'))
            return

        with ui.element('section').classes('relative w-full bg-background bg-paper-texture min-h-screen overflow-hidden animate-fade-in pb-24'):
            # Cultural decoration (Background)
            ui.image('/static/common/lotus-pattern.png').classes('absolute -right-20 -top-20 w-80 opacity-5 pointer-events-none rotate-12')
            ui.image('/static/common/lotus-pattern.png').classes('absolute -left-20 bottom-20 w-64 opacity-5 pointer-events-none -rotate-12')

            # --- HERO HEADER SECTION ---
            with ui.element('div').classes('relative h-[55dvh] md:h-[65dvh] w-full overflow-hidden shadow-2xl rounded-b-[60px] mb-[-60px] z-10'):
                ui.image(village.get('image_url')).classes('w-full h-full object-cover scale-105 hover:scale-100 transition-transform duration-[20s]')
                # Multi-layer overlay
                ui.element('div').classes('absolute inset-0 bg-gradient-to-t from-background via-black/40 to-transparent opacity-90')
                ui.element('div').classes('absolute inset-0 bg-black/10 mix-blend-overlay')
                
                with theme.container().classes('h-full flex flex-col justify-end pb-32 relative z-50'):
                    # Breadcrumbs (White theme for hero overlay)
                    with ui.row().classes('items-center gap-2 mb-8 text-xs font-black tracking-widest uppercase text-white/70'):
                        ui.link(t('nav_home'), '/').classes('hover:text-primary transition-colors no-underline text-white')
                        ui.label('/')
                        ui.link(t('villages_title'), '/lang-quan-ho').classes('hover:text-primary transition-colors no-underline text-white')
                        ui.label('/')
                        ui.label(tc(village, 'name')).classes('text-white')

                    with ui.row().classes('items-center mb-6 gap-3'):
                        badges = village.get('badges') or t('village_detail_badge')
                        if badges:
                            for badge in badges.split(','):
                                ui.label(badge.strip().upper()).classes('bg-primary/90 text-white text-[10px] font-black px-4 py-1.5 rounded-sm tracking-widest shadow-lg')
                        
                        with ui.row().classes('bg-white/20 backdrop-blur-md px-4 py-1.5 rounded-full border border-white/30'):
                            ui.icon('verified', size='16px', color='white')
                            ui.label(t('heritage_kinh_bac').upper()).classes('text-[10px] text-white font-black tracking-widest')
                    
                    # Village Name with Silk Ribbon Decoration
                    with ui.element('div').classes('relative'):
                        # Silk Ribbon
                        ui.element('div').classes('absolute -left-6 -top-2 h-10 w-48 bg-hero-gradient rotate-[-2deg] transform z-[-1] shadow-lg rounded-r-lg opacity-80')
                        
                        village_name = tc(village, 'name') or t('updating')
                        ui.label(village_name).classes('font-display text-5xl md:text-8xl lg:text-9xl font-black text-white mb-6 drop-shadow-2xl tracking-tighter leading-tight')
                    
                    with ui.row().classes('gap-10 text-white/90'):
                        with ui.row().classes('items-center gap-4 group cursor-default'):
                            with ui.element('div').classes('p-3 bg-primary rounded-2xl shadow-xl ring-4 ring-white/10'):
                                ui.icon('location_on', size='28px', color='white')
                            with ui.column().classes('gap-0'):
                                ui.label(t('village_district_prefix')).classes('text-[10px] font-black uppercase opacity-60 tracking-widest')
                                district = village.get('district') or 'Kinh Bắc'
                                ui.label(district).classes('text-2xl font-black')
                        
                        with ui.row().classes('items-center gap-4 group cursor-default'):
                            with ui.element('div').classes('p-3 bg-white/20 backdrop-blur-md rounded-2xl shadow-xl ring-4 ring-white/10'):
                                ui.icon('group', size='28px', color='white')
                            with ui.column().classes('gap-0'):
                                ui.label(t('artists')).classes('text-[10px] font-black uppercase opacity-60 tracking-widest')
                                ui.label(f"{village.get('artist_count', 0)}").classes('text-2xl font-black')

            # --- MAIN CONTENT SECTION ---
            with ui.element('div').classes('w-full bg-paper-texture relative'):
                # Decorative top Divider
                ui.element('div').classes('absolute top-0 left-0 right-0 h-24 bg-gradient-to-b from-background to-transparent z-0')
                
                with theme.container().classes('py-20 relative z-10'):
                    with ui.row().classes('grid grid-cols-1 lg:grid-cols-12 gap-16 w-full items-start'):
                        
                        # --- LEFT: MAIN INFO (8 Cols) ---
                        with ui.column().classes('lg:col-span-8 gap-12'):
                            # About Section
                            with ui.column().classes('gap-6 w-full'):
                                with ui.row().classes('items-center gap-4'):
                                    ui.element('div').classes('h-10 w-1 bg-primary rounded-full')
                                    ui.label(t('village_intro_title')).classes('text-4xl font-display font-black text-foreground tracking-tight')
                                
                                ui.html(tc(village, 'description')).classes('text-xl leading-[1.8] text-foreground/80 text-justify font-light')
                            
                            # Detail Cards Grid
                            with ui.row().classes('grid grid-cols-1 md:grid-cols-2 gap-8 w-full'):
                                # History Card
                                with ui.card().classes('p-8 rounded-3xl glass-card border-none shadow-elevated group relative overflow-hidden'):
                                    with ui.element('div').classes('absolute -right-6 -top-6 opacity-[0.03] group-hover:opacity-[0.08] transition-opacity'):
                                        ui.icon('history_edu', size='10rem')
                                    with ui.row().classes('items-center gap-3 mb-4'):
                                        ui.icon('history_edu', size='32px', color='primary').classes('drop-shadow-sm')
                                        ui.label(t('village_history_title')).classes('text-2xl font-bold font-display tracking-tight')
                                    ui.html(tc(village, 'history') or t('updating')).classes('text-muted-foreground leading-relaxed text-base font-medium')
                                
                                # Culture Card
                                with ui.card().classes('p-8 rounded-3xl glass-card border-none shadow-elevated group relative overflow-hidden'):
                                    with ui.element('div').classes('absolute -right-6 -top-6 opacity-[0.03] group-hover:opacity-[0.08] transition-opacity'):
                                        ui.icon('auto_awesome', size='10rem')
                                    with ui.row().classes('items-center gap-3 mb-4'):
                                        ui.icon('auto_awesome', size='32px', color='primary').classes('drop-shadow-sm')
                                        ui.label(t('village_culture_title')).classes('text-2xl font-bold font-display tracking-tight')
                                    ui.html(tc(village, 'culture') or t('updating')).classes('text-muted-foreground leading-relaxed text-base font-medium')

                            # Featured Melodies Segment
                            with ui.column().classes('w-full p-10 rounded-[2.5rem] bg-white/40 backdrop-blur-sm border border-primary/10 shadow-inner relative overflow-hidden'):
                                # Lotus Watermark
                                ui.image('/static/common/lotus-ornament.png').classes('absolute -bottom-10 -right-10 w-48 opacity-[0.05] pointer-events-none')
                                
                                ui.label(t('village_melodies_title')).classes('text-xs font-black uppercase tracking-[0.3em] text-primary/60 mb-6 text-center w-full')
                                with ui.row().classes('justify-center gap-4 w-full wrap'):
                                    featured_songs = village.get('featured_songs') or t('updating')
                                    for song in featured_songs.split(','):
                                        with ui.element('div').classes('group cursor-pointer'):
                                            ui.label(song.strip()).classes('bg-white px-8 py-3 rounded-2xl text-foreground font-bold border border-primary/5 shadow-sm hover:shadow-primary/20 hover:border-primary/40 hover:-translate-y-1 transition-all duration-300')

                        # --- RIGHT: SIDEBAR (4 Cols) ---
                        with ui.column().classes('lg:col-span-4 gap-10 w-full sticky top-32'):
                            
                            # Location Box
                            with ui.card().classes('w-full p-8 rounded-[2rem] glass-card border-none shadow-elevated transition-transform hover:rotate-1 duration-500'):
                                with ui.row().classes('items-center justify-between mb-6'):
                                    with ui.row().classes('items-center gap-3'):
                                        ui.icon('map', size='28px', color='primary')
                                        ui.label(t('village_location_title')).classes('text-xl font-bold font-display')
                                    ui.icon('explore', size='24px').classes('text-primary opacity-20 animate-spin-slow')
                                
                                # Enhanced Map Logic with Fallback Query
                                import urllib.parse
                                lat = village.get('latitude')
                                lng = village.get('longitude')
                                district = village.get('district') or 'Kinh Bắc'
                                name = tc(village, 'name')
                                addr = tc(village, 'address')
                                
                                # Sanitize coords
                                try:
                                    lat_val = float(lat) if lat else 0
                                    lng_val = float(lng) if lng else 0
                                except:
                                    lat_val, lng_val = 0, 0
                                
                                # Prepare search query for fallback or button
                                search_query_raw = f"{name}, {district}, Bắc Ninh, Vietnam"
                                search_query_encoded = urllib.parse.quote(search_query_raw)
                                
                                # Determine source: Coords if available, else Search Query
                                if lat_val != 0 and lng_val != 0:
                                    src = f"https://maps.google.com/maps?q={lat_val},{lng_val}&output=embed&z=15"
                                    link_url = f"https://www.google.com/maps/search/?api=1&query={lat_val},{lng_val}"
                                else:
                                    src = f"https://maps.google.com/maps?q={search_query_encoded}&output=embed&z=14"
                                    link_url = f"https://www.google.com/maps/search/?api=1&query={search_query_encoded}"
                                
                                # Embed the Map (Always visible now, with fixed height container)
                                with ui.element('div').classes('w-full h-[320px] rounded-3xl overflow-hidden border border-primary/10 shadow-inner group relative bg-muted/10'):
                                    ui.element('iframe').props(f'src="{src}" width="100%" height="320" style="border:0;" allowfullscreen loading="lazy"')
                                    # Glassy hint overlay on hover
                                    with ui.element('div').classes('absolute inset-0 bg-primary/5 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none flex items-center justify-center'):
                                        ui.icon('zoom_in', size='3rem', color='white').classes('opacity-40')

                                # Action Button
                                with ui.link(target=link_url).classes('w-full mt-6 elevated-btn py-4 bg-primary text-white rounded-2xl flex items-center justify-center gap-3 no-underline shadow-lg shadow-primary/20'):
                                    ui.icon('directions', size='20px')
                                    ui.label(t('village_open_maps')).classes('text-sm font-black uppercase tracking-widest')

                            # Explore More Sidebar Card
                            with ui.card().classes('w-full p-8 rounded-[2rem] glass-card border-none shadow-elevated relative overflow-hidden'):
                                # Background decorative circle
                                ui.element('div').classes('absolute -right-10 -bottom-10 w-40 h-40 bg-primary/5 rounded-full')
                                
                                ui.label(t('village_explore_more')).classes('text-2xl font-display font-black text-foreground mb-8 text-center w-full')
                                
                                with ui.column().classes('w-full gap-4'):
                                    # Navigation links
                                    for label, icon, path in [
                                        (t('village_artists'), 'groups', '/nghe-nhan'),
                                        (t('village_melodies'), 'library_music', '/bai-hat')
                                    ]:
                                        with ui.row().classes('w-full items-center justify-between p-4 bg-white/50 hover:bg-primary hover:text-white rounded-2xl border border-primary/5 cursor-pointer group transition-all duration-500').on('click', lambda p=path: ui.navigate.to(p)):
                                            with ui.row().classes('items-center gap-4'):
                                                with ui.element('div').classes('p-2 bg-primary/10 group-hover:bg-white/20 rounded-xl transition-colors'):
                                                    ui.icon(icon, size='24px').classes('text-primary group-hover:text-white')
                                                ui.label(label).classes('font-bold tracking-tight')
                                            ui.icon('chevron_right', size='24px').classes('group-hover:translate-x-1 transition-transform')

                # --- BOTTOM NAVIGATION ---
                with theme.container().classes('pb-24 pt-12 border-t border-primary/5 mt-12'):
                    with ui.row().classes('w-full items-center justify-between'):
                        ui.button(t('village_previous'), icon='arrow_back', on_click=lambda: ui.navigate.to(f'/lang-quan-ho/{max(1, id-1)}')).props('flat rounded-xl color="primary"').classes('font-black text-sm px-6 h-14 bg-white/40 hover:bg-white elevated-btn uppercase tracking-widest')
                        
                        ui.button(on_click=lambda: ui.navigate.to('/lang-quan-ho')).props('flat round icon="apps" color="primary"').classes('scale-150 elevated-btn bg-white/60 shadow-md ring-4 ring-primary/5')
                        
                        ui.button(t('village_next'), icon='arrow_forward', on_click=lambda: ui.navigate.to(f'/lang-quan-ho/{id+1}')).props('flat rounded-xl color="primary" icon-right="arrow_forward"').classes('font-black text-sm px-6 h-14 bg-white/40 hover:bg-white elevated-btn uppercase tracking-widest')