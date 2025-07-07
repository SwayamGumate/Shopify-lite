from django.shortcuts import render, redirect
from .forms import ProductForm
from .models import Product
from django.contrib.auth.decorators import login_required
from .models import Cart
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("shopify:home")  # fixed: use proper named route
    else:
        form = ProductForm()
    return render(request, "shopifyapp/product.html", {"form": form})


def product_list(request):
    categories = ["men", "women", "kids", "kitchen", "studio"]
    products_by_category = {}

    for category in categories:
        products_by_category[category] = Product.objects.filter(category=category)

    return render(
        request,
        "shopifyapp/product_list.html",
        {"products_by_category": products_by_category},
    )


def home(request):
    categories = ["men", "women", "kids", "kitchen", "studio"]
    products_by_category = {}

    for category in categories:
        products_by_category[category] = Product.objects.filter(category=category)

    return render(
        request,
        "shopifyapp/home.html",
        {"products_by_category": products_by_category},
    )


def category_view(request, category):
    products = Product.objects.filter(category__iexact=category)
    return render(
        request,
        "shopifyapp/category.html",
        {
            "products": products,
            "category": category.title(),
        },
    )


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("shopify:view_cart")


def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    return render(
        request, "shopifyapp/cart.html", {"cart_items": cart_items, "total": total}
    )


def remove_from_cart(request, item_id):
    Cart.objects.filter(id=item_id, user=request.user).delete()
    return redirect("shopify:view_cart")


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login after registration
            return redirect("shopify:home")
    else:
        form = UserCreationForm()
    return render(request, "registration/registration.html", {"form": form})
