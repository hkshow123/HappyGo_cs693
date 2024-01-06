import os

from django.shortcuts import get_object_or_404

from inventory.models import *
from inventory.models import Product, ProductType, Brand, Category, ProductInventory

current_time = datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib import messages
from inventory.forms import *
from .models import ShoppingCart, ShoppingCartItem
from django.contrib.auth.decorators import login_required
from .models import ShoppingCart, Order, OrderItem, Profiles
from .forms import ProfileForm
from django.shortcuts import render, redirect


def index(request):
    product_list = Product.objects.all().order_by('id')
    category_list = Category.objects.all().order_by('id')
    brand_list = Brand.objects.all().order_by('id')
    inventory_list = ProductInventory.objects.filter(is_active=True).all().order_by('product_id')
    media_list = Media.objects.all().order_by('upc')
    for obj in inventory_list:
        obj.product_obj = Product.objects.get(upc=obj.upc)

    content = {
        'product_list': product_list,
        'category_list': category_list,
        'brand_list': brand_list,
        'inventory_list': inventory_list,
        'media_list': media_list
    }
    return render(request, 'index.html', content)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('user_name')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(username, password, user)
        if user is not None and not user.is_admin:
            login(request, user)
            return redirect('products:user_view')
        else:
            messages.error(request, 'Invalid username or password or not a regular user')

    return render(request, 'user_login.html')


def user_logout(request):
    logout(request)
    print("Logged out successfully")
    return redirect('products:user_login')


def user_register(request):
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
                                         is_admin=False)

                messages.success(request, f'Account created for {user_name}!')
                return redirect('products:user_login')
    else:
        form = AdminRegistrationForm()

    return render(request, 'user_register.html', {'form': form})


@login_required
def view_cart(request):
    cart, created = ShoppingCart.objects.get_or_create(user=request.user)
    total_price = sum(item.product.store_price * item.quantity for item in cart.items.all())
    context = {'cart': cart, 'total_price': total_price}
    return render(request, 'shopping_cart.html', context)


@login_required
def add_to_cart(request, upc):
    product = get_object_or_404(ProductInventory, upc=upc)
    cart, created = ShoppingCart.objects.get_or_create(user=request.user)
    cart_item, created = ShoppingCartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('products:view_cart')


@login_required
def edit_to_cart(request):
    if request.method == 'POST':
        print("------edit_to_cart-----")

        if 'action' in request.POST and request.POST['action'] == 'checkout':
            print("------checkout-----")
            return redirect('products:checkout')

        cart, created = ShoppingCart.objects.get_or_create(user=request.user)
        for item in cart.items.all():
            quantity_field = f'quantity_{item.product.upc}'
            if quantity_field in request.POST:
                quantity = request.POST[quantity_field]
                if quantity.isdigit():
                    quantity = int(quantity)
                    item.quantity = quantity
                    item.save()
                    print("--------success------")

        return redirect('products:view_cart')

    return redirect('products:view_cart')


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(ShoppingCartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('products:view_cart')


@login_required
def user_view(request):
    if request.user.is_authenticated:
        return render(request, 'user_page.html', {'user': request.user})


@login_required
def profile_view(request):
    profile, created = Profiles.objects.get_or_create(user=request.user)
    current_user = request.user
    user_name = current_user.user_name
    email = current_user.admin_email
    user_id = current_user.id

    full_name = profile.full_name if profile.full_name else ""

    content = {
        'user_name': user_name,
        'email': email,
        'full_name': full_name,
        'user_id': user_id
    }
    return render(request, 'profiles.html', content)


@login_required
def profile_edit(request):
    profile, created = Profiles.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        profile.full_name = full_name
        profile.save()
        return redirect('products:profile_view')


@login_required
def address_view(request):
    profile, created = Profiles.objects.get_or_create(user=request.user)
    current_user = request.user
    full_name = profile.full_name if profile.full_name else ""
    street = profile.street if profile.street else ""
    city = profile.city if profile.city else ""
    state = profile.state if profile.state else ""
    zipcode = profile.zipcode if profile.zipcode else ""
    telephone = profile.telephone if profile.telephone else ""

    content = {
        'full_name': full_name,
        'street': street,
        'city': city,
        'state': state,
        'zipcode': zipcode,
        'telephone': telephone
    }

    return render(request, 'address.html', content)


@login_required
def address_edit(request):
    profile, created = Profiles.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your address has been updated.')
            return redirect('products:address_view')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profiles.html', {'form': form})


@login_required
def checkout(request):
    print("-------checkout---func------")
    cart = ShoppingCart.objects.get(user=request.user)

    total_price = sum(item.product.store_price * item.quantity for item in cart.items.all())
    if total_price > 0:
        print("$", total_price)
        if request.method == 'POST':
            print("-----checkout----POST-")
            profile, created = Profiles.objects.get_or_create(user=request.user)

            order = Order.objects.create(user=request.user,
                                         total_price=total_price,
                                         shipping_address=profile)
            print("----order obj created----")

            order_items = []
            for cart_item in cart.items.all():
                items_price = cart_item.product.store_price * cart_item.quantity
                inventory_obj = ProductInventory.objects.get(product_id=cart_item.product.product_id)
                if inventory_obj.total >= cart_item.quantity:
                    inventory_obj.total -= cart_item.quantity
                    inventory_obj.save()
                    order_item = OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        price=cart_item.product.store_price,
                        items_price=items_price
                    )
                    order_items.append(order_item)
                print("----order item created----")
                cart_item.delete()

            content = {
                'order': order,
                'profile': profile,
                'order_items': order_items,
                'total_price': total_price,
            }
            return render(request, 'order_detail.html', content)

        return render(request, 'checkout.html', {'cart': cart, 'total_price': total_price})


@login_required
def orders_view(request):
    profile = Profiles.objects.get(user=request.user),
    order_list = Order.objects.filter(user=request.user).order_by('created_at').all()
    # order_item_list = OrderItem.objects.filter(order=).order_by('created_at').all()
    content = {
        'order_list': order_list,
        'profile': profile,
    }

    return render(request, 'orders.html', content)


@login_required
def order_detail(request, order_id):
    profile, created = Profiles.objects.get_or_create(user=request.user)
    order = get_object_or_404(Order, pk=order_id)
    order_items = OrderItem.objects.filter(order=order)
    total_price = sum(item.price * item.quantity for item in order_items)
    context = {
        'order': order,
        'order_items': order_items,
        'total_price': total_price,
        'profile': profile,
    }
    return render(request, 'order_detail.html', context)


def dairy_view(request):
    category_obj = Category.objects.get(name='Dairy')
    product_types = ProductType.objects.filter(category_id=category_obj)

    product_list = Product.objects.all().order_by('id')
    category_list = Category.objects.all().order_by('id')
    brand_list = Brand.objects.all().order_by('id')
    inventory_list = (ProductInventory.objects.filter
                      (is_active=True, product_type_id__in=product_types).all().order_by('product_id'))
    media_list = Media.objects.all().order_by('upc')
    for obj in inventory_list:
        obj.product_obj = Product.objects.get(upc=obj.upc)

    content = {
        'product_list': product_list,
        'category_list': category_list,
        'brand_list': brand_list,
        'inventory_list': inventory_list,
        'media_list': media_list
    }
    return render(request, 'index.html', content)


def meat_view(request):
    category_obj = Category.objects.get(name='Meat')
    product_types = ProductType.objects.filter(category_id=category_obj)

    product_list = Product.objects.all().order_by('id')
    category_list = Category.objects.all().order_by('id')
    brand_list = Brand.objects.all().order_by('id')
    inventory_list = (ProductInventory.objects.filter
                      (is_active=True, product_type_id__in=product_types).all().order_by('product_id'))
    media_list = Media.objects.all().order_by('upc')
    for obj in inventory_list:
        obj.product_obj = Product.objects.get(upc=obj.upc)

    content = {
        'product_list': product_list,
        'category_list': category_list,
        'brand_list': brand_list,
        'inventory_list': inventory_list,
        'media_list': media_list
    }
    return render(request, 'index.html', content)


def fruit_view(request):
    category_obj = Category.objects.get(name='Fruit')
    product_types = ProductType.objects.filter(category_id=category_obj)

    product_list = Product.objects.all().order_by('id')
    category_list = Category.objects.all().order_by('id')
    brand_list = Brand.objects.all().order_by('id')
    inventory_list = (ProductInventory.objects.filter
                      (is_active=True, product_type_id__in=product_types).all().order_by('product_id'))
    media_list = Media.objects.all().order_by('upc')
    for obj in inventory_list:
        obj.product_obj = Product.objects.get(upc=obj.upc)

    content = {
        'product_list': product_list,
        'category_list': category_list,
        'brand_list': brand_list,
        'inventory_list': inventory_list,
        'media_list': media_list
    }
    return render(request, 'index.html', content)


def bakery_view(request):
    category_obj = Category.objects.get(name='Bakery')
    product_types = ProductType.objects.filter(category_id=category_obj)

    product_list = Product.objects.all().order_by('id')
    category_list = Category.objects.all().order_by('id')
    brand_list = Brand.objects.all().order_by('id')
    inventory_list = (ProductInventory.objects.filter
                      (is_active=True, product_type_id__in=product_types).all().order_by('product_id'))
    media_list = Media.objects.all().order_by('upc')
    for obj in inventory_list:
        obj.product_obj = Product.objects.get(upc=obj.upc)

    content = {
        'product_list': product_list,
        'category_list': category_list,
        'brand_list': brand_list,
        'inventory_list': inventory_list,
        'media_list': media_list
    }
    return render(request, 'index.html', content)


def item_search(request):
    if request.method == "POST":
        data = request.POST.get("item_search")
        if data is not None:
            inventory_list = ProductInventory.objects.filter(product_name__name__icontains=data).all().order_by("id")
            product_list = Product.objects.all().order_by('id')
            category_list = Category.objects.all().order_by('id')
            brand_list = Brand.objects.all().order_by('id')

            media_list = Media.objects.all().order_by('upc')
            for obj in inventory_list:
                obj.product_obj = Product.objects.get(upc=obj.upc)

            content = {
                'product_list': product_list,
                'category_list': category_list,
                'brand_list': brand_list,
                'inventory_list': inventory_list,
                'media_list': media_list
            }
            return render(request, 'index.html', content)


def product_detail(request, upc):
    product_obj = Product.objects.get(upc=upc)
    invent_obj = ProductInventory.objects.get(upc=upc)

    content = {"product_obj": product_obj,
               "invent_obj": invent_obj}

    return render(request, 'product.html', content)
