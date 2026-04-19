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
                            jade: "hsl(var(--jade))",
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
                            },
                            "slow-zoom": {
                                "0%": { transform: "scale(1)" },
                                "100%": { transform: "scale(1.1)" },
                            }
                        },
                        animation: {
                            "fade-in-up": "fade-in-up 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards",
                            "fade-in-left": "fade-in-left 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards",
                            "fade-in-right": "fade-in-right 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards",
                            float: "float 4s ease-in-out infinite",
                            reveal: "reveal 1.2s cubic-bezier(0.77, 0, 0.175, 1) forwards",
                            "slow-zoom": "slow-zoom 20s ease-in-out infinite alternate",
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

            /* Đặt lại CSS */
            *, *::before, *::after { box-sizing: border-box; }

            html {
                font-size: 14px;
                scroll-behavior: smooth;
            }
            @media (min-width: 768px) {
                html { font-size: 16px; }
            }
            @media (min-width: 1440px) {
                html { font-size: 17px; }
            }

            html, body {
                margin: 0;
                padding: 0;
                width: 100%;
                max-width: 100vw;
                overflow-x: hidden;
                background-color: hsl(var(--background));
                color: hsl(var(--foreground));
                font-family: 'Source Sans 3', sans-serif;
                -webkit-tap-highlight-color: transparent;
            }

            /* Fix cho ảnh NiceGUI/Quasar */
            img {
                max-width: 100%;
                height: auto;
                display: block;
            }
            .q-img__image {
                object-fit: cover !important;
            }
            .q-img {
                height: 100%;
            }

            /* Nút responsive cho mọi thiết bị */
            .q-btn, button, .cursor-pointer {
                min-height: 44px;
                min-width: 44px;
            }
            .nicegui-content button {
                touch-action: manipulation;
            }

            .w-full { width: 100% !important; max-width: 100vw; }

            /* =============================================
       ĐẶT LẠI LAYOUT QUASAR
       Đảm bảo cuộn tài liệu tiêu chuẩn bằng cách loại bỏ khóa 100vh
    ============================================= */
    .q-layout,
    .q-page-container,
    .q-page {
        min-height: auto !important;
    }

    .q-page-container {
        padding: 0 !important;
    }

    .q-page {
        padding: 0 !important;
        display: block !important;
    }

    /* Wrapper nội dung NiceGUI */
    .nicegui-content {
        display: flex !important;
        flex-direction: column !important;
        min-height: 100vh !important;
        padding: 0 !important;
        margin: 0 !important;
        gap: 0 !important;
        width: 100% !important;
        overflow-x: hidden;
    }

    /* Header cố định */
    .qh-navbar {
        position: fixed !important;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 1000;
        background: rgba(255, 248, 240, 0.82) !important;
        backdrop-filter: blur(24px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(24px) saturate(180%) !important;
        border-bottom: 1px solid rgba(180, 120, 60, 0.1) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
        transition: all 0.3s ease;
    }

    /* Main area grows to fill space */
    .nicegui-content > main {
        flex: 1 0 auto !important;
        display: flex !important;
        flex-direction: column !important;
        width: 100% !important;
        padding-top: 56px; /* Khoảng cách cho navbar cố định */
    }

    /* Footer không bị ẩn */
    .nicegui-content > footer {
        flex-shrink: 0 !important;
        width: 100% !important;
        margin-top: auto !important;
    }

    .nicegui-content > main > * {
        width: 100% !important;
    }

    /* =============================================
       TIỆN ÍCH
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

            /* Hiệu ứng Skeleton Shimmer */
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

            /* Hình nền văn hóa */
            .bg-pattern-lotus {
                background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M30 5c-5 0-9 4-9 9 0 4 3 8 7 9-4 1-7 5-7 9 0 5 4 9 9 9s9-4 9-9c0-4-3-8-7-9 4-1 7-5 7-9 0-5-4-9-9-9zm0 2c3.9 0 7 3.1 7 7 0 3.3-2.3 6.1-5.4 6.8-.4-1.1-.9-2.1-1.6-3.1 2.2-.6 4-2.4 4-4.7 0-2.8-2.2-5-5-5s-5 2.2-5 5c0 2.3 1.8 4.1 4 4.7-.7 1-1.2 2-1.6 3.1-3.1-.7-5.4-3.5-5.4-6.8 0-3.9 3.1-7 7-7zm0 18c3.9 0 7 3.1 7 7 0 3.3-2.3 6.1-5.4 6.8-.4-1.1-.9-2.1-1.6-3.1 2.2-.6 4-2.4 4-4.7 0-2.8-2.2-5-5-5s-5 2.2-5 5c0 2.3 1.8 4.1 4 4.7-.7 1-1.2 2-1.6 3.1-3.1-.7-5.4-3.5-5.4-6.8 0-3.9 3.1-7 7-7z' fill='%23b21e1e' fill-opacity='0.03' fill-rule='evenodd'/%3E%3C/svg%3E");
            }
            
            /* Hình ảnh giấy Dó cổ */
            .bg-paper-texture {
                background-color: #fdfcf0;
                background-image: 
                    radial-gradient(at 0% 0%, rgba(255, 255, 255, 0.5) 0, transparent 50%),
                    url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
                background-blend-mode: overlay;
                opacity: 0.98;
            }

            /* Con dấu Triện Đỏ truyền thống */
            .seal-stamped {
                background: linear-gradient(135deg, #b21e1e 0%, #8b0000 100%);
                box-shadow: inset 0 0 10px rgba(0,0,0,0.2), 2px 2px 5px rgba(0,0,0,0.3);
                position: relative;
                overflow: hidden;
            }
            .seal-stamped::after {
                content: '';
                position: absolute;
                inset: 0;
                background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100' height='100' filter='url(%23noise)' opacity='0.2'/%3E%3C/svg%3E");
                pointer-events: none;
            }

            .silk-thread {
                stroke-dasharray: 1000;
                stroke-dashoffset: 1000;
                animation: draw-silk 3s ease-out forwards;
            }
            @keyframes draw-silk {
                to { stroke-dashoffset: 0; }
            }

            /* Thành phần tìm kiếm UI hiện đại */
            .modern-search-card {
                background: rgba(255, 255, 255, 0.6) !important;
                backdrop-filter: blur(12px) saturate(180%);
                -webkit-backdrop-filter: blur(12px) saturate(180%);
                border: 1px solid rgba(180, 120, 60, 0.2) !important;
                box-shadow: 0 8px 32px 0 rgba(180, 120, 60, 0.1);
                transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            }
            .modern-search-card:hover {
                background: rgba(255, 255, 255, 0.95) !important;
                box-shadow: 0 15px 35px -5px rgba(180, 120, 60, 0.25);
            }

            .glass-card {
                background: rgba(255, 255, 255, 0.45) !important;
                backdrop-filter: blur(20px) saturate(180%);
                -webkit-backdrop-filter: blur(20px) saturate(180%);
                border: 1px solid rgba(255, 255, 255, 0.3) !important;
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
            }
            
            .modern-input .q-field__control {
                background: rgba(255, 255, 255, 0.5) !important;
                border: 1px solid rgba(180, 120, 60, 0.2) !important;
                border-radius: 16px !important;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
                padding: 4px 12px !important;
            }
            .modern-input .q-field--focused .q-field__control {
                background: white !important;
                box-shadow: 0 0 0 4px rgba(178, 30, 30, 0.1) !important;
                border-color: rgba(178, 30, 30, 0.8) !important;
                transform: translateY(-1px);
            }
            .modern-input .q-field__label {
                color: hsl(var(--muted-foreground)) !important;
                font-weight: 500;
            }

            .elevated-btn {
                transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
            }
            .elevated-btn:hover {
                transform: translateY(-3px) scale(1.02);
                box-shadow: 0 10px 20px -10px rgba(178, 30, 30, 0.5) !important;
            }
            .elevated-btn:active {
                transform: translateY(1px) scale(0.98);
            }

            .cultural-header-line {
                position: relative;
                padding-bottom: 0.5rem;
            }
            .cultural-header-line::after {
                content: '';
                position: absolute;
                bottom: 0;
                left: 0;
                width: 40px;
                height: 3px;
                background: var(--gradient-gold);
                border-radius: 2px;
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
    """Centered max-width wrapper with responsive padding."""
    return ui.element('div').classes('mx-auto px-4 sm:px-6 lg:px-8 w-full max-w-[1400px]')


from contextlib import contextmanager

@contextmanager
def frame():
    import components  # import trễ để tránh circular dependency
    apply_theme()
    
    # Header
    components.navbar()
    
    # Nội dung chính
    with ui.element('main'):
        yield
        
    # Footer và Chatbot
    components.chatbot_persona()
    components.footer()