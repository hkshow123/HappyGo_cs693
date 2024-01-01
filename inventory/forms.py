
from django import forms
from .models import Product
from .models import ProductInventory
from .models import AdminUser,User
class ImageUploadForm(forms.Form):
    image = forms.ImageField()


# your_app/forms.py



class AdminRegistrationForm(forms.ModelForm):
    class Meta:
        model = AdminUser
        fields = ['user_name', 'admin_email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_name', 'user_email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['upc', 'name', 'weight', 'description', 'product_type_id', 'brand_id', 'is_active']


class ProductInventoryForm(forms.ModelForm):
    class Meta:
        model = ProductInventory
        fields = ['upc', 'retail_price', 'store_price', 'total', 'location', 'is_active']