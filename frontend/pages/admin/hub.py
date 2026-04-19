from nicegui import app, ui
import theme
import components
from api import api_client
from translation import t
import asyncio

# --- MAIN PAGE ---
@ui.page('/admin')
async def admin_page():
    # 1. Security Check
    if not app.storage.user.get('is_authenticated') or app.storage.user.get('role') != 'admin':
        ui.navigate.to('/dang-nhap')
        return

    # 2. Local State
    class DashboardState:
        def __init__(self):
            self.stats = {
                'users': 0, 'comments': 0, 'melodies': 0, 'artists': 0, 
                'villages': 0, 'articles': 0, 'registrations': 0
            }

    state = DashboardState()

    # 3. Action Handlers
    async def load_stats():
        state.stats = {
            'users': await api_client.get_users_count(),
            'comments': await api_client.get_comments_count(),
            'melodies': await api_client.get_melodies_count(),
            'artists': await api_client.get_artists_count(),
            'villages': await api_client.get_locations_count(),
            'articles': await api_client.get_articles_count(),
            'registrations': await api_client.get_event_registrations_count()
        }
        stats_row.refresh()

    # 4. UI Layout
    with theme.frame():
        with ui.element('section').classes('pt-12 pb-24 bg-background min-h-screen'):
            with theme.container():
                # Admin Header
                with ui.row().classes('w-full justify-between items-end mb-12'):
                    with ui.column().classes('gap-1'):
                        ui.label(t('admin_label')).classes('text-[11px] font-black tracking-[0.4em] text-primary opacity-80 uppercase')
                        ui.label(t('admin_system')).classes('text-5xl font-display font-bold text-foreground tracking-tight')

                    with ui.row().classes('items-center gap-4 p-2 bg-card rounded-2xl border border-border shadow-sm'):
                        ui.avatar(icon='admin_panel_settings', color='primary', text_color='white').classes('shadow-md')
                        with ui.column().classes('gap-0 pr-4'):
                            ui.label(app.storage.user.get('user_name', 'Administrator')).classes('font-bold text-sm')
                            ui.label(t('admin_role')).classes('text-[10px] text-primary font-black uppercase tracking-widest')

                # Management Navigation Tiles - NEW UPDATED ROUTES
                with ui.row().classes('w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16'):
                    tiles = [
                        (t('user_list_title'), 'people', '/admin/accounts', 'bg-blue-700', t('user_list_desc')),
                        (t('manage_melodies'), 'music_note', '/admin/melodies', 'bg-blue-600', t('manage_melodies_desc')),
                        (t('manage_artists'), 'groups', '/admin/artists', 'bg-amber-600', t('manage_artists_desc')),
                        (t('manage_news'), 'article', '/admin/news', 'bg-emerald-600', t('manage_news_desc')),
                        (t('manage_villages'), 'map', '/admin/villages', 'bg-indigo-600', t('manage_villages_desc')),
                        (t('manage_comments'), 'comment', '/admin/comments', 'bg-rose-500', t('manage_comments_desc')),
                        (t('registration_list_title'), 'how_to_reg', '/admin/registrations', 'bg-orange-500', t('registration_list_desc')),
                        (t('manage_events'), 'event', '/admin/edit/event/0', 'bg-purple-600', t('manage_events_desc')),
                    ]
                    for title, icon, path, color, sub in tiles:
                        with ui.card().classes('group hover:shadow-2xl hover:-translate-y-1 transition-all duration-300 cursor-pointer overflow-hidden p-0 rounded-[2.5rem] border border-border/50 bg-card shadow-sm').on('click', lambda e, p=path: ui.navigate.to(p)):
                            with ui.row().classes('w-full items-center p-8 gap-6'):
                                with ui.element('div').classes(f'h-16 w-16 rounded-[1.5rem] {color} flex items-center justify-center text-white shadow-xl group-hover:scale-110 transition-transform shrink-0'):
                                    ui.icon(icon, size='2.2rem')
                                with ui.column().classes('gap-0'):
                                    ui.label(title).classes('font-black text-xl group-hover:text-primary transition-colors text-foreground tracking-tight')
                                    ui.label(sub).classes('text-[10px] text-muted-foreground font-bold uppercase tracking-wider mt-1')
                            ui.element('div').classes(f'h-2 w-full {color} opacity-0 group-hover:opacity-100 transition-all')

                # Statistics Section
                with ui.column().classes('w-full gap-6'):
                    with ui.row().classes('items-center gap-3 mb-2'):
                        ui.icon('analytics', size='1.5rem', color='primary')
                        ui.label(t('system_stats')).classes('text-2xl font-bold tracking-tight')

                    @ui.refreshable
                    def stats_row():
                        with ui.row().classes('w-full grid grid-cols-2 lg:grid-cols-4 gap-6'):
                            items = [
                                (t('stats_accounts'), state.stats['users'], 'people', 'primary'),
                                (t('stats_event_regs'), state.stats['registrations'], 'event_available', 'amber-600'),
                                (t('et_song'), state.stats['melodies'], 'music_note', 'blue-600'),
                                (t('et_artist'), state.stats['artists'], 'groups', 'orange-600'),
                                (t('et_news'), state.stats['articles'], 'article', 'emerald-600'),
                                (t('et_village'), state.stats['villages'], 'map', 'indigo-600'),
                                (t('stats_comments'), state.stats['comments'], 'comment', 'rose-500'),
                            ]
                            for label, value, icon, color in items:
                                with ui.card().classes('p-6 rounded-[2rem] border border-border/50 shadow-sm flex-row items-center gap-5 hover:bg-muted/30 transition-all'):
                                    with ui.element('div').classes(f'h-14 w-14 rounded-2xl bg-{color}/10 text-{color} flex items-center justify-center shadow-inner shrink-0'):
                                        ui.icon(icon, size='2rem')
                                    with ui.column().classes('gap-0'):
                                        ui.label(label).classes('text-[10px] uppercase font-black tracking-[0.2em] text-muted-foreground')
                                        ui.label(str(value)).classes('text-3xl font-black text-foreground')
                    
                    stats_row()
                    ui.timer(0.1, load_stats, once=True)
