from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = [
    ("men", "Men"),
    ("women", "Women"),
    ("kids", "Kids"),
    ("kitchen", "Kitchen"),
    ("studio", "Studio"),
]


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to="products/")

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

    def total_price(self):
        return self.product.price * self.quantity
