from nicegui import app, ui
import theme
import components
from api import api_client
from translation import t, tc
import asyncio

@ui.page('/admin/melodies')
async def admin_melodies_page():
    if not app.storage.user.get('is_authenticated') or app.storage.user.get('role') != 'admin':
        ui.navigate.to('/dang-nhap')
        return

    class PageState:
        def __init__(self):
            self.items = []
            self.page = 1
            self.items_per_page = 10
            self.total_count = 0
            self.delete_id = None

    state = PageState()

    async def do_delete():
        if not state.delete_id: return
        if await api_client.delete_melody(state.delete_id):
            ui.notify(t('delete_success'), type='positive')
            delete_dialog.close()
            content_area.refresh()
        else:
            ui.notify(t('delete_error'), type='negative')

    with ui.dialog() as delete_dialog, ui.card().classes('p-8 rounded-3xl text-center'):
        ui.icon('report_problem', size='4rem', color='negative').classes('mb-4')
        ui.label(t('confirm_delete')).classes('text-xl font-bold mb-2')
        ui.label(t('delete_confirm_msg')).classes('text-muted-foreground mb-6')
        with ui.row().classes('w-full justify-center gap-4'):
            ui.button(t('cancel_btn'), on_click=delete_dialog.close).props('flat')
            ui.button(t('delete_now'), on_click=do_delete).props('unelevated color=negative')

    with theme.frame():
        with ui.element('section').classes('pt-12 pb-24 bg-background w-full'):
            with theme.container():
                with ui.row().classes('w-full justify-between items-center mb-12'):
                    with ui.column().classes('gap-1'):
                        with ui.link(target='/admin').classes('flex items-center gap-1 text-primary no-underline hover:underline mb-2'):
                            ui.icon('arrow_back', size='16px')
                            ui.label(t('back_btn'))
                        ui.label(t('manage_melodies')).classes('text-4xl font-display font-bold')
                    
                    ui.button(t('add_prefix') + ' ' + t('et_song'), icon='add', 
                              on_click=lambda: ui.navigate.to('/admin/edit/song/0')).props('unelevated rounded-xl color=primary').classes('px-6 shadow-lg shadow-primary/20')

                with ui.card().classes('w-full p-8 rounded-[2rem] shadow-xl border border-border bg-card'):
                    @ui.refreshable
                    async def content_area():
                        state.total_count = await api_client.get_melodies_count()
                        skip = (state.page - 1) * state.items_per_page
                        state.items = await api_client.get_melodies(skip=skip, limit=state.items_per_page)

                        if not state.items:
                            ui.spinner().classes('mx-auto my-20')
                        else:
                            with ui.row().classes('w-full bg-muted/20 p-4 font-black text-[10px] tracking-widest text-muted-foreground uppercase rounded-t-xl'):
                                ui.label(t('et_song')).classes('flex-1')
                                ui.label(t('field_category')).classes('w-32 text-center')
                                ui.label(t('col_actions')).classes('w-32 text-right')

                            for item in state.items:
                                with ui.row().classes('w-full items-center p-4 border-b border-border/50 hover:bg-muted/30 transition-colors'):
                                    with ui.row().classes('flex-1 items-center gap-4'):
                                        ui.image(item.get('image_url') or '').classes('w-12 h-12 rounded-lg object-cover bg-muted')
                                        ui.label(tc(item, 'name')).classes('font-bold')
                                    
                                    cat = item.get('category', 'co')
                                    cat_label = { 'co': t('cat_co'), 'moi': t('cat_moi'), 'cai-bien': t('cat_cai_bien') }.get(cat, cat)
                                    colors = {'co': 'bg-primary/10 text-primary', 'moi': 'bg-jade/10 text-jade', 'cai-bien': 'bg-accent/10 text-accent'}
                                    with ui.element('div').classes('w-32 flex justify-center'):
                                        ui.label(cat_label).classes(f'px-2 py-0.5 rounded-full text-[10px] font-black uppercase tracking-wider {colors.get(cat, "bg-muted")}')

                                    with ui.row().classes('w-32 justify-end gap-2'):
                                        ui.button(icon='edit', on_click=lambda i=item: ui.navigate.to(f'/admin/edit/song/{i["id"]}')).props('flat round size=sm color=primary')
                                        ui.button(icon='delete', on_click=lambda i=item: (setattr(state, 'delete_id', i['id']), delete_dialog.open())).props('flat round size=sm color=negative')

                            components.pagination_controls(state, state.total_count, content_area)

                    await content_area()
