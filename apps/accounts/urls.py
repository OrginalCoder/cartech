from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Redirect /accounts/profile/ to dashboard_profile
    path('profile/', views.dashboard_profile_view, name='profile'),

    # Dashboard Hub
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/orders/', views.dashboard_orders_view, name='dashboard_orders'),
    path('dashboard/garage/', views.dashboard_garage_view, name='dashboard_garage'),
    path('dashboard/garage/<int:car_id>/delete/', views.dashboard_garage_delete, name='dashboard_garage_delete'),
    path('dashboard/profile/', views.dashboard_profile_view, name='dashboard_profile'),
]
