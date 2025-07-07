from django.urls import path
from . import views
from .views import register_view

app_name = "shopify"

urlpatterns = [
    path("add/", views.add_product, name="add_product"),
    path("register/", register_view, name="register"),  # 👈 Move this above category!
    path("cart/", views.view_cart, name="view_cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("", views.home, name="home"),
    path("<str:category>/", views.category_view, name="category"),  # 👈 Keep this LAST
]
