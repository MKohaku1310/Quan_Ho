from nicegui import ui, app
from components import base
from api import api_client
from translation import t
import theme
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class ShopState:
    page: int = 1
    items_per_page: int = 12
    category: Optional[str] = None
    search: str = ""
    cart: Dict[int, Dict[str, Any]] = field(default_factory=dict) # product_id -> {product, quantity}
    is_checking_out: bool = False

state = ShopState()

@ui.page('/cua-hang', response_timeout=60.0)
async def shop():
    with theme.frame():
        # Style cho cart badge
        ui.add_head_html('''
            <style>
                .cart-badge {
                    position: absolute;
                    top: -4px;
                    right: -4px;
                    background-color: #b21e1e;
                    color: white;
                    border-radius: 999px;
                    min-width: 20px;
                    height: 20px;
                    padding: 0 4px;
                    font-size: 11px;
                    font-weight: 800;
                    border: 2px solid white;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                    z-index: 60;
                }
                .product-card {
                    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                }
                .product-card:hover {
                    transform: translateY(-8px);
                    box-shadow: 0 20px 25px -5px rgba(178, 30, 30, 0.1), 0 10px 10px -5px rgba(178, 30, 30, 0.04);
                }
                /* Cart drawer premium styles */
                .cart-drawer-dialog .q-dialog__inner--minimized {
                    padding: 0 !important;
                }
                .cart-drawer-dialog .q-dialog__inner--minimized > div {
                    max-height: 100vh !important;
                    height: 100vh !important;
                }
                .cart-item-card {
                    transition: all 0.3s ease;
                    position: relative;
                    overflow: hidden;
                }
                .cart-item-card::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 4px;
                    height: 100%;
                    background: linear-gradient(180deg, #b21e1e, #d4443c);
                    border-radius: 4px 0 0 4px;
                    opacity: 0;
                    transition: opacity 0.3s ease;
                }
                .cart-item-card:hover::before {
                    opacity: 1;
                }
                .cart-item-card:hover {
                    transform: translateX(4px);
                    box-shadow: 0 8px 25px -5px rgba(178, 30, 30, 0.12);
                }
                .cart-qty-control {
                    background: linear-gradient(135deg, #fef2f2, #fff5f5);
                    border: 1px solid rgba(178, 30, 30, 0.1);
                }
                .cart-footer-gradient {
                    background: linear-gradient(180deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.95) 15%, #ffffff 100%);
                }
                .checkout-btn {
                    background: linear-gradient(135deg, #b21e1e 0%, #8b1515 100%) !important;
                    position: relative;
                    overflow: hidden;
                }
                .checkout-btn::after {
                    content: '';
                    position: absolute;
                    top: -50%;
                    left: -50%;
                    width: 200%;
                    height: 200%;
                    background: linear-gradient(45deg, transparent 40%, rgba(255,255,255,0.1) 50%, transparent 60%);
                    animation: btn-shine 3s infinite;
                }
                @keyframes btn-shine {
                    0% { transform: translateX(-100%) rotate(45deg); }
                    100% { transform: translateX(100%) rotate(45deg); }
                }
            </style>
        ''')

        @ui.refreshable
        async def product_grid():
            products = await api_client.get_products(
                skip=(state.page - 1) * state.items_per_page,
                limit=state.items_per_page,
                category=state.category if state.category != 'all' else None,
                search=state.search
            )
            total_count = await api_client.get_products_count(
                category=state.category if state.category != 'all' else None,
                search=state.search
            )

            if not products:
                with ui.column().classes('w-full items-center justify-center py-32 gap-6 opacity-40'):
                    ui.icon('inventory_2', size='80px').classes('text-muted-foreground')
                    with ui.column().classes('items-center gap-1'):
                        ui.label(t('no_products_found')).classes('text-2xl font-bold tracking-tight')
                        ui.label('Dạ, em chưa tìm thấy sản phẩm này, Quý khách vui lòng chọn mục khác nhé!').classes('text-sm italic')
                return

            def show_product_detail(p):
                with ui.dialog() as detail_dialog, ui.card().classes('p-0 rounded-[40px] border-none shadow-2xl overflow-hidden max-w-2xl w-full'):
                    with ui.row().classes('w-full h-[300px] relative'):
                        ui.image(p.get('image_url') or '/static/common/default-product.png').classes('w-full h-full object-cover')
                        ui.button(icon='close', on_click=detail_dialog.close).props('flat round color=white').classes('absolute top-4 right-4 bg-black/20 backdrop-blur-md')
                    
                    with ui.column().classes('p-10 gap-6'):
                        with ui.column().classes('gap-2'):
                            ui.label(t(f"cat_{p.get('category')}")).classes('text-primary text-[10px] font-black uppercase tracking-[0.2em]')
                            ui.label(p['name']).classes('text-3xl font-black text-foreground leading-tight')
                            ui.label("{:,.0f} VNĐ".format(p['price'])).classes('text-primary text-2xl font-black')
                        
                        ui.label(p['description']).classes('text-base text-muted-foreground leading-[1.8] text-justify')
                        
                        with ui.row().classes('w-full items-center justify-between pt-6 border-t border-border/40 mt-4'):
                            ui.label(f"Số lượng trong kho: {p.get('stock', 0)}").classes('text-sm font-bold text-muted-foreground italic')
                            ui.button(t('add_to_cart'), icon='add_shopping_cart', on_click=lambda: (add_to_cart(p), detail_dialog.close())) \
                                .props('unelevated rounded-full size=lg') \
                                .classes('bg-primary text-white font-bold px-8 shadow-xl shadow-primary/20')
                detail_dialog.open()

            with ui.element('div').classes('grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8 w-full px-4'):
                for p in products:
                    with ui.card().classes('product-card overflow-hidden rounded-3xl border border-border/40 bg-card group p-0 cursor-pointer') \
                        .on('click', lambda e, p=p: show_product_detail(p)):
                        # Image container
                        with ui.element('div').classes('relative h-64 w-full overflow-hidden'):
                            ui.image(p.get('image_url') or '/static/common/default-product.png').classes('h-full w-full object-cover transition-transform duration-700 group-hover:scale-110')
                            with ui.element('div').classes('absolute top-4 left-4'):
                                cat_key = f"cat_{p.get('category')}"
                                ui.label(t(cat_key)).classes('bg-white/90 backdrop-blur-sm text-primary text-[10px] font-black px-3 py-1 rounded-full shadow-sm uppercase tracking-wider')
                        
                        # Content
                        with ui.column().classes('p-6 gap-3'):
                            with ui.column().classes('gap-1'):
                                ui.label(p.get('name')).classes('text-lg font-bold text-foreground line-clamp-1 group-hover:text-primary transition-colors')
                                price_formatted = "{:,.0f} VNĐ".format(p.get('price', 0))
                                ui.label(price_formatted).classes('text-primary font-black text-xl')
                            
                            ui.label(p.get('description')).classes('text-sm text-muted-foreground line-clamp-2 min-h-[40px] leading-relaxed')
                            
                            with ui.row().classes('w-full justify-between items-center mt-4 pt-4 border-t border-border/40'):
                                stock = p.get('stock', 0)
                                if stock > 0:
                                    ui.label(f"Stock: {stock}").classes('text-[10px] font-bold text-muted-foreground uppercase tracking-widest')
                                    ui.button(icon='add_shopping_cart') \
                                        .on('click.stop', lambda e, p=p: add_to_cart(p)) \
                                        .props('unelevated round size=md') \
                                        .classes('bg-primary text-white shadow-lg hover:rotate-12 transition-all')
                                else:
                                    ui.label(t('out_of_stock')).classes('text-[10px] font-bold text-destructive uppercase tracking-widest')
                                    ui.button(icon='block', on_click=None).props('flat round size=md disabled').classes('text-muted-foreground opacity-30')

            base.pagination_controls(state, total_count, product_grid)

        # Helper to get/set user cart
        def get_cart() -> Dict[str, Any]:
            cart = app.storage.user.get('cart')
            if not isinstance(cart, dict):
                app.storage.user['cart'] = {}
                return app.storage.user['cart']
            
            # Clean up invalid entries immediately
            invalid_keys = []
            for k, v in cart.items():
                if not isinstance(v, dict) or not isinstance(v.get('product'), dict):
                    invalid_keys.append(k)
            
            if invalid_keys:
                for k in invalid_keys:
                    del cart[k]
                app.storage.user['cart'] = cart
                
            return cart

        def add_to_cart(product):
            cart = get_cart()
            pid = str(product['id'])
            current_qty = cart.get(pid, {}).get('quantity', 0)
            if current_qty >= product.get('stock', 0):
                ui.notify(t('out_of_stock'), type='warning')
                return
                
            if pid in cart:
                cart[pid]['quantity'] += 1
            else:
                cart[pid] = {'product': product, 'quantity': 1}
            app.storage.user.update(cart=cart) # Force persistence
            ui.notify(f"Đã thêm vào giỏ: {product['name']}", type='positive', icon='shopping_cart')
            cart_items_list.refresh()
            cart_summary_footer.refresh()
            floating_cart.refresh()

        # Floating Cart Button (More visible)
        @ui.refreshable
        def floating_cart():
            cart = get_cart()
            count = sum(item.get('quantity', 0) if isinstance(item, dict) else 0 for item in cart.values())
            with ui.button(on_click=lambda: cart_drawer.open()) \
                .props('round size=lg') \
                .classes('fixed bottom-36 right-8 z-50 bg-primary text-white shadow-2xl hover:scale-110 transition-all border-4 border-white/20'):
                ui.icon('shopping_cart', size='28px')
                if count > 0:
                    ui.html(f'<span class="cart-badge">{count}</span>')

        @ui.refreshable
        def cart_items_list():
            try:
                cart = get_cart()
                if not cart:
                    with ui.column().classes('items-center justify-center py-24 gap-10'):
                        with ui.element('div').classes('w-36 h-36 rounded-full flex items-center justify-center').style('background: linear-gradient(135deg, #fef2f2, #fce4e4);'):
                            ui.icon('shopping_basket', size='56px').classes('text-primary/30')
                        with ui.column().classes('items-center gap-3'):
                            ui.label(t('empty_cart')).classes('font-black text-xl tracking-tight text-foreground/30 uppercase')
                            ui.label('Giỏ hàng đang trống, mời Quý khách chọn sản phẩm ưng ý nhé!').classes('text-sm italic text-muted-foreground text-center max-w-[280px] leading-relaxed')
                        ui.button('TIẾP TỤC MUA SẮM', on_click=lambda: cart_drawer.close(), icon='arrow_back') \
                            .props('outline rounded-full size=md') \
                            .classes('mt-2 text-primary border-primary/20 font-bold px-8 hover:bg-primary/5 transition-all')
                    return

                # Item count header
                item_count = sum(1 for v in cart.values() if isinstance(v, dict) and isinstance(v.get('product'), dict))
                with ui.row().classes('w-full items-center gap-2 mb-2'):
                    ui.icon('inventory_2', size='16px').classes('text-muted-foreground/50')
                    ui.label(f'{item_count} sản phẩm').classes('text-xs font-bold text-muted-foreground/50 uppercase tracking-widest')

                for pid, item in list(cart.items()):
                    if not isinstance(item, dict):
                        del cart[pid]
                        app.storage.user['cart'] = cart
                        continue
                        
                    p = item.get('product')
                    if not isinstance(p, dict):
                        del cart[pid]
                        app.storage.user['cart'] = cart
                        continue
                        
                    qty = int(item.get('quantity') or 1)
                    price = float(p.get('price') or 0)
                    subtotal = price * qty
                    
                    with ui.card().classes('cart-item-card w-full p-0 rounded-2xl bg-white border border-border/10 shadow-sm'):
                        # Product name & remove button row at top
                        with ui.row().classes('w-full justify-between items-start px-4 pt-3 pb-0'):
                            ui.label(p.get('name', 'Sản phẩm')).classes('font-bold text-sm line-clamp-1 text-foreground leading-snug flex-1 mr-2')
                            ui.button(icon='close', on_click=lambda e, pid=pid: remove_from_cart(pid)) \
                                .props('flat round dense size=xs') \
                                .classes('text-muted-foreground/30 hover:text-destructive hover:bg-destructive/5 transition-all')
                        
                        with ui.row().classes('w-full items-center gap-4 px-4 pb-3 pt-2'):
                            # Small product image
                            ui.image(p.get('image_url') or '/static/common/default-product.png') \
                                .classes('w-16 h-16 rounded-xl object-cover shrink-0')
                            
                            # Price + Qty + Subtotal
                            with ui.column().classes('flex-1 gap-2'):
                                ui.label("{:,.0f}đ".format(price)).classes('text-primary/70 text-xs font-semibold')
                                with ui.row().classes('w-full items-center justify-between'):
                                    # Quantity controls
                                    with ui.row().classes('cart-qty-control items-center gap-0 rounded-lg overflow-hidden'):
                                        ui.button(icon='remove', on_click=lambda e, pid=pid: update_qty(pid, -1)) \
                                            .props('flat dense size=sm square') \
                                            .classes('text-primary/70 w-8 h-8 hover:bg-primary/10 transition-all')
                                        ui.label(str(qty)).classes('font-black text-sm min-w-[28px] text-center text-foreground')
                                        ui.button(icon='add', on_click=lambda e, pid=pid: update_qty(pid, 1)) \
                                            .props('flat dense size=sm square') \
                                            .classes('text-primary/70 w-8 h-8 hover:bg-primary/10 transition-all')
                                    
                                    # Subtotal
                                    ui.label("{:,.0f}đ".format(subtotal)).classes('font-black text-base text-primary')
            except Exception as e:
                import traceback
                traceback.print_exc()
                with ui.column().classes('w-full items-center justify-center p-8'):
                    ui.label('Đã xảy ra lỗi khi tải giỏ hàng!').classes('text-lg font-bold text-destructive')
                    ui.label(str(e)).classes('text-xs text-red-400 font-mono mt-2')
                    ui.button('Xóa giỏ hàng & Thử lại', on_click=lambda: (app.storage.user.update(cart={}), cart_items_list.refresh())).classes('mt-4 bg-primary text-white rounded-full')

        @ui.refreshable
        def cart_summary_footer():
            cart = get_cart()
            if not cart:
                return
            total = 0
            total_items = 0
            for pid, item in cart.items():
                if isinstance(item, dict) and isinstance(item.get('product'), dict):
                    qty = int(item.get('quantity') or 1)
                    price = float(item['product'].get('price') or 0)
                    total += price * qty
                    total_items += qty
            with ui.column().classes('w-full gap-5'):
                # Divider with icon
                with ui.row().classes('w-full items-center gap-3'):
                    ui.element('div').classes('flex-1 h-px bg-border/30')
                    ui.icon('receipt_long', size='18px').classes('text-muted-foreground/30')
                    ui.element('div').classes('flex-1 h-px bg-border/30')
                
                # Price breakdown
                with ui.column().classes('w-full gap-2'):
                    with ui.row().classes('w-full justify-between items-center'):
                        ui.label(f'Tạm tính ({total_items} sản phẩm)').classes('text-sm text-muted-foreground')
                        ui.label("{:,.0f}đ".format(total)).classes('text-sm font-semibold text-foreground')
                    with ui.row().classes('w-full justify-between items-center'):
                        ui.label('Phí vận chuyển').classes('text-sm text-muted-foreground')
                        ui.label('Miễn phí').classes('text-sm font-semibold text-green-600')
                
                ui.element('div').classes('w-full h-px bg-border/30')
                
                with ui.row().classes('w-full justify-between items-end'):
                    ui.label('Tổng cộng').classes('text-sm font-bold text-foreground uppercase tracking-wider')
                    with ui.column().classes('items-end gap-0'):
                        ui.label("{:,.0f}đ".format(total)).classes('font-black text-2xl text-primary tracking-tight')
                        ui.label('(Đã bao gồm VAT)').classes('text-[10px] text-muted-foreground italic')
                
                ui.button(t('checkout'), icon='lock', on_click=open_checkout) \
                    .props('unelevated rounded-full size=lg no-caps') \
                    .classes('checkout-btn w-full text-white font-black h-14 text-base shadow-xl shadow-primary/25 hover:shadow-2xl hover:shadow-primary/30 transition-all')
                
                with ui.row().classes('w-full justify-center items-center gap-4 opacity-40'):
                    ui.icon('verified_user', size='14px')
                    ui.label('Thanh toán an toàn & bảo mật').classes('text-[10px] font-semibold tracking-wider uppercase')

        def update_qty(pid, delta):
            cart = get_cart()
            pid = str(pid)
            if pid in cart:
                new_qty = cart[pid]['quantity'] + delta
                if new_qty > 0:
                    if delta > 0 and new_qty > cart[pid]['product'].get('stock', 0):
                        ui.notify(t('out_of_stock'), type='warning')
                        return
                    cart[pid]['quantity'] = new_qty
                else:
                    del cart[pid]
                app.storage.user.update(cart=cart)
                cart_items_list.refresh()
                cart_summary_footer.refresh()
                floating_cart.refresh()

        def remove_from_cart(pid):
            cart = get_cart()
            pid = str(pid)
            if pid in cart:
                del cart[pid]
                app.storage.user.update(cart=cart)
                cart_items_list.refresh()
                cart_summary_footer.refresh()
                floating_cart.refresh()

        def open_checkout():
            checkout_modal.open()

        async def handle_checkout():
            if not checkout_address.value or not checkout_phone.value:
                ui.notify(t('required_fields'), type='warning')
                return
            
            cart = get_cart()
            items = [{"product_id": int(pid), "quantity": item['quantity']} for pid, item in cart.items()]
            order_data = {
                "shipping_address": checkout_address.value,
                "contact_phone": checkout_phone.value,
                "note": checkout_note.value,
                "items": items
            }
            
            res = await api_client.create_order(order_data)
            if res:
                ui.notify(t('order_success'), type='positive')
                app.storage.user['cart'] = {}
                checkout_modal.close()
                cart_drawer.close()
                cart_items_list.refresh()
                cart_summary_footer.refresh()
                floating_cart.refresh()
                product_grid.refresh()
            else:
                ui.notify(t('order_failed'), type='negative')

        # Main Layout (inside theme.frame)
        with ui.element('div').classes('w-full bg-background min-h-screen pb-20'):
            base.page_header(t('shop_title'), t('shop_subtitle'))

            with theme.container().classes('mt-12'):
                # Toolbar
                with ui.row().classes('w-full justify-between items-center mb-12 px-4 gap-6'):
                    # Categories
                    categories = [
                        ('all', t('all_categories')),
                        ('costume', t('cat_costume')),
                        ('souvenir', t('cat_souvenir')),
                        ('specialty', t('cat_specialty')),
                        ('digital', t('cat_digital')),
                        ('ticket', t('cat_ticket'))
                    ]
                    if state.category is None: state.category = 'all'
                    
                    with ui.row().classes('gap-2 overflow-x-auto no-scrollbar py-2 max-md:w-full'):
                        for key, label in categories:
                            is_active = (state.category == key)
                            ui.button(label, on_click=lambda e, k=key: (setattr(state, 'category', k), setattr(state, 'page', 1), product_grid.refresh())) \
                                .props('unelevated rounded-full' if is_active else 'outline rounded-full') \
                                .classes(f'px-6 py-2 text-sm font-bold transition-all {"bg-primary text-white shadow-md" if is_active else "text-muted-foreground border-border/50 hover:border-primary hover:text-primary"}')

                    # Search
                    with ui.row().classes('items-center gap-4'):
                        ui.input(placeholder=t('search_products')) \
                            .props('outlined dense clearable debounce=500 icon=search') \
                            .classes('modern-input w-72 bg-background rounded-xl') \
                            .bind_value(state, 'search') \
                            .on('change', product_grid.refresh)

                # Product Grid
                await product_grid()

        # Floating elements
        floating_cart()

        # Redesigned Cart Drawer
        with ui.dialog().props('position=right full-height transition-show=slide-left transition-hide=slide-right').classes('cart-drawer-dialog') as cart_drawer:
            with ui.card().classes('h-full p-0 flex flex-col bg-[#faf9f6] rounded-none shadow-2xl overflow-hidden').style('width: 460px; max-width: 90vw; border-left: 1px solid rgba(0,0,0,0.06);'):
                # Premium Header with gradient
                with ui.element('div').classes('shrink-0 relative overflow-hidden').style('background: linear-gradient(135deg, #b21e1e 0%, #8b1515 60%, #6d1010 100%);'):
                    # Decorative pattern overlay
                    ui.element('div').classes('absolute inset-0 opacity-[0.06] pointer-events-none').style('background-image: radial-gradient(#fff 1px, transparent 1px); background-size: 16px 16px;')
                    
                    with ui.row().classes('w-full justify-between items-center p-5 relative z-10'):
                        with ui.column().classes('gap-0.5'):
                            ui.label(t('cart')).classes('text-xl font-black tracking-tight text-white uppercase')
                            with ui.row().classes('items-center gap-2 opacity-70'):
                                ui.icon('local_mall', size='11px').classes('text-white')
                                ui.label('DANH SÁCH CHỌN LỰA').classes('text-[9px] font-bold tracking-[0.2em] text-white')
                        
                        ui.button(on_click=cart_drawer.close, icon='close') \
                            .props('flat round color=white size=sm') \
                            .classes('hover:bg-white/15 transition-all')

                # Cart content - scrollable items area
                with ui.scroll_area().classes('flex-1'):
                    with ui.column().classes('w-full gap-3 p-4 pb-6'):
                        cart_items_list()

                # Fixed summary footer
                with ui.element('div').classes('shrink-0 p-4 pt-3 bg-white border-t border-border/20').style('box-shadow: 0 -8px 30px rgba(0,0,0,0.04);'):
                    cart_summary_footer()

        with ui.dialog() as checkout_modal:
            with ui.card().classes('w-full max-w-[500px] p-8 rounded-[40px] border border-border/40 shadow-2xl'):
                with ui.row().classes('w-full justify-between items-center mb-8'):
                    with ui.column().classes('gap-1'):
                        ui.label(t('checkout')).classes('text-3xl font-black text-primary tracking-tight')
                        ui.label('Thông tin nhận hàng').classes('text-xs text-muted-foreground uppercase tracking-widest')
                    ui.button(icon='close', on_click=checkout_modal.close).props('flat round dense size=sm')
                
                with ui.column().classes('w-full gap-6'):
                    with ui.column().classes('w-full gap-1'):
                        ui.label(t('shipping_address')).classes('text-[10px] font-bold text-muted-foreground uppercase ml-2')
                        checkout_address = ui.textarea(placeholder='Địa chỉ cụ thể...').classes('w-full').props('outlined rounded-2xl')
                    
                    with ui.column().classes('w-full gap-1'):
                        ui.label(t('contact_phone')).classes('text-[10px] font-bold text-muted-foreground uppercase ml-2')
                        checkout_phone = ui.input(placeholder='Số điện thoại...').classes('w-full').props('outlined rounded-2xl')
                    
                    with ui.column().classes('w-full gap-1'):
                        ui.label(t('order_note')).classes('text-[10px] font-bold text-muted-foreground uppercase ml-2')
                        checkout_note = ui.textarea(placeholder='Ghi chú cho em biết nhé...').classes('w-full').props('outlined rounded-2xl')
                    
                    with ui.row().classes('w-full justify-end gap-3 mt-6'):
                        ui.button(t('cancel'), on_click=checkout_modal.close).props('flat rounded-full').classes('text-muted-foreground font-bold px-6')
                        ui.button(t('confirm_register'), on_click=handle_checkout).props('unelevated rounded-full size=lg').classes('bg-primary text-white font-bold px-10 shadow-lg shadow-primary/20')
