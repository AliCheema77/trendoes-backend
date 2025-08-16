from django.db import models
from decimal import Decimal
from django_ckeditor_5.fields import CKEditor5Field


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class Color(models.Model):
    name = models.CharField(max_length=100)
    rgb_code = models.CharField(max_length=10, unique=True, help_text="rgb color code", null=True, blank=True)

    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Gender(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

BRAND_TYPE = (
    ("1", "National"),
    ("2", "International"),
    ("3", "Both")
)

class Brand(models.Model):
    name = models.CharField(max_length=100)
    origin = models.CharField(choices=BRAND_TYPE, max_length=13, null=True, blank=True)
    logo = models.ImageField(upload_to="brand_logo", null=True, blank=True)
    active = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

        
class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    actual_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)  
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)      
    is_active = models.BooleanField(default=True, null=True, blank=True)     
    total_sold = models.PositiveIntegerField(null=True, blank = True)
    def save(self, *args, **kwargs):
        discount = self.discount_percent / Decimal('100')
        self.price = self.actual_price * (Decimal('1.0') - discount)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"Image for {self.product.name}"

class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stocks')
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ('product', 'size', 'color')

    def __str__(self):
        return f"{self.product.name} - {self.size.name} - {self.color.name} - {self.quantity}"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=100)
    rating = models.PositiveIntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.rating} Stars"
