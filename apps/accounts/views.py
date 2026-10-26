from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import CustomUser, Profile, UserCar
from .forms import UserRegistrationForm, UserLoginForm, ProfileUpdateForm, UserCarForm
from apps.orders.models import Order
from apps.product.models import Product


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.first_name or user.username}! Shaxsiy kabinetingiz ochildi.")
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username_or_phone = form.cleaned_data['username_or_phone'].strip()
            password = form.cleaned_data['password']

            user = None
            if username_or_phone.startswith('+') or username_or_phone.isdigit():
                clean_phone = username_or_phone.replace(' ', '').replace('-', '')
                try:
                    found_user = CustomUser.objects.get(phone_number=clean_phone)
                    user = authenticate(request, username=found_user.username, password=password)
                except CustomUser.DoesNotExist:
                    user = None

            if not user:
                user = authenticate(request, username=username_or_phone, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Xush ko'rdik, {user.first_name or user.username}!")
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('dashboard')
            else:
                messages.error(request, "Foydalanuvchi nomi yoki parol noto'g'ri kiritildi.")
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "Siz tizimdan chiqdingiz.")
    return redirect('home')


# ==========================================
# DASHBOARD TIZIMI (SHAXSIY KABINET)
# ==========================================

@login_required
def dashboard_view(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')
    
    # Statistika
    total_orders_count = orders.count()
    total_spent = orders.aggregate(total=Sum('total_amount'))['total'] or 0
    pending_orders_count = orders.filter(status__in=['pending', 'processing', 'shipped']).count()
    
    # User's Garage
    cars = UserCar.objects.filter(user=user).select_related('car_model__brand')
    primary_car = cars.filter(is_primary=True).first() or cars.first()
    
    # Agar mashina bo'lsa, unga mos tavsiya etiladigan qismlar
    recommended_parts = []
    if primary_car:
        recommended_parts = Product.objects.filter(
            is_available=True,
            compatible_models=primary_car.car_model
        )[:4]
    
    if not recommended_parts:
        recommended_parts = Product.objects.filter(is_available=True, is_featured=True)[:4]

    recent_orders = orders[:5]

    context = {
        'active_tab': 'overview',
        'total_orders_count': total_orders_count,
        'total_spent': total_spent,
        'pending_orders_count': pending_orders_count,
        'cars': cars,
        'primary_car': primary_car,
        'recommended_parts': recommended_parts,
        'recent_orders': recent_orders,
    }
    return render(request, 'accounts/dashboard/overview.html', context)


@login_required
def dashboard_orders_view(request):
    user = request.user
    status_filter = request.GET.get('status')
    orders = Order.objects.filter(user=user).prefetch_related('items__product').order_by('-created_at')
    
    if status_filter:
        orders = orders.filter(status=status_filter)

    context = {
        'active_tab': 'orders',
        'orders': orders,
        'status_filter': status_filter,
    }
    return render(request, 'accounts/dashboard/orders.html', context)


@login_required
def dashboard_garage_view(request):
    user = request.user
    cars = UserCar.objects.filter(user=user).select_related('car_model__brand')
    
    if request.method == 'POST':
        form = UserCarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            car.user = user
            if car.is_primary:
                # Boshqa mashinalarni asosiy emas qilib qo'yish
                UserCar.objects.filter(user=user).update(is_primary=False)
            car.save()
            messages.success(request, f"{car.car_model} garajingizga muvaffaqiyatli qo'shildi!")
            return redirect('dashboard_garage')
    else:
        form = UserCarForm()

    context = {
        'active_tab': 'garage',
        'cars': cars,
        'form': form,
    }
    return render(request, 'accounts/dashboard/garage.html', context)


@login_required
def dashboard_garage_delete(request, car_id):
    car = get_object_or_404(UserCar, id=car_id, user=request.user)
    car_name = str(car.car_model)
    car.delete()
    messages.info(request, f"{car_name} garajdan o'chirildi.")
    return redirect('dashboard_garage')


@login_required
def dashboard_profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save()
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.phone_number = form.cleaned_data['phone_number']
            request.user.save()
            messages.success(request, "Profilingiz muvaffaqiyatli yangilandi.")
            return redirect('dashboard_profile')
    else:
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'phone_number': request.user.phone_number,
        }
        form = ProfileUpdateForm(instance=profile, initial=initial_data)

    context = {
        'active_tab': 'profile',
        'form': form,
        'profile': profile,
    }
    return render(request, 'accounts/dashboard/profile.html', context)