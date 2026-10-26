from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.product.models import Product
from .models import Order, OrderItem
from .cart import Cart


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'orders/cart_detail.html', {'cart': cart})


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = 1
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
        except (ValueError, TypeError):
            quantity = 1
        override = request.POST.get('override') == 'True'
    else:
        override = False

    cart.add(product=product, quantity=quantity, override_quantity=override)
    messages.success(request, f"'{product.name}' savatga qo'shildi.")
    
    # Qayerdan kelgan bo'lsa o'sha yerga qaytadi
    next_url = request.META.get('HTTP_REFERER')
    if next_url and 'cart' not in next_url:
        return redirect(next_url)
    return redirect('cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request, f"'{product.name}' savatdan o'chirildi.")
    return redirect('cart_detail')


def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "Savatingiz bo'sh. Iltimos, mahsulot tanlang.")
        return redirect('product_list')

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method', 'cash')
        note = request.POST.get('note', '')

        if not all([full_name, phone, address]):
            messages.error(request, "Iltimos, barcha majburiy maydonlarni to'ldiring.")
            return render(request, 'orders/checkout.html', {'cart': cart})

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            phone=phone,
            city=city or 'Toshkent',
            address=address,
            total_amount=cart.get_total_price(),
            payment_method=payment_method,
            note=note
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )

        cart.clear()
        messages.success(request, "Buyurtmangiz qabul qilindi! Tez orada operatorlarimiz bog'lanishadi.")
        return redirect('order_success', order_id=order.id)

    # Agar login bo'lgan bo'lsa, ma'lumotlarni to'ldirib qo'yamiz
    initial = {}
    if request.user.is_authenticated:
        initial['full_name'] = f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
        initial['phone'] = request.user.phone_number or ''
        if hasattr(request.user, 'profile'):
            initial['city'] = request.user.profile.city or ''
            initial['address'] = request.user.profile.shipping_address or ''

    return render(request, 'orders/checkout.html', {'cart': cart, 'initial': initial})


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_success.html', {'order': order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product').order_by('-created_at')
    return render(request, 'orders/my_orders.html', {'orders': orders})
