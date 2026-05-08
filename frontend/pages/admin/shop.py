from nicegui import ui, app
from components import base
from api import api_client
from translation import t
import theme
import asyncio

@ui.page('/admin/shop')
async def admin_shop_page():
    if app.storage.user.get('role') != 'admin':
        ui.navigate.to('/')
        return

    with theme.frame():
        with ui.element('div').classes('w-full bg-[#faf9f6] min-h-screen pb-24'):
            # Premium Admin Header
            with ui.element('div').classes('w-full bg-white border-b border-border/60 pt-12 pb-8 shadow-sm'):
                with theme.container():
                    with ui.row().classes('w-full justify-between items-center'):
                        with ui.column().classes('gap-1'):
                            with ui.row().classes('items-center gap-2'):
                                ui.icon('storefront', size='18px', color='primary')
                                ui.label(t('manage_shop')).classes('text-[10px] font-black tracking-[0.3em] text-primary uppercase')
                            ui.label('QUẢN LÝ CỬA HÀNG').classes('text-4xl font-black text-foreground tracking-tight')
                        
                        with ui.row().classes('gap-3'):
                            ui.button(t('add_prefix') + ' ' + t('product_name'), icon='add', on_click=lambda: ui.navigate.to('/admin/edit/product/0')) \
                                .props('unelevated rounded-full').classes('bg-primary text-white font-bold px-8 h-12 shadow-lg shadow-primary/20')

            with theme.container().classes('mt-12'):
                with ui.tabs().classes('w-full bg-white rounded-3xl p-2 shadow-sm border border-border/40 mb-8') as tabs:
                    product_tab = ui.tab(t('manage_products'), icon='inventory_2').classes('rounded-2xl px-8 py-4 font-bold')
                    order_tab = ui.tab(t('manage_orders'), icon='receipt_long').classes('rounded-2xl px-8 py-4 font-bold')

                with ui.tab_panels(tabs, value=product_tab).classes('w-full bg-transparent overflow-visible'):
                    with ui.tab_panel(product_tab).classes('p-0'):
                        await products_management()
                    
                    with ui.tab_panel(order_tab).classes('p-0'):
                        await orders_management()

async def products_management():
    products = await api_client.get_products(limit=100)
    
    if not products:
        with ui.column().classes('w-full items-center justify-center py-24 opacity-40'):
            ui.icon('inventory_2', size='80px')
            ui.label('Chưa có sản phẩm nào').classes('text-xl font-bold mt-4')
        return

    with ui.element('div').classes('grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8'):
        for p in products:
            with ui.card().classes('rounded-[32px] border border-border/40 overflow-hidden shadow-sm hover:shadow-md transition-all p-0 group bg-white'):
                with ui.row().classes('w-full p-6 gap-6 items-center'):
                    # Image with glow on hover
                    with ui.element('div').classes('relative h-24 w-24 shrink-0'):
                        ui.image(p.get('image_url') or '/static/common/default-product.png').classes('h-full w-full rounded-2xl object-cover shadow-md group-hover:scale-105 transition-transform')
                        ui.element('div').classes('absolute inset-0 rounded-2xl border-2 border-primary/5 group-hover:border-primary/20 transition-all')
                    
                    with ui.column().classes('flex-1 gap-1'):
                        ui.label(p['name']).classes('font-black text-lg line-clamp-1 group-hover:text-primary transition-colors')
                        ui.label("{:,.0f} đ".format(p['price'])).classes('text-primary font-black')
                        
                        with ui.row().classes('items-center gap-2 mt-2'):
                            with ui.element('div').classes(f'px-2 py-0.5 rounded-md text-[9px] font-black uppercase tracking-widest {"bg-green-100 text-green-700" if p["stock"] > 0 else "bg-red-100 text-red-700"}'):
                                ui.label('IN STOCK' if p["stock"] > 0 else 'OUT OF STOCK')
                            ui.label(f"SL: {p['stock']}").classes('text-[10px] font-bold text-muted-foreground')
                    
                    with ui.column().classes('gap-2'):
                        ui.button(icon='edit', on_click=lambda p=p: ui.navigate.to(f'/admin/edit/product/{p["id"]}')).props('flat round size=sm').classes('hover:bg-primary/5 text-primary')
                        ui.button(icon='delete_outline', on_click=lambda p=p: delete_product(p)).props('flat round size=sm color=destructive').classes('hover:bg-red-50')

async def orders_management():
    orders = await api_client.admin_get_all_orders(limit=100)
    
    if not orders:
        with ui.column().classes('w-full items-center justify-center py-24 opacity-40'):
            ui.icon('receipt_long', size='80px')
            ui.label(t('no_registrations')).classes('text-xl font-bold mt-4')
        return

    with ui.column().classes('w-full gap-6'):
        for o in orders:
            with ui.expansion(f"Đơn hàng #{o['id']} - {o['contact_phone']}").classes('w-full border border-border/40 rounded-[28px] overflow-hidden bg-white shadow-sm'):
                with ui.column().classes('p-8 gap-8'):
                    # Order Header
                    with ui.row().classes('w-full justify-between items-start'):
                        with ui.row().classes('gap-6'):
                            with ui.column().classes('gap-1'):
                                ui.label('THÔNG TIN GIAO HÀNG').classes('text-[10px] font-black text-muted-foreground uppercase tracking-widest')
                                ui.label(o['shipping_address']).classes('text-base font-bold text-foreground max-w-md')
                            
                            with ui.column().classes('gap-1'):
                                ui.label('NGÀY ĐẶT').classes('text-[10px] font-black text-muted-foreground uppercase tracking-widest')
                                date_str = o.get('created_at', 'Chưa rõ')[:10] if o.get('created_at') else 'Chưa rõ'
                                ui.label(date_str).classes('text-base font-bold')

                        with ui.column().classes('gap-2 items-end'):
                            ui.label('TRẠNG THÁI').classes('text-[10px] font-black text-muted-foreground uppercase tracking-widest')
                            status_val = o['status']
                            colors = {
                                'pending': 'amber-500',
                                'processing': 'blue-500',
                                'shipped': 'indigo-500',
                                'delivered': 'emerald-600',
                                'cancelled': 'rose-600'
                            }
                            color = colors.get(status_val, 'grey')
                            with ui.element('div').classes(f'bg-{color}/10 text-{color} px-4 py-1.5 rounded-full border border-{color}/20 flex items-center gap-2'):
                                ui.element('div').classes(f'w-2 h-2 rounded-full bg-{color} animate-pulse')
                                ui.label(t(f"status_{status_val}").upper()).classes('text-[10px] font-black tracking-widest')

                    # Items List
                    with ui.column().classes('w-full gap-3 bg-[#faf9f6] p-6 rounded-3xl border border-border/40'):
                        ui.label('DANH SÁCH SẢN PHẨM').classes('text-[10px] font-black text-muted-foreground uppercase tracking-[0.2em] mb-2')
                        for item in o['items']:
                            with ui.row().classes('w-full justify-between items-center py-2 border-b border-border/20 last:border-0'):
                                with ui.row().classes('items-center gap-4'):
                                    ui.image(item['product'].get('image_url') or '/static/common/default-product.png').classes('w-10 h-10 rounded-lg object-cover')
                                    ui.label(f"{item['product']['name']}").classes('text-sm font-bold')
                                    ui.label(f"x{item['quantity']}").classes('text-xs text-muted-foreground bg-white px-2 py-0.5 rounded border')
                                ui.label("{:,.0f} đ".format(item['price_at_purchase'] * item['quantity'])).classes('text-sm font-black text-primary')

                    # Summary & Actions
                    with ui.row().classes('w-full justify-between items-center pt-6 border-t border-border/40'):
                        with ui.column().classes('gap-0'):
                            ui.label('TỔNG CỘNG').classes('text-[10px] font-black text-muted-foreground tracking-widest')
                            ui.label("{:,.0f} VNĐ".format(o['total_price'])).classes('text-2xl font-black text-primary')

                        with ui.row().classes('gap-3'):
                            if o['status'] == 'pending':
                                ui.button('Xác nhận xử lý', on_click=lambda o=o: update_status(o['id'], 'processing')).props('unelevated rounded-full').classes('bg-blue-600 text-white font-bold px-6 shadow-md shadow-blue-200')
                            if o['status'] == 'processing':
                                ui.button('Đã giao hàng', on_click=lambda o=o: update_status(o['id'], 'delivered')).props('unelevated rounded-full').classes('bg-emerald-600 text-white font-bold px-6 shadow-md shadow-emerald-200')
                            
                            if o['status'] not in ['cancelled', 'delivered']:
                                ui.button('Hủy đơn', on_click=lambda o=o: update_status(o['id'], 'cancelled')).props('flat rounded-full color=destructive').classes('font-bold')

async def update_status(order_id, status):
    res = await api_client.admin_update_order_status(order_id, status)
    if res:
        ui.notify(t('update_success'), type='positive')
        await asyncio.sleep(0.5)
        ui.navigate.reload()
    else:
        ui.notify(t('update_error'), type='negative')

async def delete_product(product):
    dialog = ui.dialog()
    with dialog, ui.card().classes('p-10 rounded-[40px] border border-border/40 shadow-2xl'):
        with ui.column().classes('items-center text-center gap-6'):
            with ui.element('div').classes('w-20 h-20 bg-red-50 rounded-full flex items-center justify-center'):
                ui.icon('delete_sweep', color='destructive', size='40px')
            
            with ui.column().classes('gap-1'):
                ui.label(t('confirm_delete')).classes('text-2xl font-black text-foreground')
                ui.label(t('delete_confirm_msg')).classes('text-muted-foreground text-sm')
            
            with ui.row().classes('w-full justify-center gap-4 mt-4'):
                ui.button(t('cancel_btn'), on_click=lambda: dialog.submit(False)).props('flat rounded-full').classes('px-8 font-bold text-muted-foreground')
                ui.button(t('delete_now'), on_click=lambda: dialog.submit(True)).props('unelevated rounded-full color=destructive').classes('px-10 font-black shadow-lg shadow-red-100')
    
    if await dialog:
        res = await api_client.admin_delete_product(product['id'])
        if res:
            ui.notify(t('delete_success'), type='positive')
            ui.navigate.reload()
        else:
            ui.notify(t('delete_error'), type='negative')
