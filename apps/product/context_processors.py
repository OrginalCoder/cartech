from .models import Category, CarBrand


def product_categories_processor(request):
    categories = Category.objects.all()[:8]
    brands = CarBrand.objects.all()
    return {
        'nav_categories': categories,
        'nav_brands': brands,
    }
