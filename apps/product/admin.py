from django.contrib import admin
from .models import Category, CarBrand, CarModel, Product, ProductImage, ProductReview


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon", "is_featured")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("is_featured",)
    search_fields = ("name",)


class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1


@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    inlines = [CarModelInline]


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "year_from", "year_to")
    list_filter = ("brand",)
    search_fields = ("name", "brand__name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "old_price", "stock", "is_available", "is_featured", "is_new")
    list_filter = ("category", "is_available", "is_featured", "is_new", "created_at")
    list_editable = ("price", "stock", "is_available", "is_featured", "is_new")
    search_fields = ("name", "sku", "description", "manufacturer")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("compatible_models",)
    inlines = [ProductImageInline]


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("product__name", "user__username", "comment")
