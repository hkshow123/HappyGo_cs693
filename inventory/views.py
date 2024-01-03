from datetime import timedelta

from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator

from HappyGo import settings
from inventory.models import *
from django.contrib.auth import get_user_model, logout

current_time = datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
from .models import Product, ProductType, Brand, Category, ProductInventory
from .forms import ProductForm, AdminRegistrationForm, UserRegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import ImageUploadForm
from .models import Media
import os
from django.conf import settings
from products.models import Order, OrderItem, Profiles


def test_page(request):
    return render(request, 'test2.html')


class MyProtectedView(LoginRequiredMixin, TemplateView):
    template_name = 'login.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


def login_page(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        user = authenticate(request, username=user_name, password=password)

        print("-------start to login---------")
        print("Authenticate result:", user, password)

        if user is not None:
            if user.is_admin:
                login(request, user)
                print("Logged in successfully as admin")
                return redirect('inventory:inventory_mg')
            else:
                messages.error(request, 'Access denied: User is not an admin')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    print("Logged out successfully")
    return redirect('inventory:login')


def register(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get('user_name')
            password = form.cleaned_data.get('password')
            admin_email = form.cleaned_data.get('admin_email')

            print(user_name, password, admin_email)
            if not admin_email:
                messages.error(request, 'Admin Email cannot be empty.')
            else:
                User = get_user_model()
                User.objects.create_user(user_name=user_name,
                                         password=password,
                                         admin_email=admin_email,
                                         is_admin=True)

                messages.success(request, f'Account created for {user_name}!')
                return redirect('inventory:login')
    else:
        form = AdminRegistrationForm()

    return render(request, 'register.html', {'form': form})


@login_required
def home(request):
    order_list = Order.objects.filter(ship_status=False).order_by('created_at').all()

    content = {
        'order_list': order_list,
    }
    return render(request, "inventory_home.html", content)


@login_required
def admin_page(request):

    order_total =Order.objects.all().count()
    order_list = Order.objects.all().order_by('created_at')
    twenty_four_hours_ago = current_time - timedelta(hours=24)
    order_24 = Order.objects.filter(created_at__gte=twenty_four_hours_ago).count()
    unship_orders = Order.objects.filter(ship_status=False).count()
    shipped_orders = Order.objects.filter(ship_status=True).count()
    out_of_stock_items = ProductInventory.objects.filter(total__lt=1).count()
    content = {
        'order_list': order_list,
        'order_total':order_total,
        'order_24':order_24,
        'unship_orders':unship_orders,
        'shipped_orders':shipped_orders,
        'out_of_stock_items':out_of_stock_items

    }
    return render(request, "inventory_home.html", content)


@login_required
def categories(request):
    data = Category.objects.all()
    return render(request, "add_brand.html", {"data": data})


# =============================      Brand    =================================
@login_required
def add_brand(request):
    data_list = Brand.objects.all()
    if request.method == "GET":
        return render(request, "add_brand.html", {"data_list": data_list})
    else:
        name = request.POST.get("brand")
        Brand.objects.create(name=name)
        return render(request, "add_brand.html", {"data_list": data_list})


@login_required
def brand_edit(request, id):
    obj = Brand.objects.filter(id=id).first()

    if request.method == "GET":

        return render(request, "brand_edit.html", {"obj": obj})
    else:
        data_list = Brand.objects.all()
        name = request.POST.get("brand_name")
        if name is not None and 0 < len(name) < 30:
            obj = Brand.objects.filter(id=id).update(name=name)
            return redirect("inventory:add_brand")
        else:
            return render(request, "brand_edit.html", {"obj": obj, "error": "Invalid data"})


@login_required
def brand_delete(request, id):
    if request.method == "GET":
        brand = get_object_or_404(Brand, id=id)
        Product.objects.filter(brand_id=id).delete()
        brand.delete()
        return redirect("inventory:add_brand")
    return redirect("inventory:add_brand")


def base(request):
    return render(request, "base.html")


# =============================      Images    =================================

def image_add(request, upc):
    """
    Handle image upload for a product.
    """
    data_list = Media.objects.all()
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded image and create a Media record
            media = save_uploaded_image(request.FILES['image'], upc)
            if media:
                return HttpResponseRedirect('/inventory/inventory_mg/')
            else:
                form.add_error(None, "Error in saving image.")
    else:
        form = ImageUploadForm()

    return render(request, 'image_add.html', {'form': form, 'upc': upc, 'data_list': data_list})


def save_uploaded_image(image_file, upc):
    """
    Save an uploaded image to the media directory and create a Media record.
    """
    save_path = os.path.join(settings.MEDIA_ROOT, 'products')
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    file_path = os.path.join(save_path, image_file.name)
    with open(file_path, 'wb+') as destination:
        for chunk in image_file.chunks():
            destination.write(chunk)

    # Create a Media record
    inventory_obj = ProductInventory.objects.get(upc=upc)
    try:
        media = Media.objects.create(
            upc=inventory_obj,
            url=os.path.join('products', image_file.name)
        )
        print(media.upc.upc, media.url, "save------------")
        return media
    except Exception as e:
        print(f"Error in creating media record: {e}")
        return None


@login_required
def image_delete(request, upc):
    media_obj = get_object_or_404(Media, upc=upc)
    media_obj.delete()
    return redirect("inventory:image_add")


# =============================      Category   =================================
@login_required
def category_add(request):
    data_list = Category.objects.all()
    if request.method == "GET":
        return render(request, "category_add.html", {"data_list": data_list})
    else:
        category = request.POST.get("category")
        Category.objects.create(name=category)
        return render(request, "category_add.html", {"data_list": data_list})


@login_required
def category_edit(request, id):
    obj = Category.objects.filter(id=id).first()

    if request.method == "GET":

        return render(request, "category_edit.html", {"obj": obj})
    else:
        data_list = Category.objects.all()
        name = request.POST.get("category_name")
        if name is not None and 0 < len(name) < 30:
            obj = Category.objects.filter(id=id).update(name=name)
            return redirect("inventory:category_add")
        else:
            return render(request, "category_edit.html", {"obj": obj, "error": "Invalid data"})


@login_required
def category_delete(request, id):
    if request.method == "GET":
        category = get_object_or_404(Category, id=id)
        # delete all related obj before delete obj
        ProductType.objects.filter(category_id=id).delete()

        category.delete()
        return redirect("inventory:category_add")
    return redirect("inventory:category_add")


# =============================      Product Type   =================================

@login_required
def type_add(request):
    category_list = Category.objects.all()
    type_list = ProductType.objects.all()
    content = {
        "category_list": category_list,
        "type_list": type_list
    }

    if request.method == "GET":
        return render(request, "type_add.html", content)
    else:
        name = request.POST.get("type_name")
        category_id = request.POST.get("category_id")
        category_obj = get_object_or_404(Category, id=category_id)
        if name is None or len(name) > 30:
            return render(request, "type_add.html", {"obj": None, "error": "Invalid data"})
        ProductType.objects.create(name=name, category_id=category_obj)
        return render(request, "type_add.html", content)


@login_required
def type_edit(request, id):
    product_type_obj = ProductType.objects.filter(id=id).first()
    category_id = product_type_obj.category_id.id
    category_list = Category.objects.all()
    content = {"category_list": category_list,
               "product_type_obj": product_type_obj,
               "category_id": category_id}
    if request.method == "GET":
        return render(request, 'type_edit.html', content)

    else:
        name = request.POST.get("type_name")
        category_id = request.POST.get("category_id")

        print("---------------")
        print(name, category_id)
        category_obj = Category.objects.get(id=category_id)
        if name is None or len(name) > 30:
            return render(request, "type_edit.html", {"obj": None, "Data Error": "Invalid data"})
        ProductType.objects.filter(id=id).update(name=name, category_id=category_obj.id)
        return redirect("inventory:type_add")


@login_required
def type_delete(request, id):
    if request.method == "GET":
        print("-------first-------")
        ProductType.objects.filter(id=id).delete()
        print("----second-----")
        return redirect("inventory:type_add")
    return redirect("inventory:type_add")


# =============================      Product   =================================

@login_required
def product_add(request):
    error_message = None

    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            upc = form.cleaned_data["upc"]
            product_name = form.cleaned_data["name"]
            weight = form.cleaned_data["weight"]
            description = form.cleaned_data["description"]
            print(description)
            product_type_id = form.cleaned_data["product_type_id"]
            print("product_type_id", product_type_id)
            brand_id = form.cleaned_data["brand_id"]
            is_active = form.cleaned_data["is_active"]

            product = Product.objects.create(
                upc=upc,
                name=product_name,
                weight=weight,
                description=description,
                product_type_id=product_type_id,
                brand_id=brand_id,
                is_active=is_active,
                created_at=formatted_time,
                media_id=None
            )

            product_obj = Product.objects.get(upc=upc)
            ProductInventory.objects.create(
                product_id=product_obj,
                upc=product_obj.upc,
                product_name=product_obj,
                weight=product_obj.weight,
                product_type_id=product_obj.product_type_id,
                brand_id=product_obj.brand_id,
                is_active=product_obj.is_active,
                retail_price=None,
                store_price=None,
                update_at=formatted_time,
                total=0,
                location=None,
            )
            print("-------inventory object created-------")
            return redirect("inventory:product_add")
        else:
            print(form.errors)
            error_message = "Invalid data. Please check your input."

    else:
        form = ProductForm()

    category_list = Category.objects.all()
    type_list = ProductType.objects.all()
    brand_list = Brand.objects.all()
    product_list = Product.objects.all().order_by("name")
    inventory_list = ProductInventory.objects.all()

    content = {
        "category_list": category_list,
        "type_list": type_list,
        "brand_list": brand_list,
        "product_list": product_list,
        "inventory_list": inventory_list,
        "form": form,
        "error_message": error_message
    }

    return render(request, "product_add.html", content)


@login_required
def product_edit(request, id):
    error_message = None
    # id is an instance
    print("---id:", id)
    # Get the product object with the given 'id'
    product = get_object_or_404(Product, id=id)
    # product = Product.objects.get(id=id)
    print("----second0000---- and id-")

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            print("----second1111-----")
            upc = form.cleaned_data["upc"]
            product_name = form.cleaned_data["name"]
            weight = form.cleaned_data["weight"]
            description = form.cleaned_data["description"]
            product_type_id = form.cleaned_data["product_type_id"]
            brand_id = form.cleaned_data["brand_id"]
            is_active = form.cleaned_data["is_active"]

            # Update the product object with new data
            product.upc = upc
            product.name = product_name
            product.weight = weight
            product.description = description
            product.product_type_id = product_type_id
            product.brand_id = brand_id
            product.is_active = is_active
            product.created_at = product.created_at
            product.save()
            print("----second 22222-- save---")
            product_obj = product

            inventory_obj, created = ProductInventory.objects.get_or_create(product_id=product_obj.product_id.id)
            inventory_obj.upc = product_obj.upc
            inventory_obj.product_name = product_obj
            inventory_obj.weight = product_obj.weight
            inventory_obj.product_type_id = product_obj.product_type_id
            inventory_obj.brand_id = product_obj.brand_id
            inventory_obj.is_active = product_obj.is_active
            inventory_obj.total = 0
            inventory_obj.retail_price = 0
            inventory_obj.store_price = 0
            inventory_obj.updated_at = formatted_time

            inventory_obj.save()
            print("----inventory_obj_saved")
            return redirect("inventory:product_add")

        else:
            print(form.errors)
            print("----second33333-----")
            error_message = "Invalid data. Please check your input."

    else:
        form = ProductForm(instance=product)
        category_list = Category.objects.all()
        type_list = ProductType.objects.all()
        brand_list = Brand.objects.all()
        product_list = Product.objects.all().order_by("name")
        inventory_list = ProductInventory.objects.all()
        print("-----five-----")
        content = {
            "category_list": category_list,
            "type_list": type_list,
            "brand_list": brand_list,
            "product_list": product_list,
            "inventory_list": inventory_list,
            "form": form,
            "error_message": error_message,
            "product": product,
        }

        return render(request, "product_edit.html", content)


@login_required
def product_delete(request, id):
    if request.method == "GET":
        print("-------first-------")
        Product.objects.filter(id=id).delete()
        print("----second-----")
        return redirect("inventory:product_add")
    return redirect("inventory:product_add")


# ===================================Inventory ==========================
@login_required
def inventory_mg(request):
    print("-----inventory page-----")
    inventory_list = ProductInventory.objects.all().order_by("product_id")
    for obj in inventory_list:
        obj.product_obj = Product.objects.get(upc=obj.upc)
    product_list = Product.objects.all()
    type_list = ProductType.objects.all()
    location_list = Location.objects.filter(is_active=True)
    content = {'Product_list': product_list,
               'type_list': type_list,
               'inventory_list': inventory_list,
               'location_list': location_list,
               }
    return render(request, "inventory.html", content)


@login_required
def inventory_edit(request):
    print("-------edit page-------")
    error_message = None
    category_list = Category.objects.all()
    type_list = ProductType.objects.all()
    brand_list = Brand.objects.all()
    product_list = Product.objects.all().order_by("product_id")
    inventory_list = ProductInventory.objects.all().order_by("product_id")
    location_list = Location.objects.filter(is_active=True)

    content = {
        "category_list": category_list,
        "type_list": type_list,
        "brand_list": brand_list,
        "product_list": product_list,
        "inventory_list": inventory_list,
        "error_message": error_message,
        "location_list": location_list,
    }

    if request.method == "POST":
        upc = request.POST.get("obj_upc")
        retail_price = request.POST.get(f"retail_price_{upc}")
        store_price = request.POST.get(f"store_price_{upc}")
        total = request.POST.get(f"total_{upc}")
        location = request.POST.get(f"location_id_{upc}")
        is_active = request.POST.get(f"is_active_{upc}")
        print(upc, retail_price, store_price, total, location, is_active)
        inventory_obj = ProductInventory.objects.filter(upc=upc)
        inventory_obj.update(
            retail_price=retail_price,
            store_price=store_price,
            total=total,
            location=location,
            is_active=is_active)
        print("-------inventory_obj-----SAVE---")
        return redirect("inventory:inventory_mg")
    return render(request, "inventory.html", content)


@login_required
def inventory_delete(request, upc):
    error_message = "Item can't be delete, because item's total greater than 0"
    try:
        inventory_obj = ProductInventory.objects.get(upc=upc)
        if inventory_obj.total == 0:
            inventory_obj.delete()
            Product.objects.get(upc=upc).delete()
            return redirect("inventory:inventory_mg")
    except ProductInventory.DoesNotExist:
        error_message = "Inventory item not found."

    category_list = Category.objects.all()
    type_list = ProductType.objects.all()
    brand_list = Brand.objects.all()
    product_list = Product.objects.all().order_by("product_id")
    inventory_list = ProductInventory.objects.all().order_by("product_id")

    for obj in inventory_list:
        obj.product_obj = Product.objects.get(upc=obj.upc)

    location_list = Location.objects.filter(is_active=True)

    content = {
        "category_list": category_list,
        "type_list": type_list,
        "brand_list": brand_list,
        "product_list": product_list,
        "inventory_list": inventory_list,
        "error_message": error_message,
        "location_list": location_list,
    }

    return render(request, "inventory.html", content)


# =============================      Search   =================================
@login_required
def search(request):
    print("-------search page-------")
    category_list = Category.objects.all()
    type_list = ProductType.objects.all()
    brand_list = Brand.objects.all()
    product_list = Product.objects.all().order_by("product_id")

    def sub_search(request, inventory_list):
        for obj in inventory_list:
            obj.product_obj = Product.objects.get(upc=obj.upc)

        location_list = Location.objects.filter(is_active=True)

        content = {
            "category_list": category_list,
            "type_list": type_list,
            "brand_list": brand_list,
            "product_list": product_list,
            "inventory_list": inventory_list,
            "location_list": location_list,
        }

        return render(request, "inventory.html", content)

    inventory = ProductInventory.objects.all()
    if request.method == "POST":
        doc_type = request.POST.get("doc_type")
        keywords = request.POST.get("keyword")
        print("doc_type and keyword", doc_type, keywords)

        if doc_type == "Name":
            inventory_list = inventory.filter(product_name__name__icontains=keywords).order_by("product_id")
            return sub_search(request, inventory_list)
        elif doc_type == "ID":
            if keywords.isdigit():
                inventory_list = inventory.filter(product_name__id=keywords).order_by("product_id")
                return sub_search(request, inventory_list)
        else:
            inventory_list = inventory.filter(upc=keywords).order_by("product_id")
            return sub_search(request, inventory_list)

    return sub_search(request, inventory)


# =============================      Location   =================================

@login_required
def location_add(request):
    data_list = Location.objects.all()
    if request.method == "GET":
        return render(request, "location_add.html", {"data_list": data_list})
    else:
        location = request.POST.get("location")
        is_active = request.POST.get("is_active")
        Location.objects.create(location=location, is_active=is_active)
        return render(request, "location_add.html", {"data_list": data_list})


@login_required
def location_edit(request, id):
    obj = Location.objects.filter(id=id).first()

    if request.method == "GET":

        return render(request, "location_edit.html", {"obj": obj})
    else:
        data_list = Location.objects.all()
        name = request.POST.get("location_name")
        if name is not None and 0 < len(name) < 30:
            obj = Brand.objects.filter(id=id).update(name=name)
            return redirect("inventory:location_add")
        else:
            return render(request, "location_edit.html", {"obj": obj, "error": "Invalid data"})


@login_required
def location_delete(request, id):
    if request.method == "GET":
        location_obj = get_object_or_404(Location, id=id)
        location_obj.delete()
        return redirect("inventory:location_add")
    return redirect("inventory:location_add")


@login_required
def order_edit(request):
    if request.method == "POST":
        print("-------request.POST----")
        order_id = request.POST.get("order_id")
        order = get_object_or_404(Order, id=order_id)
        status = request.POST.get(f"ship_status_{order_id}")
        track = request.POST.get(f"tracking_{order_id}")
        print(order_id, status, track)

        order.ship_status = status
        order.tracking_number = track
        order.save()
        return redirect("inventory:admin_page")
    return redirect("inventory:admin_page")


