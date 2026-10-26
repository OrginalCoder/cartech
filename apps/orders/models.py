from django.db import models
from django.conf import settings
from apps.product.models import Product


class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", "Kutilmoqda"),
        ("processing", "Tayyorlanmoqda"),
        ("shipped", "Yetkazilmoqda"),
        ("delivered", "Yetkazib berildi"),
        ("cancelled", "Bekor qilindi"),
    )

    PAYMENT_CHOICES = (
        ("cash", "Qabul qilganda naqd yoki karta"),
        ("payme", "Payme"),
        ("click", "Click"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
        verbose_name="Mijoz",
    )
    full_name = models.CharField(max_length=150, verbose_name="F.I.SH")
    phone = models.CharField(max_length=20, verbose_name="Telefon raqami")
    city = models.CharField(max_length=100, verbose_name="Shahar / Viloyat")
    address = models.TextField(verbose_name="Yetkazib berish manzili")
    total_amount = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Umumiy summa")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name="Holati")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default="cash", verbose_name="To'lov usuli")
    is_paid = models.BooleanField(default=False, verbose_name="To'langan")
    note = models.TextField(blank=True, verbose_name="Qo'shimcha izoh")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Buyurtma vaqti")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqti")

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Buyurtma #{self.id} - {self.full_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name="Buyurtma")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="order_items", verbose_name="Mahsulot")
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Narxi")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Soni")

    class Meta:
        verbose_name = "Buyurtma mahsuloti"
        verbose_name_plural = "Buyurtma mahsulotlari"

    def get_cost(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.name} ({self.quantity} dona)"
