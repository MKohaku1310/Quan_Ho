from nicegui import ui, app
import theme
import components
from api import api_client
from translation import t

@ui.page('/ho-so')
async def profile_page():
    if not app.storage.user.get('is_authenticated'):
        ui.navigate.to('/dang-nhap')
        return

    me = await api_client.get_me() or {}
    user_data = {
        'name': me.get('name') or app.storage.user.get('user_name', t('anonymous')),
        'email': me.get('email') or app.storage.user.get('email', t('no_title')),
        'role': me.get('role') or app.storage.user.get('role', 'user'),
        'phone': me.get('phone') or '',
        'bio': me.get('bio') or '',
        'avatar': '/static/common/chatbot-avatar.png'
    }

    with theme.frame():
        with ui.element('section').classes('py-24 bg-background min-h-screen'):
            with theme.container().classes('max-w-4xl'):
                # Profile Header
                with ui.card().classes('w-full border border-border bg-card shadow-elevated rounded-3xl p-8 mb-8 overflow-hidden'):
                    with ui.row().classes('items-center gap-8 w-full'):
                        ui.avatar(icon='account_circle', size='100px', color='primary', text_color='white').classes('shadow-lg')
                        with ui.column().classes('gap-1 flex-1'):
                            ui.label(user_data['name']).classes('text-4xl font-black font-display text-foreground')
                            with ui.row().classes('items-center gap-2 text-muted-foreground'):
                                ui.icon('email', size='18px')
                                ui.label(user_data['email']).classes('text-sm font-medium')
                            
                            with ui.row().classes('mt-2'):
                                role_color = 'primary' if user_data['role'] == 'admin' else 'secondary'
                                ui.label(user_data['role'].upper()).classes(f'bg-{role_color}/10 text-{role_color} text-[10px] font-black px-3 py-1 rounded-full border border-{role_color}/20 tracking-widest')
                        
                        if user_data['role'] == 'admin':
                            ui.button(t('profile_admin'), icon='admin_panel_settings', on_click=lambda: ui.navigate.to('/admin')).props('unelevated rounded-lg color=secondary').classes('font-bold shadow-md shadow-secondary/20')

                # Content Tabs
                with ui.tabs().classes('w-full border-b border-border mb-8 bg-card rounded-t-xl shadow-sm') as tabs:
                    act_tab = ui.tab(t('profile_activities'), icon='history').classes('px-10 font-bold text-xs tracking-widest')
                    info_tab = ui.tab(t('profile_membership'), icon='verified_user').classes('px-10 font-bold text-xs tracking-widest')
                    fav_tab = ui.tab(t('favorites_tab'), icon='favorite').classes('px-10 font-bold text-xs tracking-widest')

                with ui.tab_panels(tabs, value=act_tab).classes('w-full bg-transparent overflow-visible') as panels:
                    with ui.tab_panel(act_tab).classes('p-0'):
                        # Activities list
                        try:
                            activities = await api_client.get_my_activities()
                        except Exception as e:
                            print(f"Profile activity load error: {e}")
                            activities = []
                            
                        if not activities:
                            with ui.column().classes('items-center justify-center py-20 opacity-40 gap-4 w-full'):
                                ui.icon('history', size='64px')
                                ui.label(t('profile_no_activities')).classes('text-lg italic font-light')
                        else:
                            with ui.column().classes('gap-4 w-full'):
                                for act in activities:
                                    # Determine icon and color based on activity type
                                    if act['type'] == 'registration':
                                        icon_name = 'event_available'
                                        icon_box = 'bg-primary/10 text-primary'
                                    elif act['type'] == 'favorite':
                                        icon_name = 'favorite'
                                        icon_box = 'bg-red-500/10 text-red-500'
                                    elif act['type'] == 'history':
                                        icon_name = 'history'
                                        icon_box = 'bg-blue-500/10 text-blue-500'
                                    else:
                                        icon_name = 'activity'
                                        icon_box = 'bg-secondary/10 text-secondary'
                                    
                                    with ui.card().classes('w-full p-4 border border-border bg-card rounded-2xl flex flex-row items-center gap-4 hover:shadow-md transition-shadow'):
                                        with ui.element('div').classes(f'h-12 w-12 rounded-xl flex items-center justify-center shrink-0 {icon_box}'):
                                            ui.icon(icon_name, size='24px')
                                        
                                        with ui.column().classes('gap-0 flex-1'):
                                            ui.label(act['title']).classes('font-bold text-base')
                                            ui.label(act['details']).classes('text-xs text-muted-foreground line-clamp-1')
                                        
                                        # Format date safely
                                        date_str = ''
                                        if act.get('date'):
                                            try:
                                                if hasattr(act['date'], 'strftime'):
                                                    date_str = act['date'].strftime('%Y-%m-%d')
                                                else:
                                                    date_str = str(act['date'])[:10]
                                            except:
                                                date_str = str(act['date'])[:10]
                                        
                                        ui.label(date_str).classes('text-[10px] font-black text-muted-foreground bg-muted px-2 py-1 rounded uppercase tracking-tighter')

                    with ui.tab_panel(info_tab).classes('p-0'):
                        with ui.card().classes('w-full p-8 bg-card border border-border rounded-[2.5rem] shadow-elevated'):
                            ui.label(t('update_personal_info')).classes('text-2xl font-bold mb-8 tracking-tight')
                            
                            with ui.column().classes('w-full gap-4 mb-8'):
                                name_in = ui.input(t('full_name'), value=user_data['name']).classes('w-full modern-input').props('outlined rounded-2xl')
                                phone_in = ui.input(t('phone_number'), value=user_data['phone']).classes('w-full modern-input').props('outlined rounded-2xl')
                                bio_in = ui.textarea(t('introduction_label'), value=user_data['bio']).classes('w-full modern-input').props('outlined rounded-2xl autogrow')
                            
                            ui.separator().classes('my-8 opacity-50')
                            ui.label(t('change_password_btn')).classes('text-lg font-bold mb-4 opacity-70')
                            
                            with ui.row().classes('w-full grid grid-cols-1 md:grid-cols-2 gap-4 mb-8'):
                                old_pw = ui.input(t('old_password')).classes('w-full modern-input').props('outlined rounded-2xl password password_toggle_button')
                                new_pw = ui.input(t('new_password')).classes('w-full modern-input').props('outlined rounded-2xl password password_toggle_button')

                            async def save_profile():
                                payload = {
                                    'name': name_in.value,
                                    'phone': phone_in.value,
                                    'bio': bio_in.value,
                                }
                                ok = await api_client.update_profile(payload)
                                if ok:
                                    app.storage.user['user_name'] = name_in.value
                                    ui.notify(t('profile_updated'), type='positive')
                                else:
                                    ui.notify(api_client.get_last_error() or t('profile_update_failed'), type='negative')

                            async def change_pw():
                                if not old_pw.value or not new_pw.value:
                                    ui.notify(t('pw_fill_required'), type='warning')
                                    return
                                ok = await api_client.change_password(old_pw.value, new_pw.value)
                                if ok:
                                    old_pw.value = ''
                                    new_pw.value = ''
                                    ui.notify(t('change_pw_success'), type='positive')
                                else:
                                    ui.notify(api_client.get_last_error() or t('change_pw_failed'), type='negative')

                            with ui.row().classes('gap-3 mb-12'):
                                ui.button(t('save_profile'), on_click=save_profile).classes('px-8 py-2 elevated-btn font-bold rounded-xl').props('unelevated color=primary')
                                ui.button(t('change_password_btn'), on_click=change_pw).classes('px-8 py-2 font-bold rounded-xl').props('outline color=primary')

                            ui.label(t('profile_member_benefits')).classes('text-xl font-bold font-display text-primary mb-6')
                            benefits = [
                                (t('profile_event_priority'), t('profile_event_priority_desc')),
                                (t('profile_comment_content'), t('profile_comment_content_desc')),
                                (t('profile_training_programs'), t('profile_training_programs_desc'))
                            ]
                            for b_title, b_desc in benefits:
                                with ui.row().classes('items-start gap-4 mb-4'):
                                    ui.icon('check_circle', color='primary').classes('mt-1')
                                    with ui.column().classes('gap-0'):
                                        ui.label(b_title).classes('font-bold')
                                        ui.label(b_desc).classes('text-sm text-muted-foreground')

                    with ui.tab_panel(fav_tab).classes('p-0'):
                        favorites = await api_client.get_favorites()
                        if not favorites:
                            ui.label(t('no_favorites')).classes('text-muted-foreground italic py-6')
                        else:
                            with ui.column().classes('gap-4'):
                                for fav in favorites:
                                    melody = fav.get('melody') or {}
                                    with ui.card().classes('p-4 rounded-xl border border-border'):
                                        with ui.row().classes('w-full justify-between items-center'):
                                            with ui.column().classes('gap-0'):
                                                ui.label(melody.get('name', t('song_label'))).classes('font-bold')
                                                ui.label(melody.get('village') or '').classes('text-xs text-muted-foreground')
                                            ui.button(t('view_btn'), on_click=lambda m_id=fav.get('melody_id'): ui.navigate.to(f'/bai-hat/{m_id}')).props('flat color=primary')
                
                # Bottom Actions
                ui.separator().classes('my-12 opacity-30')
                with ui.row().classes('w-full justify-between items-center'):
                    ui.button(t('profile_back_home'), icon='home', on_click=lambda: ui.navigate.to('/')).props('flat color=primary').classes('font-bold')
                    ui.button(t('profile_logout'), icon='logout', on_click=api_client.logout).props('outline color=destructive').classes('px-8 font-bold rounded-lg')
