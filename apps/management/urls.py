from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='mgmt_dashboard'),
    
    # Mahsulotlar
    path('products/', views.products_view, name='mgmt_products'),
    path('products/add/', views.product_add_view, name='mgmt_product_add'),
    path('products/<int:pk>/edit/', views.product_edit_view, name='mgmt_product_edit'),
    path('products/<int:pk>/delete/', views.product_delete_view, name='mgmt_product_delete'),

    # Buyurtmalar
    path('orders/', views.orders_view, name='mgmt_orders'),
    path('orders/<int:pk>/', views.order_detail_view, name='mgmt_order_detail'),
    path('orders/<int:pk>/invoice/', views.order_invoice_view, name='mgmt_order_invoice'),

    # Toifalar va Mijozlar
    path('categories/', views.categories_view, name='mgmt_categories'),
    path('customers/', views.customers_view, name='mgmt_customers'),
]
