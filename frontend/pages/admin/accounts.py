from nicegui import app, ui
import theme
import components
from api import api_client
from translation import t
import asyncio

@ui.page('/admin/accounts')
async def admin_accounts_page():
    # 1. Security Check
    if not app.storage.user.get('is_authenticated') or app.storage.user.get('role') != 'admin':
        ui.navigate.to('/dang-nhap')
        return

    # 2. Local State
    class PageState:
        def __init__(self):
            self.users = []
            self.search = ''
            self.page = 1
            self.items_per_page = 10
            self.total_count = 0
            self.edit_user_id = None
            self.delete_id = None

    state = PageState()

    # 3. Action Handlers
    async def do_save_edit():
        if not state.edit_user_id: return
        payload = {'name': edit_name.value, 'role': edit_role.value}
        if await api_client.update_user_admin(state.edit_user_id, payload):
            ui.notify(t('update_success'), type='positive')
            edit_dialog.close()
            content_area.refresh()
        else:
            ui.notify(t('update_error'), type='negative')

    async def do_delete():
        if not state.delete_id: return
        if await api_client.delete_user(state.delete_id):
            ui.notify(t('user_deleted'), type='positive')
            delete_dialog.close()
            content_area.refresh()
        else:
            ui.notify(t('delete_user_error'), type='negative')

    # 4. Dialogs
    with ui.dialog() as edit_dialog, ui.card().classes('p-8 rounded-3xl w-96'):
        ui.label(t('update_account')).classes('text-2xl font-bold mb-6')
        edit_name = ui.input(t('user_fullname')).classes('w-full modern-input').props('outlined rounded-2xl')
        edit_role = ui.select({'admin': t('role_admin'), 'user': t('role_member')}, label=t('system_role')).classes('w-full modern-input').props('outlined rounded-2xl')
        with ui.row().classes('w-full justify-end gap-3 mt-6'):
            ui.button(t('close_btn'), on_click=edit_dialog.close).props('flat')
            ui.button(t('save_changes'), on_click=do_save_edit).props('unelevated rounded-xl')

    with ui.dialog() as delete_dialog, ui.card().classes('p-8 rounded-3xl text-center'):
        ui.icon('report_problem', size='4rem', color='negative').classes('mb-4')
        ui.label(t('confirm_delete_account')).classes('text-xl font-bold mb-2')
        ui.label(t('data_deleted_forever')).classes('text-muted-foreground mb-6')
        with ui.row().classes('w-full justify-center gap-4'):
            ui.button(t('cancel_btn'), on_click=delete_dialog.close).props('flat')
            ui.button(t('delete_now'), on_click=do_delete).props('unelevated color=negative')

    # 5. UI Layout
    with theme.frame():
        with ui.element('section').classes('pt-12 pb-24 bg-background w-full'):
            with theme.container():
                # Header
                with ui.row().classes('w-full justify-between items-center mb-12'):
                    with ui.column().classes('gap-1'):
                        with ui.link(target='/admin').classes('flex items-center gap-1 text-primary no-underline hover:underline mb-2'):
                            ui.icon('arrow_back', size='16px')
                            ui.label(t('back_btn'))
                        ui.label(t('user_list_title')).classes('text-4xl font-display font-bold')
                        ui.label(t('user_list_desc')).classes('text-muted-foreground')

                # Main Content Card
                with ui.card().classes('w-full p-8 rounded-[2rem] shadow-xl border border-border bg-card'):
                    @ui.refreshable
                    async def content_area():
                        state.total_count = await api_client.get_users_count()
                        skip = (state.page - 1) * state.items_per_page
                        state.users = await api_client.get_users(skip=skip, limit=state.items_per_page)

                        if not state.users:
                            ui.spinner().classes('mx-auto my-20')
                        else:
                            # Table Header
                            with ui.row().classes('w-full bg-muted/20 p-4 font-black text-[10px] tracking-widest text-muted-foreground uppercase rounded-t-xl'):
                                ui.label(t('col_user')).classes('flex-1')
                                ui.label(t('col_role')).classes('w-32 text-center')
                                ui.label(t('col_actions')).classes('w-32 text-center')

                            for user in state.users:
                                with ui.row().classes('w-full items-center p-4 border-b border-border/50 hover:bg-muted/30 transition-colors'):
                                    with ui.column().classes('flex-1 gap-0'):
                                        ui.label(user.get('name', 'N/A')).classes('font-bold')
                                        ui.label(user.get('email', 'N/A')).classes('text-xs text-muted-foreground')
                                    
                                    role = user.get('role', 'user')
                                    is_admin = role == 'admin'
                                    with ui.element('div').classes('w-32 flex justify-center'):
                                        bg_color = 'bg-primary/10 text-primary' if is_admin else 'bg-jade/10 text-jade'
                                        ui.label(t('role_admin') if is_admin else t('role_member')).classes(
                                            f'px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-wider {bg_color}'
                                        )

                                    with ui.row().classes('w-32 justify-end gap-2'):
                                        def start_edit(u=user):
                                            state.edit_user_id = u['id']
                                            edit_name.value = u.get('name', '')
                                            edit_role.value = u.get('role', 'user')
                                            edit_dialog.open()
                                        
                                        def start_del(u_id=user['id']):
                                            if u_id == app.storage.user.get('user_id'):
                                                ui.notify(t('cannot_delete_self'), type='warning')
                                                return
                                            state.delete_id = u_id
                                            delete_dialog.open()

                                        ui.button(icon='edit', on_click=start_edit).props('flat round size=sm color=primary')
                                        ui.button(icon='delete', on_click=start_del).props('flat round size=sm color=negative')

                            components.pagination_controls(state, state.total_count, content_area)

                    await content_area()
