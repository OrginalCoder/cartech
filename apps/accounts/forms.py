from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import CustomUser, Profile, UserCar
from apps.product.models import CarModel


class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True, label="Ism", widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2.5 rounded-xl border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-red-600 focus:outline-none transition',
        'placeholder': 'Ali'
    }))
    last_name = forms.CharField(max_length=50, required=True, label="Familiya", widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2.5 rounded-xl border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-red-600 focus:outline-none transition',
        'placeholder': 'Valiyev'
    }))
    phone_number = forms.CharField(max_length=20, required=True, label="Telefon raqami", widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2.5 rounded-xl border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-red-600 focus:outline-none transition',
        'placeholder': '+998901234567'
    }))
    email = forms.EmailField(required=True, label="Elektron pochta", widget=forms.EmailInput(attrs={
        'class': 'w-full px-4 py-2.5 rounded-xl border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-red-600 focus:outline-none transition',
        'placeholder': 'ali@example.com'
    }))
    password = forms.CharField(label="Parol", widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-2.5 rounded-xl border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-red-600 focus:outline-none transition',
        'placeholder': 'Kamida 8 ta belgi'
    }))
    password_confirm = forms.CharField(label="Parolni tasdiqlang", widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-2.5 rounded-xl border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-red-600 focus:outline-none transition',
        'placeholder': 'Parolni qaytadan kiriting'
    }))

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-red-600 focus:outline-none transition',
                'placeholder': 'alivaliyev'
            }),
        }

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        phone = phone.replace(' ', '').replace('-', '')
        if CustomUser.objects.filter(phone_number=phone).exists():
            raise ValidationError("Ushbu telefon raqami allaqachon ro'yxatdan o'tgan.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('password_confirm')
        if p1 and p2 and p1 != p2:
            self.add_error('password_confirm', "Parollar bir-biriga mos kelmadi.")
        return cleaned_data


class UserLoginForm(forms.Form):
    username_or_phone = forms.CharField(label="Foydalanuvchi nomi yoki Telefon", widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2.5 rounded-xl border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-red-600 focus:outline-none transition',
        'placeholder': 'Username yoki +9989...'
    }))
    password = forms.CharField(label="Parol", widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-2.5 rounded-xl border border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-red-600 focus:outline-none transition',
        'placeholder': '••••••••'
    }))


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True, label="Ism", widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 bg-slate-50 text-slate-800 text-sm focus:outline-none focus:ring-2 focus:ring-rose-500'
    }))
    last_name = forms.CharField(max_length=50, required=True, label="Familiya", widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 bg-slate-50 text-slate-800 text-sm focus:outline-none focus:ring-2 focus:ring-rose-500'
    }))
    email = forms.EmailField(required=True, label="Email", widget=forms.EmailInput(attrs={
        'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 bg-slate-50 text-slate-800 text-sm focus:outline-none focus:ring-2 focus:ring-rose-500'
    }))
    phone_number = forms.CharField(max_length=20, required=True, label="Telefon", widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 bg-slate-50 text-slate-800 text-sm focus:outline-none focus:ring-2 focus:ring-rose-500'
    }))

    class Meta:
        model = Profile
        fields = ['city', 'shipping_address']
        widgets = {
            'city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 bg-slate-50 text-slate-800 text-sm focus:outline-none focus:ring-2 focus:ring-rose-500',
                'placeholder': 'Toshkent shahar, Chilonzor tumani'
            }),
            'shipping_address': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 bg-slate-50 text-slate-800 text-sm focus:outline-none focus:ring-2 focus:ring-rose-500',
                'placeholder': 'Ko\'cha, uy raqami, xonadon'
            }),
        }


class UserCarForm(forms.ModelForm):
    class Meta:
        model = UserCar
        fields = ['car_model', 'year', 'vin_code', 'license_plate', 'is_primary']
        widgets = {
            'car_model': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 bg-slate-50 text-slate-800 text-sm focus:outline-none focus:ring-2 focus:ring-rose-500'
            }),
            'year': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 bg-slate-50 text-slate-800 text-sm focus:outline-none focus:ring-2 focus:ring-rose-500',
                'placeholder': '2023'
            }),
            'vin_code': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 bg-slate-50 text-slate-800 text-sm uppercase font-mono focus:outline-none focus:ring-2 focus:ring-rose-500',
                'placeholder': 'KL1SF69YEB...'
            }),
            'license_plate': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 bg-slate-50 text-slate-800 text-sm uppercase font-mono focus:outline-none focus:ring-2 focus:ring-rose-500',
                'placeholder': '01 A 777 AA'
            }),
            'is_primary': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-rose-600 rounded border-slate-300 focus:ring-rose-500'
            }),
        }
