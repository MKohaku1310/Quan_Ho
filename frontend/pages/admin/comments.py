from nicegui import app, ui
import theme
import components
from api import api_client
from translation import t
import asyncio

@ui.page('/admin/comments')
async def admin_comments_page():
    if not app.storage.user.get('is_authenticated') or app.storage.user.get('role') != 'admin':
        ui.navigate.to('/dang-nhap')
        return

    class PageState:
        def __init__(self):
            self.comments = []
            self.page = 1
            self.items_per_page = 15
            self.total_count = 0
            self.delete_id = None

    state = PageState()

    async def do_delete():
        if not state.delete_id: return
        if await api_client.delete_comment(state.delete_id):
            ui.notify(t('comment_deleted'), type='positive')
            delete_dialog.close()
            content_area.refresh()
        else:
            ui.notify(t('delete_comment_error'), type='negative')

    with ui.dialog() as delete_dialog, ui.card().classes('p-8 rounded-3xl text-center'):
        ui.icon('report_problem', size='4rem', color='negative').classes('mb-4')
        ui.label(t('delete_comment_title')).classes('text-xl font-bold mb-2')
        ui.label(t('comment_deleted_forever')).classes('text-muted-foreground mb-6')
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
                        ui.label(t('comment_list_title')).classes('text-4xl font-display font-bold')
                        ui.label(t('comment_list_desc')).classes('text-muted-foreground')

                with ui.card().classes('w-full p-8 rounded-[2rem] shadow-xl border border-border bg-card'):
                    @ui.refreshable
                    async def content_area():
                        state.total_count = await api_client.get_comments_count()
                        skip = (state.page - 1) * state.items_per_page
                        state.comments = await api_client.get_comments(skip=skip, limit=state.items_per_page)

                        if not state.comments:
                            ui.label(t('no_comment_found')).classes('mx-auto my-20 text-muted-foreground italic')
                        else:
                            with ui.row().classes('w-full bg-muted/20 p-4 font-black text-[10px] tracking-widest text-muted-foreground uppercase rounded-t-xl'):
                                ui.label(t('col_content')).classes('flex-1')
                                ui.label(t('col_sender')).classes('w-48')
                                ui.label(t('col_link')).classes('w-32 text-center')
                                ui.label(t('col_actions')).classes('w-32 text-right')

                            for comment in state.comments:
                                with ui.row().classes('w-full items-center p-4 border-b border-border/50 hover:bg-muted/30 transition-colors'):
                                    content = comment.get('content', '')
                                    ui.label(content[:100] + ('...' if len(content) > 100 else '')).classes('flex-1 text-sm')
                                    
                                    with ui.column().classes('w-48 gap-0'):
                                        ui.label((comment.get('user') or {}).get('name', t('anonymous'))).classes('font-bold text-xs')
                                        ui.label(comment.get('created_at', '')[:10]).classes('text-[10px] text-muted-foreground')

                                    is_melody = comment.get('melody_id')
                                    target_label = t('link_melody') if is_melody else t('link_news')
                                    bg_color = 'bg-primary/10 text-primary' if is_melody else 'bg-accent/10 text-accent'
                                    with ui.element('div').classes('w-32 flex justify-center'):
                                        ui.label(target_label).classes(f'px-2 py-0.5 rounded-full text-[10px] font-black uppercase tracking-wider {bg_color}')

                                    with ui.row().classes('w-32 justify-end'):
                                        def start_del(c_id=comment['id']):
                                            state.delete_id = c_id
                                            delete_dialog.open()
                                        ui.button(icon='delete', on_click=start_del).props('flat round size=sm color=negative')

                            components.pagination_controls(state, state.total_count, content_area)

                    await content_area()
