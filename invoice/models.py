from django.db import models
from inventory.models import Product, Size, Color

class Order(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=50, default="COD")
    coupon = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE, related_name = "items")
    product = models.ForeignKey(Product, on_delete = models.PROTECT)
    quantity = models.PositiveIntegerField()
    size = models.ForeignKey(Size, on_delete = models.PROTECT)
    color = models.ForeignKey(Color, on_delete = models.PROTECT)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)


 