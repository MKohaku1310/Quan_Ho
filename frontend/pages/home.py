from nicegui import ui
import theme
import components
from api import api_client
from translation import t

import asyncio

@ui.page('/', response_timeout=60.0)
async def home_page():
    with theme.frame():
        components.hero_banner()

        # Featured Melodies
        with ui.element('section').classes('py-24 bg-background w-full').props('id="home-content"'):
            with theme.container():
                components.section_title(t('home_featured_melodies'), t('home_melodies_subtitle'))

                # Parallel data fetching using asyncio.gather
                tasks = [
                    api_client.get_melodies(),
                    api_client.get_artists(),
                    api_client.get_articles(),
                    api_client.get_events()
                ]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Unpack safely
                melodies = results[0] if isinstance(results[0], list) else []
                artists_data = results[1] if isinstance(results[1], list) else []
                articles_data = results[2] if isinstance(results[2], list) else []
                events_data = results[3] if isinstance(results[3], list) else []

                featured_melodies = melodies[:3] if melodies else []


                if not featured_melodies:
                    with ui.row().classes('w-full justify-center py-20'):
                        ui.spinner(size='xl', color='primary', thickness=2)
                else:
                    with ui.row().classes('grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 w-full'):
                        cat_map = {'co': t('cat_co'), 'moi': t('cat_moi'), 'cai-bien': t('cat_cai_bien')}
                        for song in featured_melodies:
                            components.song_card(
                                song.get('id'),
                                song.get('name', t('no_title')),
                                song.get('artist', {}).get('name', t('card_artist_default')) if isinstance(song.get('artist'), dict) else t('card_artist_default'),
                                song.get('image_url'),
                                melody=cat_map.get(song.get('category'), t('card_melody_old')),
                                duration=song.get('duration'),
                                video_url=song.get('video_url')
                            )

                with ui.row().classes('mt-12 w-full justify-center'):
                    with ui.link(target='/bai-hat').classes('no-underline flex items-center gap-2 text-primary font-bold cursor-pointer group'):
                        ui.label(t('home_view_all_songs')).classes('text-sm uppercase tracking-widest')
                        ui.icon('arrow_forward', size='20px').classes('group-hover:translate-x-1 transition-transform')

        components.hero_stats_section()

        # Featured Artists
        with ui.element('section').classes('py-24 bg-background w-full'):
            with theme.container():
                components.section_title(t('home_featured_artists'), t('home_artists_subtitle'))

                featured_artists = artists_data[:4] if artists_data else []


                if not featured_artists:
                    ui.label(t('searching_artists')).classes('w-full text-center py-10 italic text-muted-foreground')
                else:
                    with ui.row().classes('grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 w-full'):
                        for i, artist in enumerate(featured_artists):
                            components.artist_card(
                                artist.get('id'),
                                artist.get('name', t('card_artist_default')),
                                artist.get('image_url', '/static/common/chatbot-avatar.png'),
                                artist.get('village', t('heritage_kinh_bac')),
                                index=i
                            )

        # News & Events
        with ui.element('section').classes('bg-card py-24 border-t border-border w-full'):
            with theme.container():
                components.section_title(t('home_news_events'), t('home_news_subtitle'))

                news_items = (articles_data[:2] if articles_data else []) + (events_data[:2] if events_data else [])


                if not news_items:
                    ui.label(t('no_news')).classes('w-full text-center py-10 opacity-50')
                else:
                    with ui.row().classes('grid grid-cols-1 lg:grid-cols-2 gap-6 w-full'):
                        for item in news_items:
                            components.news_card(
                                item.get('id'),
                                item.get('title', t('new_announcement')),
                                item.get('image_url', 'https://images.unsplash.com/photo-1526462981764-f6cf0f4ea260?auto=format&fit=crop&q=80&w=400'),
                                type=t('event_label') if 'start_date' in item else t('news_label'),
                                date=(item.get('created_at') or item.get('start_date') or '--/--/----')[:10],
                            )

                    with ui.row().classes('mt-12 w-full justify-center'):
                        with ui.link(target='/tin-tuc').classes('no-underline flex items-center gap-2 text-primary font-bold cursor-pointer group'):
                            ui.label(t('home_view_all_news')).classes('text-sm uppercase tracking-widest')
                            ui.icon('arrow_forward', size='20px').classes('group-hover:translate-x-1 transition-transform')
