from nicegui import app, ui
import theme
import components
from api import api_client
from translation import t
import asyncio
import re

# Decorators are no longer used on page functions due to FastAPI signature conflicts.
# Auth checks are performed inside page functions directly.

@ui.page('/dang-ky')
def register_page():
    if app.storage.user.get('is_authenticated'):
        ui.navigate.to('/')
        return

    with theme.frame():
        with ui.element('section').classes('py-20 md:py-32 bg-background w-full flex justify-center px-4 overflow-hidden relative'):
            # Background Decorative Elements
            ui.element('div').classes('absolute top-0 right-0 w-96 h-96 bg-primary/5 rounded-full blur-3xl -mr-48 -mt-48')
            ui.element('div').classes('absolute bottom-0 left-0 w-96 h-96 bg-secondary/5 rounded-full blur-3xl -ml-48 -mb-48')
            
            with ui.card().classes('w-full max-w-md p-0 rounded-[2.5rem] shadow-2xl border border-border bg-card/80 backdrop-blur-xl overflow-hidden'):
                with ui.row().classes('w-full g-0'):
                    # Form Side
                    with ui.column().classes('w-full p-6 sm:p-10 gap-5'):
                        with ui.column().classes('items-center w-full gap-1 mb-2'):
                            with ui.element('div').classes('h-16 w-16 rounded-3xl bg-primary/10 flex items-center justify-center text-primary mb-1 shadow-inner'):
                                ui.icon('person_add', size='2.5rem')
                            ui.label(t('register_title')).classes('font-display text-3xl font-bold text-center tracking-tight capitalize')
                            ui.label(t('register_subtitle')).classes('text-muted-foreground text-sm text-center max-w-[280px]')

                        with ui.column().classes('gap-4 w-full'):
                            name = ui.input(t('name_required')).classes('w-full modern-input').props('outlined rounded-2xl bg-background shadow-sm')
                            email = ui.input(t('email_field')).classes('w-full modern-input').props('outlined rounded-2xl type=email bg-background shadow-sm')
                            password = ui.input(t('password_field')).classes('w-full modern-input').props('outlined rounded-2xl type=password bg-background shadow-sm')
                            confirm_pass = ui.input(t('confirm_password_field')).classes('w-full modern-input').props('outlined rounded-2xl type=password bg-background shadow-sm')

                            async def handle_register():
                                if not all([name.value, email.value, password.value]):
                                    ui.notify(t('fill_all_fields'), type='warning')
                                    return
                                if password.value != confirm_pass.value:
                                    ui.notify(t('password_mismatch'), type='warning')
                                    return
                                
                                reg_btn.props('loading')
                                success = await api_client.register(name.value, email.value, password.value)
                                reg_btn.props(remove='loading')
                                
                                if success:
                                    ui.notify(t('register_success'), type='positive', position='top')
                                    ui.navigate.to('/dang-nhap')
                                else:
                                    ui.notify(t('register_failed'), type='negative')
                                    
                            reg_btn = ui.button(t('register_now_btn'), on_click=handle_register).props('unelevated rounded-xl').classes('w-full bg-primary text-white font-black py-3 mt-4 shadow-xl shadow-primary/20 hover:scale-[1.02] transition-transform text-base uppercase tracking-wider')
                            
                            with ui.row().classes('w-full justify-center gap-1.5 mt-4 text-sm'):
                                ui.label(t('already_have_account')).classes('text-muted-foreground')
                                ui.link(t('login_here_link'), '/dang-nhap').classes('text-primary font-bold hover:underline')

@ui.page('/dang-nhap')
def login_page():
    if app.storage.user.get('is_authenticated'):
        ui.navigate.to('/')
        return

    with theme.frame():
        with ui.element('section').classes('py-20 md:py-32 bg-background w-full flex justify-center px-4 overflow-hidden relative'):
            # Decorative
            ui.element('div').classes('absolute top-1/2 left-0 w-80 h-80 bg-primary/5 rounded-full blur-3xl -ml-40')
            
            with ui.card().classes('w-full max-w-md p-0 rounded-[2.5rem] shadow-2xl border border-border bg-card/80 backdrop-blur-xl overflow-hidden'):
                with ui.column().classes('w-full p-6 sm:p-10 gap-6'):
                    with ui.column().classes('items-center w-full gap-1'):
                        with ui.element('div').classes('h-16 w-16 rounded-3xl bg-primary/10 flex items-center justify-center text-primary mb-1 shadow-inner'):
                            ui.icon('login', size='2.5rem')
                        ui.label(t('login_title')).classes('font-display text-3xl font-bold text-center tracking-tight')
                        ui.label(t('login_subtitle')).classes('text-muted-foreground text-sm text-center')

                    with ui.column().classes('gap-5 w-full'):
                        email = ui.input(t('email_field')).classes('w-full modern-input').props('outlined rounded-2xl bg-background shadow-sm icon=alternate_email')
                        password = ui.input(t('password_field')).classes('w-full modern-input').props('outlined rounded-2xl type=password bg-background shadow-sm icon=lock')
                        
                        with ui.row().classes('w-full justify-between items-center -mt-2'):
                            ui.checkbox(t('remember_login')).classes('text-sm text-muted-foreground opacity-80')
                            ui.link(t('forgot_password_link'), '#').classes('text-sm text-primary hover:underline font-medium')

                        async def handle_login():
                            if not email.value or not password.value:
                                ui.notify(t('enter_email_password'), type='warning')
                                return
                            
                            login_btn.props('loading')
                            success = await api_client.login(email.value, password.value)
                            login_btn.props(remove='loading')
                            
                            if success:
                                ui.notify(f"{t('login_welcome')} {app.storage.user.get('user_name')}!", type='positive', position='top')
                                ui.navigate.to('/')
                            else:
                                ui.notify(t('login_failed'), type='negative')
                                
                        login_btn = ui.button(t('login'), on_click=handle_login).props('unelevated rounded-xl').classes('w-full bg-primary text-white font-black py-3 shadow-xl shadow-primary/20 hover:scale-[1.02] transition-transform text-base uppercase tracking-wider')
                        
                        with ui.row().classes('w-full justify-center gap-1.5 mt-2 text-sm'):
                            ui.label(t('test_dont_have_account')).classes('text-muted-foreground')
                            ui.link(t('register_free_link'), '/dang-ky').classes('text-primary font-bold hover:underline')


