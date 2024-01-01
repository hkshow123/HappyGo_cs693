from datetime import timezone, datetime

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db import models
from django.utils.translation import gettext_lazy as _  # for translating
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from django.db import models
from django.contrib.auth.models import AbstractBaseUser


# use for store hierarchy data


class Category(models.Model):
    """
    Inventory category table implimented with MPTT
    """
    name = models.CharField(
        max_length=100,
        null=False,
        unique=False,
        blank=False,
        verbose_name=_("category name"),
        help_text=_("format:required,max-100")
    )



    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("product category")
        verbose_name_plural = _("product categories")



class Product(models.Model):
    """
    Product details table
    """
    upc = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=False,
        verbose_name=_("product upc"),
        help_text=_("format:required,unique")
    )

    name = models.CharField(
        max_length=100,
        null=False,
        unique=False,
        blank=False,
        verbose_name=_("product name"),
        help_text=_("format:required,max-100")
    )
    description = models.TextField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name=_("product description"),
        help_text=_("format:required,max-100"),
    )
    product_type_id = models.ForeignKey(
        "ProductType",
        to_field="id",
        on_delete=models.CASCADE,
        verbose_name=_("product type"),
        null=True,
    )
    is_active = models.BooleanField(
        default=True,
        unique=False,
        blank=False,
        verbose_name=("Product visibility"),
        help_text=_("format:true=product visible"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("created at"),
        help_text=_("format:Y-m-d H:M:S")
    )

    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=False,
        blank=False,
        default=0,
        verbose_name=_("weight of product")
    )

    media_id = models.ForeignKey(
        "Media",
        to_field="id",
        on_delete=models.CASCADE,
        verbose_name=_("pictures"),
        null=True,
        blank=True,

    )

    brand_id = models.ForeignKey(
        "Brand",
        to_field="id",
        on_delete=models.CASCADE,
        verbose_name=_("brand"),
        null=True,

    )



class ProductType(models.Model):
    """
    Product type table
    """

    name = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
        verbose_name=_("type of product"),
        help_text=_("format:product,unique,max-255"),
    )

    category_id = models.ForeignKey(
        "Category",
        to_field="id",
        default=0,
        on_delete=models.CASCADE)




class Brand(models.Model):
    """
    Product brands table
    """
    name = models.CharField(
        max_length=30,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("brand name"),
        help_text=_("format:required,unique,max-255"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("created at"),
        help_text=_("format:Y-m-d H:M:S"),
    )

class Location(models.Model):
    """
    Product stocks location table
    """

    location = models.CharField(
        max_length=20,
        verbose_name=_("location"),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Location availability"),
        help_text=_("format:true=product visible")
    )

class Media(models.Model):
    """
    Product media (picture, video, etc.)
    """
    upc = models.ForeignKey(
        "ProductInventory",
        on_delete=models.SET_NULL,
        null=True,
    )

    url = models.URLField(
        max_length=100,
        verbose_name=_("url")
    )



class ProductInventory(models.Model):
    """
    Product inventory table
    """

    product_id = models.OneToOneField(
        "Product",
        to_field="id",
        related_name="product_id",
        verbose_name=_("product id"),
        on_delete=models.PROTECT,
        default=1,
        unique=True,
    )
    product_name = models.ForeignKey(
        "Product",
        to_field="id",
        related_name="product_name",
        verbose_name=_("product name"),
        on_delete=models.PROTECT,
        default=1,
    )

    product_type_id = models.ForeignKey(
        "ProductType",
        to_field="id",
        related_name="product_type",
        on_delete=models.PROTECT,
        blank=False,
        verbose_name=_("product type"),
        default=1,

    )


    brand_id = models.ForeignKey(
        "Brand",
        to_field="id",
        related_name="brand",
        verbose_name=_("brand id"),
        on_delete=models.PROTECT,
        default=1,
    )
    upc = models.CharField(
        max_length=12,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("universal product code"),
        help_text=_("format:required,unique,max-12")
        , default=1,
    )
    #
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("product visibility_in"),
        help_text=_("format:true=product visible")
    )

    retail_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        unique=False,
        null=True,
        blank=True,
        verbose_name=_("recommended price"),
        default=0,
        help_text=_("format:maximum price 999.99"),
        error_messages={
            "name": {
                "max_length": _("the price must be greater than or equal to 999.99")
            }
        }

    )

    store_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        unique=False,
        null=True,
        default=0,
        blank=True,
        verbose_name=_("recommended price"),
        help_text=_("format:maximum price 999.99"),
        error_messages={
            "name": {
                "max_length": _("the price must be greater than or equal to 999.99")
            }
        }

    )

    weight = models.FloatField(
        unique=False,
        null=False,
        blank=False,
        verbose_name=_("product weight"),
        default=0,
    )

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")



    update_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("last update at"),
        help_text=_("format:Y-m-d H:M:S")
    )

    total = models.IntegerField(
        default=0,
        editable=True,
        blank=False,
        verbose_name=_("Total")

    )

    location = models.ForeignKey(
        "Location",to_field="id",
        on_delete=models.CASCADE,
        null=True,
    )


#======================== user ===================

class AdminUserManager(BaseUserManager):
    def create_user(self, user_name, password=None, **extra_fields):

        if not user_name:
            raise ValueError(_('The Username must be set'))
        user = self.model(user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(user_name, password, **extra_fields)

class AdminUser(AbstractBaseUser):
    user_name = models.CharField(max_length=30, unique=True, verbose_name=_("User name"))
    password = models.CharField(max_length=100, verbose_name=_("Password"))
    admin_email = models.EmailField(max_length=254, unique=True, verbose_name=_("Email address"))
    is_admin = models.BooleanField(default=False, verbose_name=_("admin user"))
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['email']

    objects = AdminUserManager()

    def __str__(self):
        return self.user_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin


class User(models.Model):
    user_name = models.CharField(
        unique=True,
        max_length=30,
        null=False,
        blank=False,
        verbose_name=_("User name")
    )

    password = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        verbose_name=_("password")
    )

    user_email = models.EmailField(
        max_length=20,
        null=False,
        blank=False,
        unique=True,
        verbose_name=_("email address")
    )