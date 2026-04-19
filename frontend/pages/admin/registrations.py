from nicegui import app, ui
import theme
import components
from api import api_client
from translation import t
import asyncio

@ui.page('/admin/registrations')
async def admin_registrations_page():
    if not app.storage.user.get('is_authenticated') or app.storage.user.get('role') != 'admin':
        ui.navigate.to('/dang-nhap')
        return

    class PageState:
        def __init__(self):
            self.registrations = []
            self.page = 1
            self.items_per_page = 15
            self.total_count = 0

    state = PageState()

    with theme.frame():
        with ui.element('section').classes('pt-12 pb-24 bg-paper-texture min-h-screen animate-fade-in-up'):
            with theme.container().classes('max-w-6xl'):
                # Header
                with ui.row().classes('w-full justify-between items-center mb-12 px-4'):
                    with ui.row().classes('items-center gap-6'):
                        with ui.element('div').classes('h-16 w-16 seal-stamped rounded-3xl flex items-center justify-center rotate-[-3deg] shadow-lg'):
                            ui.icon('how_to_reg', size='2.5rem', color='white')
                        with ui.column().classes('gap-0'):
                            ui.label(t('content_admin')).classes('text-[11px] font-black tracking-[0.4em] text-primary opacity-90 uppercase cultural-header-line')
                            ui.label(t('registration_list_title')).classes('text-4xl sm:text-5xl font-display font-bold text-foreground tracking-tighter mt-1')
                    
                    with ui.link(target='/admin').classes('group flex items-center gap-3 no-underline'):
                        ui.button(icon='arrow_back', color='primary').props('flat round').classes('bg-white/40 backdrop-blur-md shadow-sm group-hover:-translate-x-1 transition-transform')
                        ui.label(t('back_btn')).classes('text-sm font-black tracking-widest text-primary opacity-70 group-hover:opacity-100 transition-opacity')

                # Main Content
                with ui.card().classes('w-full p-0 rounded-[2.5rem] glass-card border-none shadow-elevated overflow-hidden'):
                    @ui.refreshable
                    async def content_area():
                        state.total_count = await api_client.get_event_registrations_count()
                        skip = (state.page - 1) * state.items_per_page
                        state.registrations = await api_client.get_all_event_registrations(skip=skip, limit=state.items_per_page)

                        if not state.registrations:
                            with ui.column().classes('w-full items-center justify-center py-24 gap-4'):
                                ui.icon('event_busy', size='4rem', color='muted')
                                ui.label(t('no_registrations')).classes('text-muted-foreground italic text-lg')
                        else:
                            # Table Header
                            with ui.row().classes('w-full bg-primary/5 p-6 font-black text-[11px] tracking-[0.2em] text-primary/70 uppercase border-b border-primary/10'):
                                ui.label(t('col_event')).classes('flex-1')
                                ui.label(t('col_participant')).classes('w-48 text-center')
                                ui.label(t('col_contact')).classes('w-48 text-center')
                                ui.label(t('col_note')).classes('w-48 text-center')

                            # Rows
                            for reg in state.registrations:
                                with ui.row().classes('w-full items-center p-6 border-b border-border/30 hover:bg-primary/[0.02] transition-all duration-300 group'):
                                    # Event Info
                                    with ui.column().classes('flex-1 gap-1'):
                                        ui.label((reg.get('event') or {}).get('title', 'N/A')).classes('font-display font-bold text-lg text-foreground group-hover:text-primary transition-colors line-clamp-1')
                                        with ui.row().classes('items-center gap-2'):
                                            ui.icon('calendar_today', size='12px', color='muted')
                                            ui.label(reg.get('created_at', '')[:10]).classes('text-[11px] text-muted-foreground font-medium')
                                    
                                    # Participant Info
                                    with ui.column().classes('gap-0 w-48 items-center text-center'):
                                        ui.label(reg.get('name', 'N/A')).classes('font-bold text-sm text-foreground')
                                        ui.label((reg.get('user') or {}).get('email', '')).classes('text-[11px] text-muted-foreground')

                                    # Contact Info
                                    with ui.column().classes('gap-1 w-48 items-center'):
                                        with ui.element('div').classes('px-3 py-1 bg-primary/10 rounded-full'):
                                            ui.label(reg.get('phone', 'N/A')).classes('font-bold text-xs text-primary')
                                        ui.label(t('at_local')).classes('text-[9px] font-black tracking-widest text-muted-foreground/50 uppercase')

                                    # Note
                                    with ui.row().classes('w-48 justify-center'):
                                        note = reg.get('note', '')
                                        if note:
                                            with ui.element('div').classes('p-3 bg-muted/20 rounded-xl w-full'):
                                                ui.label(note).classes('text-xs text-muted-foreground italic line-clamp-2 leading-relaxed')
                                        else:
                                            ui.label('—').classes('text-muted-foreground/30')

                            # Pagination
                            with ui.row().classes('w-full p-6 bg-muted/5'):
                                components.pagination_controls(state, state.total_count, content_area)

                    await content_area()
