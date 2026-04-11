from nicegui import ui
import theme
import components
from api import api_client

@ui.page('/lang-quan-ho')
async def villages_page():
    with theme.frame():
        components.page_header('Làng Quan họ', 'Khai phá không gian văn hóa tại 49 làng Quan họ gốc')

        villages = await api_client.get_locations()
        map_state = {'query': 'Bắc Ninh, Việt Nam', 'lat': None, 'lng': None}

        def get_map_src():
            lat, lng = map_state.get('lat'), map_state.get('lng')
            q = f'{lat},{lng}' if lat and lng else map_state.get('query', 'Bắc Ninh')
            return f'https://www.google.com/maps?q={q}&output=embed&z=14'

        with ui.element('section').classes('pt-10 pb-4 w-full'):
            with theme.container():
                map_card = ui.card().classes('w-full overflow-hidden rounded-3xl border border-border shadow-elevated p-0')
                with map_card:
                    map_iframe = ui.html(f'<iframe src="{get_map_src()}" width="100%" height="450" style="border:0;" allowfullscreen loading="lazy"></iframe>')

        with ui.element('section').classes('pb-24 w-full'):
            with theme.container():
                if not villages:
                    components.empty_state('Dữ liệu đang được cập nhật...')
                else:
                    with ui.row().classes('grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 w-full'):
                        for v in villages:
                            def make_click(village):
                                def on_click():
                                    lat, lng = village.get('latitude'), village.get('longitude')
                                    if lat and lng:
                                        map_state.update({'lat': lat, 'lng': lng, 'query': f'{lat},{lng}'})
                                    else:
                                        map_state.update({'lat': None, 'lng': None, 'query': f"{village.get('name')} {village.get('address', '')} Bắc Ninh".strip()})
                                    map_iframe.content = f'<iframe src="{get_map_src()}" width="100%" height="450" style="border:0;" allowfullscreen loading="lazy"></iframe>'
                                return on_click

                            with ui.card().classes('group overflow-hidden rounded-2xl border border-border cursor-pointer').on('click', make_click(v)):
                                ui.image(v.get('image_url', 'https://images.unsplash.com/photo-1526462981764-f6cf0f4ea260?auto=format&fit=crop&q=80&w=600')).classes('h-48 w-full object-cover')
                                with ui.column().classes('p-6 gap-2'):
                                    ui.label(v.get('name', 'Làng')).classes('font-display text-xl font-bold text-primary')
                                    ui.label(v.get('description', '')).classes('text-sm text-muted-foreground line-clamp-3')
                                    ui.button('Xem trên bản đồ', icon='map').props('flat rounded').classes('text-primary font-bold mt-2')
