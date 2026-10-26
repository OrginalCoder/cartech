from django import forms
from apps.product.models import Product, Category, CarModel
from apps.orders.models import Order


class AdminProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'category', 'sku', 'price', 'old_price', 'stock',
            'compatible_models', 'image', 'manufacturer', 'country',
            'warranty', 'short_description', 'description',
            'is_available', 'is_featured', 'is_new'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-700 bg-slate-800 text-white text-sm focus:outline-none focus:ring-2 focus:ring-rose-500',
                'placeholder': 'Mahsulot to\'liq nomi'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-700 bg-slate-800 text-white text-sm focus:outline-none focus:ring-2 focus:ring-rose-500'
            }),
            'sku': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-700 bg-slate-800 text-white text-sm uppercase font-mono focus:outline-none focus:ring-2 focus:ring-rose-500',
                'placeholder': 'SH-5W30-4L'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-700 bg-slate-800 text-white text-sm font-bold focus:outline-none focus:ring-2 focus:ring-rose-500',
                'placeholder': '450000'
            }),
            'old_price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-700 bg-slate-800 text-white text-sm focus:outline-none focus:ring-2 focus:ring-rose-500',
                'placeholder': '500000 (chegirma bo\'lsa)'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-700 bg-slate-800 text-white text-sm focus:outline-none focus:ring-2 focus:ring-rose-500',
                'placeholder': '10'
            }),
            'compatible_models': forms.SelectMultiple(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-700 bg-slate-800 text-white text-sm h-32 focus:outline-none focus:ring-2 focus:ring-rose-500'
            }),
            'manufacturer': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-700 bg-slate-800 text-white text-sm focus:outline-none focus:ring-2 focus:ring-rose-500',
                'placeholder': 'Shell, Brembo, GM...'
            }),
            'country': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-700 bg-slate-800 text-white text-sm focus:outline-none focus:ring-2 focus:ring-rose-500',
                'placeholder': 'Koreya, Germaniya, O\'zbekiston...'
            }),
            'warranty': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-700 bg-slate-800 text-white text-sm focus:outline-none focus:ring-2 focus:ring-rose-500',
                'placeholder': '12 oy'
            }),
            'short_description': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-700 bg-slate-800 text-white text-sm focus:outline-none focus:ring-2 focus:ring-rose-500',
                'placeholder': 'Qisqa bir qatorlik tavsif'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-700 bg-slate-800 text-white text-sm focus:outline-none focus:ring-2 focus:ring-rose-500',
                'placeholder': 'Mahsulotning to\'liq xususiyatlari va tavsifi...'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full text-sm text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-rose-600 file:text-white hover:file:bg-rose-700'
            }),
            'is_available': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-rose-600 rounded bg-slate-800 border-slate-700'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-rose-600 rounded bg-slate-800 border-slate-700'}),
            'is_new': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-rose-600 rounded bg-slate-800 border-slate-700'}),
        }


class AdminCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'icon', 'description', 'image', 'is_featured']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-700 bg-slate-800 text-white text-sm',
                'placeholder': 'Kategoriya nomi'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-700 bg-slate-800 text-white text-sm',
                'placeholder': 'fa-oil-can, fa-cog, fa-car-battery'
            }),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-700 bg-slate-800 text-white text-sm',
                'placeholder': 'Toifa haqida qisqacha...'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full text-sm text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-rose-600 file:text-white hover:file:bg-rose-700'
            }),
            'is_featured': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-rose-600 rounded bg-slate-800 border-slate-700'}),
        }
