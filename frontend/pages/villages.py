import json
from nicegui import ui, app
import theme
import components
from api import api_client
import asyncio

# Leaflet Assets and Initialization Logic
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
        if (window.map) return;
        var mapElement = document.getElementById("map");
        if (!mapElement) return;
        window.map = L.map("map").setView([21.1861, 106.0763], 11);
        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            attribution: '&copy; OpenStreetMap contributors'
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
    # Inject Leaflet head assets outside frame context to avoid 500 error
    ui.add_head_html(LEAFLET_CSS)
    ui.add_head_html(LEAFLET_JS)
    ui.add_head_html(LEAFLET_POPUP_STYLE)
    ui.add_body_html(f'<script>{LEAFLET_INIT_JS}</script>')
    
    with theme.frame():
        # Hero section
        components.page_header('49 Làng Quan họ gốc', 'Khám phá không gian văn hóa di sản tại quê hương Quan họ')

        # ... (rest of state and fetching logic remains)
        class State:
            def __init__(self, items):
                self.all_items = items
                self.filtered_items = items
                self.search_query = ''
                self.district_filter = 'Tất cả'

        # Fetch data
        villages = await api_client.get_villages()
        if not villages:
            villages = [
                {'id': 1, 'name': 'Làng Diềm', 'district': 'TP Bắc Ninh', 'latitude': 21.2167, 'longitude': 106.0500, 'description': 'Cái nôi cổ nhất của dân ca Quan họ với kiến trúc cổng làng cổ kính rêu phong và giếng Ngọc thiêng liêng...', 'artist_count': 12, 'featured_songs': 'Ngồi tựa mạn thuyền, La hới la nương', 'badges': 'Cái nôi Quan họ, Di tích quốc gia', 'image_url': '/static/village_diem_ancient_gate_1775935115741.png'},
                {'id': 2, 'name': 'Làng Lim', 'district': 'Tiên Du', 'latitude': 21.1667, 'longitude': 106.0167, 'description': 'Nơi diễn ra hội Lim truyền thống với các canh hát đối đáp trên thuyền rồng đầy thơ mộng...', 'artist_count': 8, 'featured_songs': 'Khách đến chơi nhà', 'badges': 'Lễ hội lớn nhất', 'image_url': '/static/quan_ho_festival_boat_1775935130553.png'},
                {'id': 3, 'name': 'Làng Bịu', 'district': 'Tiên Du', 'latitude': 21.1750, 'longitude': 106.0250, 'description': 'Làng Bịu nổi tiếng với truyền thống truyền dạy Quan họ cho thế hệ trẻ ngay tại đình làng...', 'artist_count': 5, 'featured_songs': 'Ba sáu thứ chim', 'badges': 'Kết chạ truyền thống', 'image_url': '/static/quan_ho_teaching_children_1775935150468.png'}
            ]
        
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
            
            with ui.element('div').classes('grid grid-cols-1 lg:grid-cols-2 gap-6 w-full p-2'):
                for item in state.filtered_items:
                    components.village_grid_card(item, on_map_click=lambda item=item: ui.run_javascript(f'window.focusMarker({item["id"]})'))

        def apply_filters():
            q = state.search_query.lower()
            d = state.district_filter
            state.filtered_items = [
                v for v in state.all_items
                if (q in v.get('name', '').lower() or q in v.get('description', '').lower()) 
                and (d == 'Tất cả' or v.get('district') == d)
            ]
            village_list.refresh()
            update_markers()

        # Main Layout: Responsive Split
        with ui.element('div').classes('w-full flex flex-col md:flex-row h-screen md:h-[calc(100vh-64px)] overflow-hidden bg-background border-t border-border'):
            
            # Map Section
            with ui.element('div').classes('w-full md:w-[55%] lg:w-[60%] h-[40vh] md:h-full relative order-first md:order-last border-b md:border-b-0 md:border-l border-border'):
                ui.element('div').props('id="map"').classes('w-full h-full').style('height: 100%; width: 100%;')

            # List Section
            with ui.element('div').classes('w-full md:w-[45%] lg:w-[40%] h-[60vh] md:h-full flex flex-col bg-background order-last md:order-first'):
                # Control bar
                with ui.element('div').classes('p-4 sm:p-6 gap-4 bg-card/30 border-b border-border w-full shadow-sm z-10 flex flex-col'):
                    with ui.element('div').classes('w-full flex flex-col sm:flex-row items-center gap-3'):
                        search_input = ui.input(placeholder='Tìm làng...').classes('w-full sm:flex-1 shadow-inner bg-background').props('outlined dense clearable icon="search"').on('update:model-value', lambda e: (setattr(state, 'search_query', e or ''), apply_filters()))
                        
                        districts = ['Tất cả', 'Tiên Du', 'Từ Sơn', 'Yên Phong', 'TP Bắc Ninh']
                        district_select = ui.select(districts, value='Tất cả', label='Huyện').classes('w-full sm:w-40 bg-background').props('outlined dense rounded').on('update:model-value', lambda e: (setattr(state, 'district_filter', e), apply_filters()))

                # Scroll Area
                with ui.scroll_area().classes('flex-1 w-full'):
                    with ui.column().classes('p-4 sm:p-6 w-full gap-2'):
                        village_list()

        # Delayed init for Leaflet animation
        ui.timer(0.2, lambda: ui.run_javascript('window.initMap()'), once=True)
        ui.timer(0.5, update_markers, once=True)

@ui.page('/lang-quan-ho/{id}')
async def village_detail_page(id: int):
    with theme.frame():
        village = await api_client.get_village(id)
        # Fallback if API fails
        if not village:
            village = {
                'id': id, 
                'name': 'Làng Diềm', 
                'district': 'TP Bắc Ninh', 
                'latitude': 21.2167, 
                'longitude': 106.0500, 
                'description': 'Cái nôi cổ nhất của dân ca Quan họ Bắc Ninh. Làng Diềm (Viêm Xá) là nơi duy nhất thờ vị Thủy tổ Quan họ - Đức Vua Bà. Nơi đây không chỉ giữ được những làn điệu cổ truyền mà còn duy trì nếp sống, văn hóa Quan họ vô cùng đậm đà.', 
                'image_url': '/static/village_diem_ancient_gate_1775935115741.png', 
                'history': 'Làng Diềm có lịch sử hàng ngàn năm, gắn liền với huyền tích về Đức Vua Bà. Trải qua bao thăng trầm, làng vẫn giữ được 12 giọng Quan họ cổ tinh túy.', 
                'culture': 'Hàng năm vào ngày mùng 6 tháng Giêng, làng Diềm mở lễ hội Vua Bà - ngày hội lớn nhất của làng với nghi thức rước kiệu và các canh hát cửa đình, hát dưới thuyền đặc sắc.', 
                'artist_count': 15, 
                'featured_songs': 'Ngồi tựa mạn thuyền, La hới la nương', 
                'badges': 'Thủy tổ Quan họ, Di tích Quốc gia'
            }

        with ui.element('section').classes('w-full bg-background min-h-screen'):
            # Hero section
            with ui.element('div').classes('relative h-[450px] md:h-[550px] w-full overflow-hidden'):
                ui.image(village.get('image_url')).classes('w-full h-full object-cover')
                with ui.element('div').classes('absolute inset-0 bg-gradient-to-t from-background via-black/20 to-transparent'):
                    with theme.container().classes('h-full flex flex-col justify-end pb-12'):
                        with ui.row().classes('items-center mb-4 gap-2'):
                            for badge in (village.get('badges') or 'Di sản').split(','):
                                ui.label(badge.strip()).classes('bg-primary text-white text-xs font-bold px-3 py-1 rounded-full shadow-lg h-min')
                        
                        ui.label(village.get('name')).classes('font-display text-5xl md:text-7xl font-bold text-white mb-4 drop-shadow-xl')
                        
                        with ui.row().classes('gap-6 text-white/90'):
                            with ui.row().classes('items-center gap-2'):
                                ui.icon('location_on', size='22px').classes('text-primary')
                                ui.label(f"Huyện {village.get('district')}").classes('text-lg font-medium')
                            with ui.row().classes('items-center gap-2'):
                                ui.icon('group', size='22px').classes('text-primary')
                                ui.label(f"{village.get('artist_count')} Nghệ nhân").classes('text-lg font-medium')

            # Content sections
            with theme.container().classes('py-16 gap-12'):
                with ui.row().classes('grid grid-cols-1 lg:grid-cols-3 gap-16 w-full'):
                    # Detailed Text
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
                                for song in village.get('featured_songs', 'Đang cập nhật').split(','):
                                    ui.label(song.strip()).classes('bg-muted px-4 py-2 rounded-xl text-foreground font-medium border border-border/50 hover:border-primary transition-all')

                    # Interactive Sidebar
                    with ui.column().classes('gap-8'):
                        # Map detail
                        with ui.card().classes('w-full p-4 rounded-3xl border border-border bg-card shadow-sm overflow-hidden'):
                            ui.label('Vị trí địa lý').classes('text-lg font-bold mb-3 px-2')
                            lat, lng = village.get('latitude'), village.get('longitude')
                            if lat and lng:
                                src = f"https://www.google.com/maps?q={lat},{lng}&output=embed&z=15"
                                ui.html(f'<iframe src="{src}" width="100%" height="300" style="border:0; border-radius: 16px" allowfullscreen loading="lazy"></iframe>')
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
                ui.button('Làng trước đó', icon='arrow_back').props('flat rounded color="primary"').classes('font-bold')
                ui.button('Về danh sách', on_click=lambda: ui.navigate.to('/lang-quan-ho')).props('outline rounded color="primary"').classes('px-8 font-bold')
                ui.button('Làng tiếp theo', icon='arrow_forward').props('flat rounded color="primary" icon-right="arrow_forward"').classes('font-bold').props('icon-right="arrow_forward" icon=""')

