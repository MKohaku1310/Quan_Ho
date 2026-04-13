from nicegui import app, ui
import theme
import components
from api import api_client

import asyncio

@ui.page('/admin/edit/{et_type}/{et_id}')
async def admin_editor_page(et_type: str, et_id: int):
    if not app.storage.user.get('is_authenticated') or app.storage.user.get('role') != 'admin':
        ui.navigate.to('/dang-nhap')
        return

    # Mapping for titles and icons
    type_map = {
        'song': ('Bài hát', 'music_note'),
        'artist': ('Nghệ nhân', 'groups'),
        'village': ('Làng Quan họ', 'map'),
        'news': ('Tin tức / Sự kiện', 'article')
    }
    
    label, icon = type_map.get(et_type, ('Nội dung', 'edit'))
    is_edit = et_id > 0
    title_text = f"{'Chỉnh sửa' if is_edit else 'Thêm mới'} {label}"
    
    # Fetch data if editing
    data = {}
    if is_edit:
        if et_type == 'song': data = await api_client.get_melody(et_id)
        elif et_type == 'artist': data = await api_client.get_artist(et_id)
        elif et_type == 'village': data = await api_client.get_village(et_id)
        elif et_type == 'news': data = await api_client.get_article(et_id)
    
    if is_edit and not data:
        ui.notify('Không tìm thấy dữ liệu', type='negative')
        ui.navigate.to('/admin')
        return

    with theme.frame():
        with ui.element('section').classes('pt-12 pb-24 bg-background min-h-screen'):
            with theme.container().classes('max-w-4xl'):
                # Header
                with ui.row().classes('w-full justify-between items-end mb-10 px-4'):
                    with ui.column().classes('gap-1'):
                        ui.label('QUẢN TRỊ NỘI DUNG').classes('text-[10px] font-black tracking-[0.3em] text-primary opacity-80 uppercase')
                        ui.label(title_text).classes('text-4xl font-display font-bold text-foreground tracking-tight')
                    
                    ui.button('QUAY LẠI', icon='arrow_back', on_click=lambda: ui.navigate.back()).props('flat rounded').classes('font-bold')

                # Form Card
                with ui.card().classes('w-full p-8 sm:p-12 rounded-[2.5rem] shadow-xl border border-border bg-card flex flex-col gap-8'):
                    with ui.row().classes('items-center gap-4 mb-4'):
                        with ui.element('div').classes('h-12 w-12 rounded-2xl bg-primary/10 text-primary flex items-center justify-center'):
                            ui.icon(icon, size='1.8rem')
                        ui.label('Thông tin cơ bản').classes('text-2xl font-bold tracking-tight')

                    # Form Fields based on Type
                    fields = {}
                    
                    with ui.column().classes('w-full gap-6'):
                        # Shared: Name/Title
                        name_label = 'Tiêu đề' if et_type == 'news' else 'Tên gọi'
                        fields['name'] = ui.input(name_label, value=data.get('name') or data.get('title')).classes('w-full').props('outlined rounded-xl bg-background')
                        
                        if et_type == 'song':
                            fields['category'] = ui.select({'co': 'Làn điệu cổ', 'moi': 'Làn điệu mới', 'cai-bien': 'Làn điệu cải biên'}, value=data.get('category', 'co'), label='Thể loại').classes('w-full').props('outlined rounded-xl bg-background')
                            fields['village'] = ui.input('Làng quê', value=data.get('village')).classes('w-full').props('outlined rounded-xl bg-background')
                            fields['lyrics'] = ui.textarea('Lời bài hát', value=data.get('lyrics')).classes('w-full').props('outlined rounded-xl bg-background auto-grow')
                            fields['audio_url'] = ui.input('Link Audio (URL)', value=data.get('audio_url')).classes('w-full').props('outlined rounded-xl bg-background')
                        
                        elif et_type == 'artist':
                            fields['generation'] = ui.select({'truyen-thong': 'Nghệ nhân truyền thống', 'the-he-moi': 'Thế hệ mới'}, value=data.get('generation', 'truyen-thong'), label='Thế hệ').classes('w-full').props('outlined rounded-xl bg-background')
                            fields['village'] = ui.input('Làng quê', value=data.get('village')).classes('w-full').props('outlined rounded-xl bg-background')
                            fields['biography'] = ui.textarea('Tiểu sử', value=data.get('biography')).classes('w-full').props('outlined rounded-xl bg-background auto-grow')
                        
                        elif et_type == 'village':
                            fields['district'] = ui.input('Huyện/Thành phố', value=data.get('district')).classes('w-full').props('outlined rounded-xl bg-background')
                            fields['description'] = ui.textarea('Mô tả ngắn', value=data.get('description')).classes('w-full').props('outlined rounded-xl bg-background auto-grow')
                            with ui.row().classes('w-full grid grid-cols-2 gap-4'):
                                fields['latitude'] = ui.number('Vĩ độ (Lat)', value=data.get('latitude')).classes('w-full').props('outlined rounded-xl bg-background')
                                fields['longitude'] = ui.number('Kinh độ (Lng)', value=data.get('longitude')).classes('w-full').props('outlined rounded-xl bg-background')

                        elif et_type == 'news':
                            fields['category'] = ui.select({'tin-tuc': 'Tin tức', 'le-hoi': 'Lễ hội', 'nghe-thuat': 'Nghệ thuật'}, value=data.get('category', 'tin-tuc'), label='Phân loại').classes('w-full').props('outlined rounded-xl bg-background')
                            fields['content'] = ui.textarea('Nội dung chi tiết', value=data.get('content')).classes('w-full').props('outlined rounded-xl bg-background auto-grow')

                        # Shared: Image
                        fields['image_url'] = ui.input('Link ảnh đại diện', value=data.get('image_url')).classes('w-full').props('outlined rounded-xl bg-background')
                        if fields['image_url'].value:
                            ui.image(fields['image_url'].value).classes('w-full h-48 object-cover rounded-2xl border border-border shadow-sm')

                    # Action Buttons
                    with ui.row().classes('w-full justify-end gap-4 mt-8'):
                        ui.button('HỦY BỎ', on_click=lambda: ui.navigate.back()).props('flat rounded-xl').classes('px-8 font-bold text-muted-foreground')
                        
                        async def handle_save():
                            save_btn.props('loading')
                            payload = {k: v.value for k, v in fields.items()}
                            # Special case for news title
                            if et_type == 'news':
                                payload['title'] = payload.pop('name')
                            
                            if is_edit:
                                if et_type == 'song': res = await api_client.update_melody(et_id, payload)
                                elif et_type == 'artist': res = await api_client.update_artist(et_id, payload)
                                elif et_type == 'village': res = await api_client.update_location(et_id, payload)
                                elif et_type == 'news': res = await api_client.update_article(et_id, payload)
                            else:
                                if et_type == 'song': res = await api_client.create_melody(payload)
                                elif et_type == 'artist': res = await api_client.create_artist(payload)
                                elif et_type == 'village': res = await api_client.create_location(payload)
                                elif et_type == 'news': res = await api_client.create_article(payload)
                            
                            save_btn.props(remove='loading')
                            if res:
                                ui.notify(f"{'Cập nhật' if is_edit else 'Thêm mới'} thành công!", type='positive')
                                await asyncio.sleep(1)
                                ui.navigate.back()
                            else:
                                ui.notify('Đã xảy ra lỗi khi lưu dữ liệu', type='negative')
                        
                        save_btn = ui.button('LƯU DỮ LIỆU', on_click=handle_save).props('unelevated rounded-xl color=primary').classes('px-10 py-3 font-black shadow-xl shadow-primary/20 hover:scale-[1.02] transition-transform')
