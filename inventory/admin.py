from django.contrib import admin
from .models import (
    Category, SubCategory, Color, Size, Gender,
    Brand, Product, Image, Stock, Review
)
from .forms import ProductForm

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

class StockInline(admin.TabularInline):
    model = Stock
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ['name', 'category', 'subcategory', 'brand', 'actual_price', 'discount_percent', 'price', "total_sold"]
    list_filter = ['category', 'subcategory', 'brand', 'gender']
    search_fields = ['name']
    inlines = [ImageInline, StockInline]
    

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ["product", "size", "color", "quantity"]
    list_filter = ['size', 'color']
    search_fields = ["product__name"]

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Gender)
admin.site.register(Brand)
admin.site.register(Review)
