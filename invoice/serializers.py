from rest_framework import serializers
from .models import Order, OrderItem
from django.db import transaction
from inventory.models import Product, Size, Color, Stock

class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'size', 'color', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id', 'name', 'email', 'phone', 'street', 'city', 'postal_code', 'country',
            'payment_method', 'coupon', 'notes', 'subtotal', 'shipping_fee', 'discount',
            'total', 'created_at', 'items'
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            for item_data in items_data:
                order_item = OrderItem.objects.create(order=order, **item_data)
                
                try:
                    # Lock the stock row for update
                    stock = Stock.objects.select_for_update().get(
                        product=order_item.product,
                        size=order_item.size,
                        color=order_item.color
                    )
                    
                    if stock.quantity >= order_item.quantity:
                        stock.quantity -= order_item.quantity
                        stock.save()
                    else:
                        # Not enough stock, transaction will be rolled back.
                        raise serializers.ValidationError(
                            f"Not enough stock for {order_item.product.name} "
                            f"(Size: {order_item.size}, Color: {order_item.color}). "
                            f"Only {stock.quantity} left, but {order_item.quantity} were requested."
                        )
                except Stock.DoesNotExist:
                    # Stock for this specific product variant doesn't exist.
                    raise serializers.ValidationError(
                        f"Stock for {order_item.product.name} "
                        f"(Size: {order_item.size}, Color: {order_item.color}) does not exist."
                    )
        return order