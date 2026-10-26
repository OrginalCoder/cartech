from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .models import Category, CarBrand, CarModel, Product, ProductReview


def home_view(request):
    categories = Category.objects.filter(is_featured=True)[:8]
    brands = CarBrand.objects.all()[:10]
    featured_products = Product.objects.filter(is_available=True, is_featured=True)[:8]
    new_products = Product.objects.filter(is_available=True, is_new=True)[:8]
    discount_products = Product.objects.filter(is_available=True, old_price__isnull=False)[:4]
    models = CarModel.objects.select_related('brand').all()

    context = {
        'categories': categories,
        'brands': brands,
        'featured_products': featured_products,
        'new_products': new_products,
        'discount_products': discount_products,
        'car_models': models,
    }
    return render(request, 'product/home.html', context)


def product_list_view(request):
    products = Product.objects.filter(is_available=True).select_related('category')
    
    # Qidiruv so'zi
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(sku__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )

    # Kategoriya filtri
    category_slug = request.GET.get('category')
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    # Brend va Model filtri
    brand_id = request.GET.get('brand')
    model_id = request.GET.get('car_model')
    if model_id:
        products = products.filter(compatible_models__id=model_id)
    elif brand_id:
        products = products.filter(compatible_models__brand__id=brand_id)

    # Narx filtri
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and min_price.isdigit():
        products = products.filter(price__gte=min_price)
    if max_price and max_price.isdigit():
        products = products.filter(price__lte=max_price)

    # Saralash
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'popular':
        products = products.order_by('-is_featured', '-created_at')
    else:
        products = products.order_by('-created_at')

    # Duplikatlarni olib tashlash (ManyToMany filtrlashdan keyin)
    products = products.distinct()

    # Paginatsiya
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    brands = CarBrand.objects.prefetch_related('models').all()

    context = {
        'products': page_obj,
        'page_obj': page_obj,
        'categories': categories,
        'brands': brands,
        'selected_category': selected_category,
        'selected_category_slug': category_slug,
        'selected_brand_id': brand_id,
        'selected_model_id': model_id,
        'query': query or '',
        'sort_by': sort_by,
        'min_price': min_price or '',
        'max_price': max_price or '',
        'total_count': products.count(),
    }
    return render(request, 'product/product_list.html', context)


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(id=product.id)[:4]

    reviews = product.reviews.select_related('user').all()

    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating', 5)
        comment = request.POST.get('comment', '').strip()
        if comment:
            ProductReview.objects.create(
                product=product,
                user=request.user,
                rating=int(rating),
                comment=comment
            )
            messages.success(request, "Fikringiz uchun rahmat! Sharhingiz qabul qilindi.")
            return redirect('product_detail', slug=slug)

    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
    }
    return render(request, 'product/product_detail.html', context)
