from django.contrib import admin
from django.urls import path
from . import views
app_name = 'inventory'

urlpatterns = [
    path('',views.home, name='home'),
    path('categories/',views.categories, name='categories'),

    # Brand
    path('add_brand/', views.add_brand,name='add_brand'),
    path('base/', views.base),
    path('brand_edit/<int:id>/', views.brand_edit,name='brand_edit'),
    path('brand_delete/<int:id>/', views.brand_delete,name='brand_delete'),

    # Media
    path('image_add/<str:upc>', views.image_add, name='image_add'),
    path('image_delete/<str:upc>/', views.image_delete, name='image_delete'),

    # Category
    path('category_add/', views.category_add, name='category_add'),
    path('category_delete/<int:id>/', views.category_delete,name='category_delete'),
    path('category_edit/<int:id>/', views.category_edit,name='category_edit'),

    # Product Type
    path('type_add/', views.type_add, name='type_add'),
    path('type_delete/<int:id>/', views.type_delete, name='type_delete'),
    path('type_edit/<int:id>/', views.type_edit, name='type_edit'),

    # Product
    path('product_add/', views.product_add, name='product_add'),
    path('product_delete/<int:id>/', views.product_delete, name='product_delete'),
    path('product_edit/<int:id>/', views.product_edit, name='product_edit'),

    # Inventory
    path('inventory_mg/', views.inventory_mg, name='inventory_mg'),
    path('inventory_edit/',views.inventory_edit, name='inventory_edit'),
    path('inventory_delete/<str:upc>/', views.inventory_delete, name='inventory_delete'),
    path('admin_page/', views.admin_page, name='admin_page'),

    # Location
    path('location_add/', views.location_add, name='location_add'),
    path('location_edit/<int:id>', views.location_edit, name='location_edit'),
    path('location_delete/<int:id>', views.location_delete, name='location_delete'),


    # Search
    path('search/', views.search, name='search'),

    # Login / log out
    path('login/',views.login_page, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('protected/', views.MyProtectedView.as_view(), name='my_protected_view'),

    # Order
    path('order_edit/', views.order_edit, name='order_edit'),

    # Item Search



]