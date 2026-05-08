from nicegui import ui, app
from api import api_client
from translation import t
import theme
import components
import asyncio

@ui.page('/admin/events')
async def admin_events_page():
    if app.storage.user.get('role') != 'admin':
        ui.navigate.to('/')
        return

    with theme.frame():
        with ui.element('div').classes('w-full bg-[#faf9f6] min-h-screen pb-24'):
            # Header
            with ui.element('div').classes('w-full bg-white border-b border-border/60 pt-12 pb-8 shadow-sm'):
                with theme.container():
                    with ui.row().classes('w-full justify-between items-center'):
                        with ui.column().classes('gap-1'):
                            with ui.row().classes('items-center gap-2'):
                                ui.icon('event', size='18px', color='primary')
                                ui.label(t('manage_events')).classes('text-[10px] font-black tracking-[0.3em] text-primary uppercase')
                            ui.label('QUẢN LÝ SỰ KIỆN').classes('text-4xl font-black text-foreground tracking-tight')
                        
                        ui.button(t('add_prefix') + ' ' + t('et_event'), icon='add', on_click=lambda: ui.navigate.to('/admin/edit/event/0')) \
                            .props('unelevated rounded-full').classes('bg-primary text-white font-bold px-8 h-12 shadow-lg shadow-primary/20')

            # Content
            with theme.container().classes('mt-12'):
                await events_list()

async def events_list():
    events = await api_client.get_events(limit=100)
    
    if not events:
        with ui.column().classes('w-full items-center justify-center py-24 opacity-40'):
            ui.icon('event_busy', size='80px')
            ui.label('Chưa có sự kiện nào').classes('text-xl font-bold mt-4')
        return

    with ui.element('div').classes('grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8'):
        for e in events:
            with ui.card().classes('rounded-[32px] border border-border/40 overflow-hidden shadow-sm hover:shadow-md transition-all p-0 group bg-white'):
                # Image
                with ui.element('div').classes('relative h-48 w-full overflow-hidden'):
                    ui.image(e.get('image_url') or 'https://images.unsplash.com/photo-1599908608021-b5d929aa054e?auto=format&fit=crop&q=80&w=800').classes('w-full h-full object-cover group-hover:scale-105 transition-transform duration-700')
                    # Status Badge
                    status = e.get('status', 'upcoming')
                    color = 'green' if status == 'ongoing' else 'blue' if status == 'upcoming' else 'grey'
                    ui.label(t(f'status_{status}').upper()).classes(f'absolute top-4 right-4 bg-{color}-600 text-white text-[9px] font-black px-3 py-1 rounded-full shadow-lg z-10')

                with ui.column().classes('p-6 gap-3'):
                    ui.label(e['title']).classes('font-black text-xl line-clamp-1 group-hover:text-primary transition-colors')
                    
                    with ui.row().classes('items-center gap-2 text-muted-foreground'):
                        ui.icon('place', size='16px')
                        ui.label(e.get('location') or 'Bắc Ninh').classes('text-xs font-bold')
                    
                    with ui.row().classes('items-center gap-2 text-muted-foreground'):
                        ui.icon('schedule', size='16px')
                        date_str = e.get('start_date', '')[:10] if e.get('start_date') else 'N/A'
                        ui.label(date_str).classes('text-xs font-bold')

                    ui.separator().classes('my-2 opacity-50')
                    
                    with ui.row().classes('w-full items-center gap-6'):
                        with ui.row().classes('items-center gap-1'):
                            ui.icon('people', size='16px', color='primary')
                            ui.label(f"{e.get('registered_count', 0)}/{e.get('max_participants', 100)}").classes('text-xs font-black text-primary')
                        
                        with ui.row().classes('gap-1'):
                            ui.button(icon='edit', on_click=lambda e=e: ui.navigate.to(f'/admin/edit/event/{e["id"]}')).props('flat round size=sm').classes('text-primary hover:bg-primary/5')
                            ui.button(icon='delete_outline', on_click=lambda e=e: delete_event(e)).props('flat round size=sm color=destructive').classes('hover:bg-red-50')

async def delete_event(event):
    dialog = ui.dialog()
    with dialog, ui.card().classes('p-10 rounded-[40px] border border-border/40 shadow-2xl'):
        with ui.column().classes('items-center text-center gap-6'):
            with ui.element('div').classes('w-20 h-20 bg-red-50 rounded-full flex items-center justify-center'):
                ui.icon('delete_sweep', color='destructive', size='40px')
            
            with ui.column().classes('gap-1'):
                ui.label(t('confirm_delete')).classes('text-2xl font-black text-foreground')
                ui.label('Bạn có chắc chắn muốn xóa sự kiện này? Hành động này không thể hoàn tác.').classes('text-muted-foreground text-sm')
            
            with ui.row().classes('w-full justify-center gap-4 mt-4'):
                ui.button(t('cancel_btn'), on_click=lambda: dialog.submit(False)).props('flat rounded-full').classes('px-8 font-bold text-muted-foreground')
                ui.button(t('delete_now'), on_click=lambda: dialog.submit(True)).props('unelevated rounded-full color=destructive').classes('px-10 font-black shadow-lg shadow-red-100')
    
    if await dialog:
        res = await api_client.delete_event(event['id'])
        if res:
            ui.notify(t('delete_success'), type='positive')
            ui.navigate.reload()
        else:
            ui.notify(t('delete_error'), type='negative')
