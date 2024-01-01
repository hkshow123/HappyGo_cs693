from django.db import models
from django.conf import settings
from inventory.models import Product, ProductInventory,AdminUser,AdminUserManager


# Create your models here.
class ShoppingCart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shopping_cart')
    created_at = models.DateTimeField(auto_now_add=True)

class ShoppingCartItem(models.Model):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(ProductInventory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Profiles(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='profile' )
    full_name = models.CharField(max_length=60, blank=True,null=True)
    street = models.CharField(max_length=60, blank=True,null=True)
    city = models.CharField(max_length=60, blank=True,null=True)
    state = models.CharField(max_length=60, blank=True,null=True)
    zipcode = models.CharField(max_length=5, blank=True,null=True)
    telephone = models.CharField(max_length=15, blank=True,null=True)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(Profiles, on_delete=models.DO_NOTHING, null=True)
    total_price = models.DecimalField(max_digits=6, decimal_places=2,default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    ship_status = models.BooleanField(default=False)
    tracking_number = models.CharField(max_length=10, blank=True,null=True,default=None)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(ProductInventory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # price at the time of purchase
    items_price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)