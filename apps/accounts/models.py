from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name="Telefon raqami")
    email = models.EmailField(unique=True, verbose_name="Elektron pochta")

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"

    def __str__(self):
        return f"{self.username} ({self.phone_number})"


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile", verbose_name="Foydalanuvchi")
    shipping_address = models.TextField(blank=True, null=True, verbose_name="Yetkazib berish manzili")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Shahar / Tuman")

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profillar"

    def __str__(self):
        return f"{self.user.username}"


class UserCar(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="cars", verbose_name="Egasi")
    car_model = models.ForeignKey('product.CarModel', on_delete=models.CASCADE, verbose_name="Model")
    year = models.PositiveIntegerField(verbose_name="Ishlab chiqarilgan yili", null=True, blank=True)
    vin_code = models.CharField(max_length=17, blank=True, verbose_name="VIN-kod / Kuzov raqami")
    license_plate = models.CharField(max_length=15, blank=True, verbose_name="Davlat raqami")
    is_primary = models.BooleanField(default=True, verbose_name="Asosiy mashina")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Mijoz avtomobili"
        verbose_name_plural = "Mijoz avtomobillari"
        ordering = ["-is_primary", "-created_at"]

    def __str__(self):
        return f"{self.car_model} ({self.year or ''})"