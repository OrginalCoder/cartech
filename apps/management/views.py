from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.core.paginator import Paginator
from apps.product.models import Product, Category, CarBrand, CarModel
from apps.orders.models import Order, OrderItem
from apps.accounts.models import CustomUser
from .forms import AdminProductForm, AdminCategoryForm


def is_store_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


@user_passes_test(is_store_admin, login_url='login')
def dashboard_view(request):
    orders = Order.objects.all().order_by('-created_at')
    products = Product.objects.all()

    # Asosiy ko'rsatkichlar
    total_revenue = orders.filter(status='delivered').aggregate(total=Sum('total_amount'))['total'] or 0
    all_revenue = orders.aggregate(total=Sum('total_amount'))['total'] or 0
    total_orders_count = orders.count()
    pending_orders_count = orders.filter(status__in=['pending', 'processing']).count()
    delivered_orders_count = orders.filter(status='delivered').count()
    total_products_count = products.count()
    total_customers_count = CustomUser.objects.filter(is_staff=False).count()

    # Kam qolgan tovarlar (stock <= 5)
    low_stock_products = products.filter(stock__lte=5, is_available=True)[:6]

    # So'nggi buyurtmalar
    recent_orders = orders[:6]

    context = {
        'active_menu': 'dashboard',
        'total_revenue': total_revenue,
        'all_revenue': all_revenue,
        'total_orders_count': total_orders_count,
        'pending_orders_count': pending_orders_count,
        'delivered_orders_count': delivered_orders_count,
        'total_products_count': total_products_count,
        'total_customers_count': total_customers_count,
        'low_stock_products': low_stock_products,
        'recent_orders': recent_orders,
    }
    return render(request, 'management/dashboard.html', context)


@user_passes_test(is_store_admin, login_url='login')
def products_view(request):
    products = Product.objects.select_related('category').all().order_by('-created_at')
    
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(sku__icontains=query) |
            Q(category__name__icontains=query)
        )

    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    stock_filter = request.GET.get('stock')
    if stock_filter == 'low':
        products = products.filter(stock__lte=5)
    elif stock_filter == 'out':
        products = products.filter(stock=0)

    paginator = Paginator(products, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    context = {
        'active_menu': 'products',
        'products': page_obj,
        'categories': categories,
        'query': query or '',
        'selected_category': category_slug or '',
        'selected_stock': stock_filter or '',
        'total_count': products.count(),
    }
    return render(request, 'management/products.html', context)


@user_passes_test(is_store_admin, login_url='login')
def product_add_view(request):
    if request.method == 'POST':
        form = AdminProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"'{product.name}' muvaffaqiyatli qo'shildi!")
            return redirect('mgmt_products')
    else:
        form = AdminProductForm()

    context = {
        'active_menu': 'products',
        'form': form,
        'title': "Yangi mahsulot qo'shish",
    }
    return render(request, 'management/product_form.html', context)


@user_passes_test(is_store_admin, login_url='login')
def product_edit_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = AdminProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"'{product.name}' muvaffaqiyatli yangilandi!")
            return redirect('mgmt_products')
    else:
        form = AdminProductForm(instance=product)

    context = {
        'active_menu': 'products',
        'form': form,
        'product': product,
        'title': f"Mahsulotni tahrirlash: {product.name}",
    }
    return render(request, 'management/product_form.html', context)


@user_passes_test(is_store_admin, login_url='login')
def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    name = product.name
    product.delete()
    messages.info(request, f"'{name}' o'chirildi.")
    return redirect('mgmt_products')


@user_passes_test(is_store_admin, login_url='login')
def orders_view(request):
    orders = Order.objects.all().order_by('-created_at')
    
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)

    query = request.GET.get('q')
    if query:
        orders = orders.filter(
            Q(full_name__icontains=query) |
            Q(phone__icontains=query) |
            Q(id__icontains=query)
        )

    paginator = Paginator(orders, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'active_menu': 'orders',
        'orders': page_obj,
        'status_filter': status_filter or '',
        'query': query or '',
        'total_count': orders.count(),
    }
    return render(request, 'management/orders.html', context)


@user_passes_test(is_store_admin, login_url='login')
def order_detail_view(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        is_paid = request.POST.get('is_paid') == 'on'
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
        order.is_paid = is_paid
        order.save()
        messages.success(request, f"Buyurtma #{order.id} holati yangilandi!")
        return redirect('mgmt_order_detail', pk=order.pk)

    context = {
        'active_menu': 'orders',
        'order': order,
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'management/order_detail.html', context)


@user_passes_test(is_store_admin, login_url='login')
def order_invoice_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'management/order_invoice.html', {'order': order})


@user_passes_test(is_store_admin, login_url='login')
def categories_view(request):
    categories = Category.objects.all().annotate(product_count=Count('products'))

    if request.method == 'POST':
        form = AdminCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            cat = form.save()
            messages.success(request, f"'{cat.name}' toifasi yaratildi!")
            return redirect('mgmt_categories')
    else:
        form = AdminCategoryForm()

    context = {
        'active_menu': 'categories',
        'categories': categories,
        'form': form,
    }
    return render(request, 'management/categories.html', context)


@user_passes_test(is_store_admin, login_url='login')
def customers_view(request):
    customers = CustomUser.objects.filter(is_staff=False).annotate(
        orders_count=Count('orders'),
        total_spent=Sum('orders__total_amount')
    ).order_by('-date_joined')

    context = {
        'active_menu': 'customers',
        'customers': customers,
    }
    return render(request, 'management/customers.html', context)
