# products/urls.py
from django.urls import path
from .views import view_cart, add_to_cart, remove_from_cart
from . import views
app_name = 'products'

urlpatterns = [
    path('', views.index, name='index'),
    # path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_register, name='user_register'),
    path('user/', views.user_view, name='user_view'),
    path('logout/', views.user_logout, name='logout'),


    # Shopping cart
    path('cart/', view_cart, name='view_cart'),
    path('cart/add/<str:upc>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/update/',views.edit_to_cart, name='edit_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_detail/<int:order_id>', views.order_detail, name='order_details'),


    # User portal
    path('profile/',views.profile_view, name='profile_view'),
    path('profile_edit/', views.profile_edit, name='profile_edit'),
    path('address/', views.address_view, name='address_view'),
    path('address_edit/', views.address_edit, name='address_edit'),
    path('orders/', views.orders_view, name='orders_view'),


    # Category
    path('dairy_view/', views.dairy_view, name='dairy_view'),
    path('meat_view/', views.meat_view, name='meat_view'),
    path('fruit_view/', views.fruit_view, name='fruit_view'),
    path('bakery_view/', views.bakery_view, name='bakery_view'),

    # Item Search
    path('item_search/', views.item_search, name='item_search'),
]
