from django.db import models

# Create your models here.
from django.db import models
from django.utils.translation import gettext_lazy as _  # for translating
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField


# use for store hierarchy data

# Create your models here.

class Category(MPTTModel):
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
    slug = models.SlugField(
        max_length=100,
        null=False,
        unique=False,
        blank=False,
        verbose_name=("category saft URL"),
        help_text=_("format:required,letters,numbers,underscore,or hyphens")
    )
    is_active = models.BooleanField(
        default=True,
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="children",
        null=True,
        unique=False,
        verbose_name=_("parent of category"),
        help_text=_("format:not required"),
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("product category")
        verbose_name_plural = _("product categories")

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Product details table
    """
    web_id = models.CharField(
        max_length=50,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("product web id"),
        help_text=_("format:required,unique")
    )
    slug = models.CharField(
        max_length=50,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("product web id"),
        help_text=_("format:required,letters,numbers,underscore,or hyphens")
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
    category = TreeManyToManyField(Category)
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
    update_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("last update at"),
        help_text=_("format:Y-m-d H:M:S")
    )
    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    """
    Product attribute table
    """
    name = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
        null=False,
        verbose_name=_("product attribute name"),
        help_text=_("format:required,unique,max-255")
    )

    description = models.TextField(
        unique=True,
        blank=False,
        null=False,
        verbose_name=_("Product attribute description"),
        help_text=_("format:required"),
    )

    def __str__(self):
        return self.name


class ProductAttributeValue(models.Model):
    """
    Product attribute value table
    """
    product_attribute = models.ForeignKey(
        ProductAttribute,
        on_delete=models.PROTECT,
        related_name="product_attribute",
    )

    attribute_value = models.CharField(
        max_length=255,
        unique=False,
        blank=False,
        null=False,
        verbose_name=_("attribute value"),
        help_text=_("format:required,max-255"),
    )

    def __str__(self):
        return f"{self.product_attribute.name}:{self.attribute_value}"


class ProductAttributeValues(models.Model):
    """
    Product attribute values link table
    """

    attribute_values = models.ForeignKey(
        "ProductAttributeValue", on_delete=models.PROTECT,
        related_name="attribute_values"
    )

    product_inventory = models.ForeignKey(
        "ProductInventory", on_delete=models.PROTECT,
        related_name="product_attribute_value",
    )
    class Meta:
        unique_together =("attribute_values", "product_inventory")

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

    def __str__(self):
        return self.name


class Brand(models.Model):
    """
    Product brands table
    """
    name = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("brand name"),
        help_text=_("format:required,unique,max-255"),
    )


class ProductInventory(models.Model):
    """
    Product inventory table
    """
    sku = models.CharField(
        max_length=20,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("stock keeping unit"),
        help_text=_("format:required,unique,max-20")
    )

    upc = models.CharField(
        max_length=12,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_("universal product code"),
        help_text=_("format:required,unique,max-12")
    )

    product_type = models.ForeignKey(
        ProductType,related_name="product_type", on_delete=models.PROTECT
    )

    product= models.ForeignKey(
        Product, related_name="product", on_delete=models.PROTECT
    )
    brand = models.ForeignKey(
        Brand, related_name="brand", on_delete=models.PROTECT
    )

    attribute_values = models.ManyToManyField(
        ProductAttributeValue,
        related_name="product_attribute_values",
        through="ProductAttributeValues",
    )
    #
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("product visibility"),
        help_text=_("format:true=product visible")
    )

    retail_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        unique=False,
        null=False,
        blank=False,
        verbose_name=_("recommended price"),
        help_text=_("format:maximum price 999.99"),
        error_messages={
            "name":{
                "max_length": _("the price must be greater than or equal to 999.99")
            }
        }

    )

    store_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        unique=False,
        null=False,
        blank=False,
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
        verbose_name=_("product weight")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("created at"),
        help_text=_("format:Y-m-d H:M:S")
    )
    update_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("last update at"),
        help_text=_("format:Y-m-d H:M:S")
    )
    def __str__(self):
        return self.product.name



class AdminUser(models.Model):

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

    email = models.EmailField(
        max_length=20,
        null=False,
        blank=False,
        unique=True,
        verbose_name=_("email address")
    )


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

    email = models.EmailField(
        max_length=20,
        null=False,
        blank=False,
        unique=True,
        verbose_name=_("email address")
    )