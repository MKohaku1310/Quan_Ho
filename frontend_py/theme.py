from nicegui import ui
import functools
import asyncio


def apply_theme():
    ui.add_head_html('''
        <script src="https://cdn.tailwindcss.com"></script>
        <script>
            tailwind.config = {
                theme: {
                    extend: {
                        colors: {
                            border: "hsl(var(--border))",
                            input: "hsl(var(--input))",
                            ring: "hsl(var(--ring))",
                            background: "hsl(var(--background))",
                            foreground: "hsl(var(--foreground))",
                            primary: {
                                DEFAULT: "hsl(var(--primary))",
                                foreground: "hsl(var(--primary-foreground))",
                            },
                            secondary: {
                                DEFAULT: "hsl(var(--secondary))",
                                foreground: "hsl(var(--secondary-foreground))",
                            },
                            muted: {
                                DEFAULT: "hsl(var(--muted))",
                                foreground: "hsl(var(--muted-foreground))",
                            },
                            accent: {
                                DEFAULT: "hsl(var(--accent))",
                                foreground: "hsl(var(--accent-foreground))",
                            },
                            card: {
                                DEFAULT: "hsl(var(--card))",
                                foreground: "hsl(var(--card-foreground))",
                            },
                            gold: {
                                DEFAULT: "hsl(var(--gold))",
                                light: "hsl(var(--gold-light))",
                                dark: "hsl(var(--gold-dark))",
                            },
                            crimson: {
                                DEFAULT: "hsl(var(--crimson))",
                                light: "hsl(var(--crimson-light))",
                            },
                            cream: "hsl(var(--cream))",
                            ink: "hsl(var(--ink))",
                        },
                        fontFamily: {
                            display: ["Playfair Display", "serif"],
                            body: ["Source Sans 3", "sans-serif"],
                        },
                        borderRadius: {
                            lg: "var(--radius)",
                            md: "calc(var(--radius) - 2px)",
                            sm: "calc(var(--radius) - 4px)",
                        },
                        keyframes: {
                            "fade-in-up": {
                                from: { opacity: "0", transform: "translateY(30px)" },
                                to:   { opacity: "1", transform: "translateY(0)" },
                            },
                            "fade-in-left": {
                                from: { opacity: "0", transform: "translateX(-40px)" },
                                to:   { opacity: "1", transform: "translateX(0)" },
                            },
                            "fade-in-right": {
                                from: { opacity: "0", transform: "translateX(40px)" },
                                to:   { opacity: "1", transform: "translateX(0)" },
                            },
                            float: {
                                "0%, 100%": { transform: "translateY(0)" },
                                "50%":      { transform: "translateY(-12px)" },
                            },
                            shimmer: {
                                "100%": { transform: "translateX(100%)" },
                            },
                            reveal: {
                                "0%": { "clip-path": "inset(0 100% 0 0)" },
                                "100%": { "clip-path": "inset(0 0 0 0)" },
                            }
                        },
                        animation: {
                            "fade-in-up": "fade-in-up 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards",
                            "fade-in-left": "fade-in-left 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards",
                            "fade-in-right": "fade-in-right 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards",
                            float: "float 4s ease-in-out infinite",
                            reveal: "reveal 1.2s cubic-bezier(0.77, 0, 0.175, 1) forwards",
                        },
                    },
                },
            }
        </script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400;1,500&family=Source+Sans+3:wght@300;400;500;600;700&display=swap');

            :root {
                --background: 30 25% 97%;
                --foreground: 15 30% 12%;
                --card: 30 20% 95%;
                --card-foreground: 15 30% 12%;
                --popover: 30 25% 97%;
                --popover-foreground: 15 30% 12%;
                --primary: 0 72% 38%;
                --primary-foreground: 40 60% 95%;
                --secondary: 35 60% 52%;
                --secondary-foreground: 15 30% 12%;
                --muted: 30 15% 90%;
                --muted-foreground: 15 10% 45%;
                --accent: 40 75% 55%;
                --accent-foreground: 15 30% 12%;
                --destructive: 0 84.2% 60.2%;
                --destructive-foreground: 210 40% 98%;
                --border: 25 20% 85%;
                --input: 25 20% 85%;
                --ring: 0 72% 38%;
                --radius: 0.625rem;
                --gold: 40 75% 55%;
                --gold-light: 40 70% 75%;
                --gold-dark: 35 65% 40%;
                --crimson: 0 72% 38%;
                --crimson-light: 0 60% 55%;
                --cream: 35 40% 94%;
                --ink: 15 30% 12%;
                --terracotta: 15 55% 48%;
                --jade: 160 35% 35%;
                --gradient-hero: linear-gradient(135deg, hsl(0 72% 38%), hsl(0 72% 28%), hsl(35 60% 30%));
                --gradient-gold: linear-gradient(135deg, hsl(40 75% 55%), hsl(35 65% 40%));
                --gradient-warm: linear-gradient(180deg, hsl(30 25% 97%), hsl(35 40% 94%));
                --shadow-card: 0 4px 24px -4px hsl(15 30% 12% / 0.08);
                --shadow-elevated: 0 12px 40px -8px hsl(15 30% 12% / 0.15);
            }

            .dark {
                --background: 15 20% 8%;
                --foreground: 30 20% 92%;
                --card: 15 18% 12%;
                --card-foreground: 30 20% 92%;
                --popover: 15 18% 12%;
                --popover-foreground: 30 20% 92%;
                --primary: 0 65% 50%;
                --primary-foreground: 30 20% 95%;
                --secondary: 35 55% 45%;
                --secondary-foreground: 30 20% 92%;
                --muted: 15 15% 18%;
                --muted-foreground: 25 12% 55%;
                --accent: 40 65% 50%;
                --accent-foreground: 15 20% 8%;
                --destructive: 0 62.8% 30.6%;
                --destructive-foreground: 210 40% 98%;
                --border: 15 15% 22%;
                --input: 15 15% 22%;
                --ring: 0 65% 50%;
                --gold: 40 65% 50%;
                --gold-light: 40 55% 60%;
                --gold-dark: 35 55% 35%;
                --crimson: 0 65% 50%;
                --crimson-light: 0 55% 60%;
                --cream: 15 12% 15%;
                --ink: 30 20% 92%;
                --terracotta: 15 50% 55%;
                --jade: 160 30% 40%;
                --gradient-hero: linear-gradient(135deg, hsl(0 65% 25%), hsl(0 50% 15%), hsl(15 20% 8%));
                --gradient-gold: linear-gradient(135deg, hsl(40 65% 50%), hsl(35 55% 35%));
                --gradient-warm: linear-gradient(180deg, hsl(15 20% 8%), hsl(15 18% 12%));
                --shadow-card: 0 4px 24px -4px hsl(0 0% 0% / 0.3);
                --shadow-elevated: 0 12px 40px -8px hsl(0 0% 0% / 0.5);
            }

            /* Reset */
            *, *::before, *::after { box-sizing: border-box; }

            html, body {
                margin: 0;
                padding: 0;
                width: 100%;
                overflow-x: hidden;
                background-color: hsl(var(--background));
                color: hsl(var(--foreground));
                font-family: 'Source Sans 3', sans-serif;
            }

            /* =============================================
               QUASAR LAYOUT RESET
               Force standard document block flow to avoid 100vh flex lock
               and overlapping footer issues.
            ============================================= */
            .q-layout,
            .q-page-container,
            .q-page {
                display: block !important;
                min-height: auto !important;
                overflow: visible !important;
            }

            /* Xóa toàn bộ padding Quasar inject cho sidebar/header */
            .q-page-container {
                padding: 0 !important;
            }

            .q-page {
                padding: 0 !important;
                min-height: unset !important;
            }

            /* NiceGUI bọc content trong div.nicegui-content */
            .nicegui-content {
                display: flex !important;
                flex-direction: column !important;
                min-height: 100vh !important;
                padding: 0 !important;
                margin: 0 !important;
                gap: 0 !important;
                align-items: stretch !important;
                width: 100% !important;
            }

            /* header/footer semantic tags */
            body > .q-layout header,
            .nicegui-content > header {
                flex-shrink: 0;
                width: 100%;
                position: sticky;
                top: 0;
                z-index: 50;
            }

            /* Ensure footer stays at bottom and is full width */
            .nicegui-content > footer {
                flex-shrink: 0 !important;
                width: 100% !important;
                margin-top: auto !important;
                display: block !important;
            }

            /* main giữa header và footer */
            .nicegui-content > main {
                flex: 1 0 auto !important;
                display: flex !important;
                flex-direction: column !important;
                align-items: stretch !important;
                width: 100% !important;
            }

            /* Tất cả section/div con trực tiếp của main full width */
            .nicegui-content > main > * {
                width: 100% !important;
            }

            /* =============================================
               UTILITY
            ============================================= */
            .text-gradient-gold {
                background: var(--gradient-gold);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            .bg-hero-gradient  { background: var(--gradient-hero); }
            .bg-warm-gradient  { background: var(--gradient-warm); }
            .shadow-card       { box-shadow: var(--shadow-card); }
            .shadow-elevated   { box-shadow: var(--shadow-elevated); }

            /* Advanced Skeleton Shimmer */
            .skeleton-shimmer {
                position: relative;
                overflow: hidden;
                background-color: hsl(var(--muted));
            }
            .skeleton-shimmer::after {
                content: "";
                position: absolute;
                inset: 0;
                transform: translateX(-100%);
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
                animation: shimmer 1.5s infinite;
            }

            /* Cultural Background Pattern */
            .bg-pattern-lotus {
                background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M30 5c-5 0-9 4-9 9 0 4 3 8 7 9-4 1-7 5-7 9 0 5 4 9 9 9s9-4 9-9c0-4-3-8-7-9 4-1 7-5 7-9 0-5-4-9-9-9zm0 2c3.9 0 7 3.1 7 7 0 3.3-2.3 6.1-5.4 6.8-.4-1.1-.9-2.1-1.6-3.1 2.2-.6 4-2.4 4-4.7 0-2.8-2.2-5-5-5s-5 2.2-5 5c0 2.3 1.8 4.1 4 4.7-.7 1-1.2 2-1.6 3.1-3.1-.7-5.4-3.5-5.4-6.8 0-3.9 3.1-7 7-7zm0 18c3.9 0 7 3.1 7 7 0 3.3-2.3 6.1-5.4 6.8-.4-1.1-.9-2.1-1.6-3.1 2.2-.6 4-2.4 4-4.7 0-2.8-2.2-5-5-5s-5 2.2-5 5c0 2.3 1.8 4.1 4 4.7-.7 1-1.2 2-1.6 3.1-3.1-.7-5.4-3.5-5.4-6.8 0-3.9 3.1-7 7-7z' fill='%23b21e1e' fill-opacity='0.03' fill-rule='evenodd'/%3E%3C/svg%3E");
            }
            
            .silk-thread {
                stroke-dasharray: 1000;
                stroke-dashoffset: 1000;
                animation: draw-silk 3s ease-out forwards;
            }
            @keyframes draw-silk {
                to { stroke-dashoffset: 0; }
            }

            ::-webkit-scrollbar       { width: 8px; }
            ::-webkit-scrollbar-track { background: hsl(var(--background)); }
            ::-webkit-scrollbar-thumb {
                background: hsl(var(--primary) / 0.3);
                border-radius: 10px;
            }
            ::-webkit-scrollbar-thumb:hover { background: hsl(var(--primary) / 0.5); }
        </style>
    ''')

    ui.dark_mode().disable()
    ui.colors(
        primary='#b21e1e',
        secondary='#d68e33',
        accent='#d68e33',
        dark='#140f0c',
    )


def container():
    """Centered max-width wrapper."""
    return ui.element('div').classes('mx-auto px-4 w-full max-w-[1400px]')


from contextlib import contextmanager

@contextmanager
def frame():
    import components  # late import to avoid circular dependency
    apply_theme()
    
    # Header
    components.navbar()
    
    # Main Content
    with ui.element('main'):
        yield
        
    # Footer and Chatbot
    components.chatbot_persona()
    components.footer()