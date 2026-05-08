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
                'villages': 0, 'articles': 0, 'registrations': 0, 'orders': 0
            }

    state = DashboardState()

    async def load_stats():
        try:
            state.stats = {
                'users': await api_client.get_users_count(),
                'comments': await api_client.get_comments_count(),
                'melodies': await api_client.get_melodies_count(),
                'artists': await api_client.get_artists_count(),
                'villages': await api_client.get_locations_count(),
                'articles': await api_client.get_articles_count(),
                'registrations': await api_client.get_event_registrations_count(),
                'orders': await api_client.admin_get_orders_count()
            }
            overview_stats.refresh()
        except Exception as e:
            print(f"Error loading dashboard stats: {e}")

    # 4. UI Layout
    with theme.frame():
        with ui.element('div').classes('w-full bg-[#faf9f6] min-h-screen pb-24'):
            # Premium Admin Header
            with ui.element('div').classes('w-full bg-white border-b border-border/60 pt-12 pb-8 shadow-sm'):
                with theme.container():
                    with ui.row().classes('w-full justify-between items-center'):
                        with ui.column().classes('gap-1'):
                            with ui.row().classes('items-center gap-2'):
                                ui.icon('dashboard', size='18px', color='primary')
                                ui.label(t('admin_label')).classes('text-[10px] font-black tracking-[0.3em] text-primary uppercase')
                            ui.label(t('admin_system')).classes('text-4xl font-black text-foreground tracking-tight')
                        
                        with ui.row().classes('items-center gap-4 bg-muted/30 p-2 rounded-2xl border border-border/40'):
                            ui.avatar(app.storage.user.get('user_name', 'A')[0].upper(), color='primary', text_color='white').classes('shadow-lg font-black')
                            with ui.column().classes('gap-0 pr-4'):
                                ui.label(app.storage.user.get('user_name', 'Administrator')).classes('font-bold text-sm')
                                ui.label('Hệ thống quản trị di sản').classes('text-[9px] text-muted-foreground uppercase tracking-widest')

            with theme.container().classes('mt-12'):
                # 1. Overview Statistics (Top Row)
                @ui.refreshable
                def overview_stats():
                    with ui.row().classes('w-full grid grid-cols-2 lg:grid-cols-4 gap-6 mb-12'):
                        stat_items = [
                            (t('stats_accounts'), state.stats['users'], 'group', 'blue-600'),
                            (t('et_song'), state.stats['melodies'], 'music_note', 'primary'),
                            (t('et_artist'), state.stats['artists'], 'groups', 'amber-600'),
                            (t('et_village'), state.stats['villages'], 'map', 'indigo-600'),
                            (t('et_news'), state.stats['articles'], 'article', 'cyan-600'),
                            (t('stats_comments'), state.stats['comments'], 'forum', 'rose-600'),
                            (t('stats_event_regs'), state.stats['registrations'], 'assignment_turned_in', 'orange-600'),
                            (t('manage_orders'), state.stats['orders'], 'payments', 'emerald-600'),
                        ]
                        for label, value, icon, color in stat_items:
                            with ui.card().classes(f'p-6 rounded-[24px] border border-border/40 shadow-sm flex-row items-center gap-5 bg-white group hover:shadow-md transition-all'):
                                with ui.element('div').classes(f'h-14 w-14 rounded-2xl bg-{color}/5 text-{color} flex items-center justify-center shadow-inner shrink-0 group-hover:scale-110 transition-transform'):
                                    ui.icon(icon, size='24px')
                                with ui.column().classes('gap-0'):
                                    ui.label(label).classes('text-[10px] uppercase font-bold tracking-widest text-muted-foreground')
                                    ui.label(str(value)).classes('text-3xl font-black text-foreground tracking-tight')

                async def refresh_all_stats():
                    ui.notify('Đang cập nhật dữ liệu...', icon='refresh', color='info')
                    await load_stats()
                    ui.notify('Đã cập nhật số liệu mới nhất.', type='positive')

                with ui.row().classes('w-full justify-end mb-4 px-2'):
                    ui.button('Cập nhật số liệu', icon='refresh', on_click=refresh_all_stats).props('flat rounded-full color=primary').classes('text-xs font-bold')

                overview_stats()

                # 2. Management Modules (Categorized)
                ui.label('CÔNG CỤ QUẢN TRỊ').classes('text-[11px] font-black text-muted-foreground tracking-[0.4em] uppercase mb-8 ml-2')
                
                with ui.row().classes('w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8'):
                    management_tools = [
                        (t('manage_melodies'), 'music_note', '/admin/melodies', 'primary', t('manage_melodies_desc')),
                        (t('manage_artists'), 'groups', '/admin/artists', 'amber-700', t('manage_artists_desc')),
                        (t('manage_villages'), 'map', '/admin/villages', 'indigo-700', t('manage_villages_desc')),
                        (t('manage_news'), 'article', '/admin/news', 'emerald-700', t('manage_news_desc')),
                        (t('manage_events'), 'event', '/admin/events', 'purple-700', t('manage_events_desc')),
                        (t('user_list_title'), 'person_search', '/admin/accounts', 'blue-700', t('user_list_desc')),
                        (t('manage_comments'), 'forum', '/admin/comments', 'rose-600', t('manage_comments_desc')),
                        (t('registration_list_title'), 'fact_check', '/admin/registrations', 'orange-600', t('registration_list_desc')),
                        (t('manage_shop'), 'storefront', '/admin/shop', 'pink-600', 'Quản lý kho hàng & đơn hàng'),
                    ]

                    for title, icon, path, color, sub in management_tools:
                        with ui.card().classes('group hover:border-primary/40 transition-all duration-300 cursor-pointer overflow-hidden p-0 rounded-[32px] border border-border/40 bg-white shadow-sm h-full').on('click', lambda e, p=path: ui.navigate.to(p)):
                            with ui.column().classes('w-full p-8 gap-5'):
                                with ui.row().classes('w-full justify-between items-center'):
                                    with ui.element('div').classes(f'h-14 w-14 rounded-2xl bg-{color} flex items-center justify-center text-white shadow-lg group-hover:rotate-6 transition-all'):
                                        ui.icon(icon, size='28px')
                                    ui.icon('chevron_right', size='24px').classes('text-muted-foreground opacity-20 group-hover:opacity-100 group-hover:translate-x-1 transition-all')
                                
                                with ui.column().classes('gap-1'):
                                    ui.label(title).classes('font-black text-xl text-foreground tracking-tight group-hover:text-primary transition-colors')
                                    ui.label(sub).classes('text-xs text-muted-foreground leading-relaxed font-medium')
                            
                            ui.element('div').classes(f'h-1.5 w-full bg-{color} opacity-10 group-hover:opacity-100 transition-all')

                ui.timer(0.5, load_stats, once=True)
