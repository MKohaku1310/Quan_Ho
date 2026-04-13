import json
from nicegui import ui, app
import theme
import components
from api import api_client
import asyncio

# Tài sản Leaflet và Logic khởi tạo
LEAFLET_CSS = '<link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/>'
LEAFLET_JS = '<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>'
LEAFLET_POPUP_STYLE = '''
    <style>
        .leaflet-popup-content-wrapper { border-radius: 12px; padding: 0; overflow: hidden; }
        .leaflet-popup-content { margin: 0; width: 200px !important; }
    </style>
'''

LEAFLET_INIT_JS = '''
    window.map;
    window.markers = {};
    
    window.initMap = function() {
        if (typeof L === 'undefined') return setTimeout(window.initMap, 500);
        var mapElement = document.getElementById("map");
        if (!mapElement) return;
        if (window.map) {
            window.map.invalidateSize();
            return;
        }
        
        // Sử dụng Google Maps Tiles cho giao diện quen thuộc
        window.map = L.map("map", {
            zoomControl: true,
            scrollWheelZoom: true
        }).setView([21.1861, 106.0763], 11);
        
        L.tileLayer('https://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
            maxZoom: 20,
            subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
            attribution: 'Map data &copy; Google'
        }).addTo(window.map);
    };
    
    window.addMarker = function(id, lat, lng, name, image, description) {
        if (!window.map) window.initMap();
        if (window.markers[id]) window.map.removeLayer(window.markers[id]);
        
        var popupContent = `
            <div style="font-family: sans-serif;">
                <img src="${image}" style="width: 100%; height: 100px; object-fit: cover; border-bottom: 1px solid #eee">
                <div style="padding: 12px">
                    <h3 style="margin: 0 0 4px; font-size: 14px; font-weight: bold; color: #8B0000">${name}</h3>
                    <p style="margin: 0 0 10px; font-size: 11px; color: #666; line-height: 1.4">${description}</p>
                    <button onclick="window.location.href='/lang-quan-ho/${id}'" style="width: 100%; padding: 8px; background: #8B0000; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 11px; font-weight: bold; transition: opacity 0.2s;" onmouseover="this.style.opacity=0.8" onmouseout="this.style.opacity=1">Xem chi tiết</button>
                </div>
            </div>
        `;
        
        var marker = L.marker([lat, lng]).addTo(window.map).bindPopup(popupContent);
        window.markers[id] = marker;
    };
    
    window.focusMarker = function(id) {
        var marker = window.markers[id];
        if (marker) {
            window.map.setView(marker.getLatLng(), 15);
            marker.openPopup();
        }
    };
    
    window.clearMarkers = function() {
        if (!window.map) return;
        for (var id in window.markers) {
            window.map.removeLayer(window.markers[id]);
        }
        window.markers = {};
    };
'''

@ui.page('/lang-quan-ho', response_timeout=60.0)
async def villages_page():
    # Chèn tài sản Leaflet head ngoài frame context để tránh lỗi 500
    ui.add_head_html(LEAFLET_CSS)
    ui.add_head_html(LEAFLET_JS)
    ui.add_head_html(LEAFLET_POPUP_STYLE)
    ui.add_body_html(f'<script>{LEAFLET_INIT_JS}</script>')
    
    with theme.frame():
        # Hero section
        components.page_header('49 Làng Quan họ gốc', 'Khám phá không gian văn hóa di sản tại quê hương Quan họ')

        # ... (phần còn lại của logic state và fetching giữ nguyên)
        class State:
            def __init__(self, items):
                self.all_items = items
                self.filtered_items = items
                self.search_query = ''
                self.district_filter = 'Tất cả'
                self.page = 1
                self.items_per_page = 12
                self.view_tab = 'list'

        # Lấy dữ liệu với xử lý lỗi
        try:
            villages = await api_client.get_villages()
        except Exception as e:
            print(f"Error in villages_page: {e}")
            villages = []
            
        if not villages:
            villages = []
        
        state = State(villages)

        def update_markers():
            ui.run_javascript('window.clearMarkers();')
            for v in state.filtered_items:
                lat, lng = v.get('latitude'), v.get('longitude')
                name = v.get('name', '').replace('"', '\\"')
                desc = (v.get('description', '')[:80] + '...').replace('"', '\\"')
                img = v.get('image_url', '')
                if lat and lng:
                    ui.run_javascript(f'window.addMarker({v["id"]}, {lat}, {lng}, "{name}", "{img}", "{desc}")')

        @ui.refreshable
        def village_list():
            if not state.filtered_items:
                components.empty_state('Không tìm thấy làng nào phù hợp.')
                return
            
            start = (state.page - 1) * state.items_per_page
            end = start + state.items_per_page
            page_items = state.filtered_items[start:end]
            
            with ui.row().classes('grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 w-full'):
                for item in page_items:
                    components.village_grid_card(item, on_map_click=None)
            
            # UI phân trang
            total_pages = (len(state.filtered_items) + state.items_per_page - 1) // state.items_per_page
            if total_pages > 1:
                with ui.row().classes('w-full justify-center mt-12 gap-2 pb-8'):
                    ui.button(icon='chevron_left', on_click=lambda: (setattr(state, 'page', max(1, state.page-1)), village_list.refresh())).props('flat round dense').classes('text-primary')
                    for p in range(1, total_pages + 1):
                        ui.button(str(p), on_click=lambda p=p: (setattr(state, 'page', p), village_list.refresh())).props(f'flat round dense {"color=primary shadow-md bg-primary/10" if p == state.page else "color=grey"}').classes('font-bold text-sm')
                    ui.button(icon='chevron_right', on_click=lambda: (setattr(state, 'page', min(total_pages, state.page+1)), village_list.refresh())).props('flat round dense').classes('text-primary')

        def apply_filters():
            q = state.search_query.lower()
            d = state.district_filter
            state.filtered_items = [
                v for v in state.all_items
                if (q in v.get('name', '').lower() or q in v.get('description', '').lower()) 
                and (d == 'Tất cả' or v.get('district') == d)
            ]
            state.page = 1
            village_list.refresh()
            update_markers()

        with ui.element('section').classes('pt-6 pb-16 bg-background w-full min-h-screen'):
            with theme.container():
                # Header Bộ lọc & Tab
                with ui.column().classes('w-full gap-6 mb-8'):
                    # Thanh điều khiển
                    with ui.element('div').classes('modern-search-card p-3 gap-4 w-full flex flex-col md:flex-row items-center rounded-2xl border border-border bg-card shadow-sm'):
                        with ui.row().classes('flex-1 w-full items-center gap-4'):
                            search_input = ui.input(placeholder='Tìm làng...').classes('modern-input flex-1 bg-background rounded-lg').props('outlined dense clearable debounce=500 icon=search')
                            search_input.on('update:model-value', lambda e: (setattr(state, 'search_query', e or ''), apply_filters()))
                            
                            districts = ['Tất cả', 'Tiên Du', 'Từ Sơn', 'Yên Phong', 'TP Bắc Ninh']
                            district_select = ui.select(districts, value='Tất cả').classes('modern-select w-44 bg-background').props('outlined dense rounded-lg options-dense')
                            district_select.on('update:model-value', lambda e: (setattr(state, 'district_filter', e or 'Tất cả'), apply_filters()))
                        
                        if app.storage.user.get('role') == 'admin':
                            ui.button('THÊM LÀNG', icon='add_location', on_click=lambda: ui.navigate.to('/admin/edit/village/0')).props('unelevated rounded color=primary').classes('font-bold shadow-md shadow-primary/20 whitespace-nowrap px-6')

                    # Các tab
                    with ui.tabs().classes('w-full border-b border-border') as tabs:
                        list_tab = ui.tab('list', label='DANH SÁCH', icon='grid_view').classes('px-8 font-bold text-sm tracking-widest')
                        map_tab = ui.tab('map', label='BẢN ĐỒ', icon='map').classes('px-8 font-bold text-sm tracking-widest')

                # Các Panel Tab
                with ui.tab_panels(tabs, value='list').classes('w-full bg-transparent overflow-visible') as panels:
                    with ui.tab_panel('list').classes('p-0'):
                        village_list()
                    
                    with ui.tab_panel('map').classes('p-0'):
                        with ui.card().classes('relative w-full h-[600px] p-0 rounded-2xl border border-border shadow-lg overflow-hidden'):
                            ui.element('div').props('id="map"').classes('w-full h-full')
                        
                        # Kích hoạt khởi tạo bản đồ khi tab mở
                        async def on_tab_change(e):
                            if e.value == 'map':
                                # Đợi một chút để DOM ổn định
                                await asyncio.sleep(0.5)
                                await ui.run_javascript('window.initMap()', respond=False)
                                await asyncio.sleep(0.2)
                                update_markers()
                        
                        tabs.on('update:model-value', on_tab_change)

        # Tải marker ban đầu
        ui.timer(0.5, update_markers, once=True)

@ui.page('/lang-quan-ho/{id}')
async def village_detail_page(id: int):
    with theme.frame():
        village = await api_client.get_village(id)
        if not village:
            components.empty_state('Không tìm thấy thông tin làng này.')
            return

        with ui.element('section').classes('w-full bg-background min-h-screen'):
            # Phần hero
            with ui.element('div').classes('relative h-[450px] md:h-[550px] w-full overflow-hidden'):
                ui.image(village.get('image_url')).classes('w-full h-full object-cover')
                with ui.element('div').classes('absolute inset-0 bg-gradient-to-t from-background via-black/20 to-transparent'):
                    with theme.container().classes('h-full flex flex-col justify-end pb-12'):
                        with ui.row().classes('items-center mb-4 gap-2'):
                            badges = village.get('badges') or 'Di sản'
                            for badge in badges.split(','):
                                ui.label(badge.strip()).classes('bg-primary text-white text-xs font-bold px-3 py-1 rounded-full shadow-lg h-min')
                        
                        ui.label(village.get('name')).classes('font-display text-5xl md:text-7xl font-bold text-white mb-4 drop-shadow-xl')
                        
                        with ui.row().classes('gap-6 text-white/90'):
                            with ui.row().classes('items-center gap-2'):
                                ui.icon('location_on', size='22px').classes('text-primary')
                                district = village.get('district') or 'Kinh Bắc'
                                ui.label(f"Huyện {district}").classes('text-lg font-medium')
                            with ui.row().classes('items-center gap-2'):
                                ui.icon('group', size='22px').classes('text-primary')
                                ui.label(f"{village.get('artist_count', 0)} Nghệ nhân").classes('text-lg font-medium')

            # Các phần nội dung
            with theme.container().classes('py-16 gap-12'):
                with ui.row().classes('grid grid-cols-1 lg:grid-cols-3 gap-16 w-full'):
                    # Văn bản chi tiết
                    with ui.column().classes('lg:col-span-2 gap-10'):
                        with ui.column().classes('gap-4'):
                            ui.label('Giới thiệu chung').classes('text-3xl font-display font-bold text-primary')
                            ui.label(village.get('description')).classes('text-lg leading-relaxed text-foreground/80 text-justify')
                        
                        ui.separator().classes('opacity-50')
                        
                        with ui.row().classes('grid grid-cols-1 md:grid-cols-2 gap-8 w-full'):
                            with ui.column().classes('gap-4'):
                                with ui.row().classes('items-center gap-2'):
                                    ui.icon('history_edu', size='28px').classes('text-primary')
                                    ui.label('Lịch sử hình thành').classes('text-xl font-bold font-display')
                                ui.label(village.get('history', 'Đang cập nhật...')).classes('text-muted-foreground leading-relaxed text-sm')
                            
                            with ui.column().classes('gap-4'):
                                with ui.row().classes('items-center gap-2'):
                                    ui.icon('auto_awesome', size='28px').classes('text-primary')
                                    ui.label('Đặc trưng văn hóa').classes('text-xl font-bold font-display')
                                ui.label(village.get('culture', 'Đang cập nhật...')).classes('text-muted-foreground leading-relaxed text-sm')

                        with ui.column().classes('p-8 bg-card rounded-3xl border border-border shadow-sm w-full gap-4'):
                            ui.label('Làn điệu đặc trưng').classes('text-xl font-bold text-center w-full')
                            with ui.row().classes('justify-center gap-3 w-full wrap'):
                                featured_songs = village.get('featured_songs') or 'Đang cập nhật'
                                for song in featured_songs.split(','):
                                    ui.label(song.strip()).classes('bg-muted px-4 py-2 rounded-xl text-foreground font-medium border border-border/50 hover:border-primary transition-all')

                    # Sidebar tương tác
                    with ui.column().classes('gap-8'):
                        with ui.column().classes('gap-4'):
                            with ui.row().classes('items-center gap-2'):
                                ui.icon('map', size='28px').classes('text-primary')
                                ui.label('Vị trí địa lý').classes('text-xl font-bold font-display')
                            
                            # Refined Google Maps integration
                            name = village.get('name')
                            addr = village.get('address')
                            lat, lng = village.get('latitude'), village.get('longitude')
                            
                            query = f"{name}, {addr}" if addr else f"{name}"
                            src_query = query.replace(' ', '+')
                            
                            if lat and lng:
                                # Using name + address for embed provides better branding than raw cords
                                src = f"https://www.google.com/maps?q={lat},{lng}&output=embed&z=15"
                                ui.html(f'<iframe src="{src}" width="100%" height="350" style="border:0;border-radius:1.5rem;box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);" allowfullscreen="" loading="lazy"></iframe>')
                                
                                with ui.link(target=f"https://www.google.com/maps/search/?api=1&query={src_query}").classes('flex items-center gap-2 text-primary hover:text-primary-focus transition-colors font-medium mt-2'):
                                    ui.icon('open_in_new', size='18px')
                                    ui.label('Mở trong Google Maps').classes('text-sm font-bold')
                            else:
                                ui.element('div').classes('h-[300px] bg-muted rounded-2xl flex items-center justify-center p-6 text-center').add(ui.label('Thông tin tọa độ đang được cập nhật').classes('text-sm italic text-muted-foreground'))

                        # Quick Links
                        with ui.card().classes('w-full p-6 rounded-3xl bg-primary text-white space-y-4'):
                            ui.label('Khám phá thêm').classes('text-xl font-bold')
                            with ui.row().classes('w-full justify-between items-center cursor-pointer group').on('click', lambda: ui.navigate.to('/nghe-nhan')):
                                ui.label('Nghệ nhân của làng').classes('font-medium')
                                ui.icon('chevron_right').classes('group-hover:translate-x-1 transition-transform')
                            ui.separator().classes('bg-white/20')
                            with ui.row().classes('w-full justify-between items-center cursor-pointer group').on('click', lambda: ui.navigate.to('/bai-hat')):
                                ui.label('Kho tàng làn điệu').classes('font-medium')
                                ui.icon('chevron_right').classes('group-hover:translate-x-1 transition-transform')

            # Navigation
            ui.separator().classes('my-12 opacity-30')
            with ui.row().classes('w-full justify-between items-center py-4'):
                ui.button('Làng trước đó', icon='arrow_back', on_click=lambda: ui.navigate.to(f'/lang-quan-ho/{max(1, id-1)}')).props('flat rounded color="primary"').classes('font-bold')
                ui.button('Về danh sách', on_click=lambda: ui.navigate.to('/lang-quan-ho')).props('outline rounded color="primary"').classes('px-8 font-bold')
                ui.button('Làng tiếp theo', icon='arrow_forward', on_click=lambda: ui.navigate.to(f'/lang-quan-ho/{id+1}')).props('flat rounded color="primary" icon-right="arrow_forward"').classes('font-bold')

