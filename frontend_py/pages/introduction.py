from nicegui import ui
import theme
import components

@ui.page('/gioi-thieu')
def introduction_page():
    with theme.frame():

        # ── Hero Section ────────────────────────────────────────────────────
        with ui.element('section').classes(
            'relative min-h-[50vh] flex items-center justify-center overflow-hidden w-full'
        ).style('padding-top: 56px;'):
            ui.image('/static/hero-banner.jpg').classes('absolute inset-0 h-full w-full object-cover')
            ui.element('div').classes('absolute inset-0 bg-hero-gradient opacity-80')
            with ui.column().classes('relative z-10 text-center items-center px-4 gap-4'):
                ui.label('LỊCH SỬ VÀ GIÁ TRỊ VĂN HÓA').classes(
                    'text-[10px] font-bold tracking-[0.4em] text-gold-light uppercase animate-fade-in'
                )
                with ui.column().classes('gap-1 animate-fade-in-up'):
                    ui.label('Giới thiệu').classes('font-display text-2xl md:text-3xl font-bold text-white/90 shadow-sm')
                    ui.label('Quan Họ Bắc Ninh').classes('font-display text-4xl md:text-7xl font-black text-gradient-gold drop-shadow-2xl')

        # ── About + Features Section ─────────────────────────────────────────
        with ui.element('section').classes('py-16 bg-background w-full relative overflow-hidden'):
            ui.image('/static/lotus-ornament.png').classes(
                'absolute -left-20 -top-20 w-64 h-64 opacity-[0.03] rotate-12 pointer-events-none'
            )
            with theme.container():
                components.section_title('Quan họ là gì?')
                with ui.column().classes('max-w-4xl mx-auto text-center items-center gap-6 mb-16'):
                    ui.label(
                        'Dân ca Quan họ Bắc Ninh là một hình thức hát giao duyên đối đáp giữa nam (liền anh) '
                        'và nữ (liền chị), phổ biến tại vùng Kinh Bắc xưa.'
                    ).classes('text-muted-foreground text-lg leading-relaxed font-light')
                    ui.label(
                        'Năm 2009, Quan họ được UNESCO vinh danh là Di sản Văn hóa Phi vật thể đại diện của '
                        'Nhân loại, khẳng định sức sống mãnh liệt của di sản.'
                    ).classes('bg-primary/5 px-6 py-4 rounded-2xl border border-primary/10 text-foreground italic text-sm md:text-base')

                with ui.row().classes('grid gap-6 md:grid-cols-3 w-full items-stretch'):
                    components.intro_feature_card('music_note', 'Lề lối giao duyên', 'Lối hát đối đáp nam nữ với kỹ thuật "Vang, Rền, Nền, Nảy" điêu luyện.')
                    components.intro_feature_card('groups', 'Tục kết chạ', 'Sự gắn kết thiêng liêng giữa các làng Quan họ, tạo nên cộng đồng bền chặt.')
                    components.intro_feature_card('favorite', 'Liền anh, Liền chị', 'Cách xưng hô đầy trân trọng thể hiện nét văn hóa ứng xử Kinh Bắc thanh lịch.')

        # ── Costume Section ──────────────────────────────────────────────────
        with ui.element('section').classes('py-20 bg-background/50 border-y border-border w-full relative overflow-hidden'):
            ui.label('TRUYỀN THỐNG').classes(
                'absolute -right-20 top-20 text-[12vw] font-black text-primary/5 select-none pointer-events-none uppercase'
            )
            with theme.container():
                components.section_title('Trang Phục Truyền Thống', 'Nét đặc trưng làm nên linh hồn của dân ca Quan họ.')
                with ui.column().classes('mt-12 gap-12 w-full'):
                    components.costume_block(
                        'Trang phục Liền chị',
                        'Nổi bật với áo mớ ba mớ bảy, nón quai thao thắt dải lụa thướt tha mang vẻ đẹp dịu dàng kiêu sa đặc trưng của người con gái Kinh Bắc.',
                        '/static/costume_lien_chi.png',
                        items=['Áo mớ ba mớ bảy (Silk layers)', 'Nón quai thao (Palm hat)', 'Khăn mỏ quạ (Headscarf)'],
                    )
                    components.costume_block(
                        'Trang phục Liền anh',
                        'Đậm chất nam nhi Kinh Bắc với áo the đen, quần lụa trắng, khăn xếp và chiếc ô đen che nghiêng thể hiện phong thái thanh lịch.',
                        '/static/costume_lien_anh.png',
                        items=['Áo the thâm (Black robe)', 'Khăn xếp (Layered wrap)', 'Ô đen (Traditional umbrella)'],
                        reverse=True,
                    )

        # ── History Timeline ─────────────────────────────────────────────────
        with ui.element('section').classes('py-20 bg-background w-full'):
            with theme.container().classes('max-w-6xl'):
                components.section_title('Dòng chảy lịch sử', 'Hành trình kiến tạo nên tâm hồn người Việt.')

                timeline_data = [
                    ('Thế kỷ XV',        'Bắt đầu hình thành tại vùng vựa lúa Kinh Bắc.'),
                    ('Thế kỷ XVII-XVIII', 'Thời kỳ phát triển rực rỡ nhất với hệ thống làng Quan họ.'),
                    ('Thế kỷ XIX',        'Trở thành biểu tượng văn hóa tiêu biểu nhất của xứ Bắc.'),
                    ('2009',              'Vinh danh là Di sản văn hóa phi vật thể của nhân loại.'),
                ]

                # Wrapper có position:relative để chứa đường kẻ dọc tuyệt đối
                with ui.element('div').classes('relative mt-12 w-full'):

                    # ── Đường kẻ dọc ở GIỮA (left: 50%) ──────────────────
                    # Dùng div thay SVG: left-1/2 + -translate-x-1/2 đảm bảo
                    # luôn thẳng hàng với cột center 10% của timeline_item
                    ui.element('div').classes(
                        'absolute top-0 bottom-0 left-1/2 -translate-x-1/2 '
                        'w-px pointer-events-none z-0'
                    ).style(
                        'background: linear-gradient('
                        '  to bottom,'
                        '  transparent 0%,'
                        '  hsl(0 72% 38% / 0.5) 4%,'
                        '  hsl(0 72% 38% / 0.5) 96%,'
                        '  transparent 100%'
                        ');'
                    )

                    # ── Các mốc timeline ───────────────────────────────────
                    for i, (year, text) in enumerate(timeline_data):
                        components.timeline_item(year, text, index=i, total=len(timeline_data))

        # ── Quote Section ────────────────────────────────────────────────────
        with ui.element('section').classes('py-16 bg-card border-t border-border w-full'):
            with theme.container().classes('max-w-4xl text-center items-center'):
                components.unesco_quote(
                    'Dân ca Quan họ Bắc Ninh thể hiện tính cộng đồng, sự chia sẻ và lòng mến khách của người dân Việt Nam.',
                    subtitle='GIÁ TRỊ DI SẢN NHÂN LOẠI'
                )