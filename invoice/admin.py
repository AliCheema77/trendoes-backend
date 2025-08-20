from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ("product", "quantity", "size", "color", "price")
    extra = 0  
    can_delete = False 
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "total", "created_at", "payment_method")
    list_filter = ("payment_method", "created_at", "country")
    search_fields = ("id", "name", "email")
    inlines = [OrderItemInline]
    readonly_fields = ("created_at", "subtotal", "shipping_fee", "discount", "total")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity", "size", "color", "price")
    search_fields = ("order__id", "product__name")
