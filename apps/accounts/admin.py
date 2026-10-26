from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile, UserCar


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profil ma'lumotlari"


class UserCarInline(admin.TabularInline):
    model = UserCar
    extra = 1


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'phone_number', 'is_staff')
    search_fields = ('username', 'email', 'phone_number')
    inlines = (ProfileInline, UserCarInline)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Shaxsiy Ma'lumotlar", {"fields": ("first_name", "last_name", "email", "phone_number")}),
        ("Huquqlar", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Muhim sanalar", {"fields": ("last_login", "date_joined")}),
    )


@admin.register(UserCar)
class UserCarAdmin(admin.ModelAdmin):
    list_display = ('user', 'car_model', 'year', 'vin_code', 'license_plate', 'is_primary')
    list_filter = ('car_model__brand', 'is_primary')
    search_fields = ('user__username', 'vin_code', 'license_plate')
