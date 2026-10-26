from django.db import models
from django.utils.text import slugify
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Kategoriya nomi")
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    icon = models.CharField(max_length=50, default="fa-wrench", help_text="FontAwesome ikon klassi, masalan: fa-oil-can, fa-cog, fa-car-battery")
    image = models.ImageField(upload_to="categories/", blank=True, null=True, verbose_name="Rasm")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    is_featured = models.BooleanField(default=True, verbose_name="Bosh sahifada ko'rsatish")

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CarBrand(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Brend nomi")
    slug = models.SlugField(max_length=110, unique=True, blank=True)
    logo = models.ImageField(upload_to="brands/", blank=True, null=True, verbose_name="Logotip")

    class Meta:
        verbose_name = "Avtomobil brendi"
        verbose_name_plural = "Avtomobil brendlari"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, related_name="models", verbose_name="Brend")
    name = models.CharField(max_length=100, verbose_name="Model nomi")
    year_from = models.PositiveIntegerField(null=True, blank=True, verbose_name="Yildan")
    year_to = models.PositiveIntegerField(null=True, blank=True, verbose_name="Yilgacha")

    class Meta:
        verbose_name = "Avtomobil modeli"
        verbose_name_plural = "Avtomobil modellari"
        unique_together = ("brand", "name")
        ordering = ["brand", "name"]

    def __str__(self):
        return f"{self.brand.name} {self.name}"


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Mahsulot nomi")
    slug = models.SlugField(max_length=260, unique=True, blank=True)
    sku = models.CharField(max_length=60, unique=True, blank=True, null=True, verbose_name="Artikul / Kod")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", verbose_name="Kategoriya")
    compatible_models = models.ManyToManyField(CarModel, blank=True, related_name="products", verbose_name="Mos keladigan mashinalar")
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Narxi (so'm)")
    old_price = models.DecimalField(max_digits=12, decimal_places=0, blank=True, null=True, verbose_name="Eski narxi (so'm)")
    image = models.ImageField(upload_to="products/", blank=True, null=True, verbose_name="Asosiy rasm")
    short_description = models.CharField(max_length=300, blank=True, verbose_name="Qisqa tavsif")
    description = models.TextField(blank=True, verbose_name="Batafsil tavsif")
    stock = models.PositiveIntegerField(default=10, verbose_name="Ombordagi soni")
    manufacturer = models.CharField(max_length=100, blank=True, verbose_name="Ishlab chiqaruvchi")
    country = models.CharField(max_length=100, blank=True, verbose_name="Ishlab chiqarilgan mamlakat")
    warranty = models.CharField(max_length=100, default="1 oy", verbose_name="Kafolat muddati")
    is_available = models.BooleanField(default=True, verbose_name="Sotuvda mavjud")
    is_featured = models.BooleanField(default=False, verbose_name="Ommabop / Tavsiya etiladi")
    is_new = models.BooleanField(default=True, verbose_name="Yangi mahsulot")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def discount_percent(self):
        if self.old_price and self.old_price > self.price:
            return int(((self.old_price - self.price) / self.old_price) * 100)
        return 0

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="gallery_images", verbose_name="Mahsulot")
    image = models.ImageField(upload_to="products/gallery/", verbose_name="Qo'shimcha rasm")

    class Meta:
        verbose_name = "Mahsulot rasmi"
        verbose_name_plural = "Mahsulot rasmlari"


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews", verbose_name="Mahsulot")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews", verbose_name="Foydalanuvchi")
    rating = models.PositiveSmallIntegerField(default=5, verbose_name="Baho (1-5)")
    comment = models.TextField(verbose_name="Izoh")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yozilgan sana")

    class Meta:
        verbose_name = "Sharh"
        verbose_name_plural = "Sharhlar"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.product.name} ({self.rating}★)"
