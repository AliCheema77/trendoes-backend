from rest_framework import serializers
from .models import Product, Image, Stock, Category, SubCategory, Color,Size, Gender, Brand

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ["id", "name"]


class ColorSerializer(serializers.ModelSerializer):
    hexCode = serializers.CharField(source="rgb_code")
    class Meta:
        model = Color
        fields = ["id", "name", "hexCode"]
        

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['id', 'name']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name"]


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ["id", "name"]

class ImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    alt = serializers.SerializerMethodField()

    def get_url(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url
    
    def get_alt(self, obj):
        return f"Product image of {obj.product.name} not found !!!"

    class Meta:
        model = Image
        fields = ['id', 'url', "alt"]


class StockSerializer(serializers.ModelSerializer):
    size = SizeSerializer()
    color = ColorSerializer()
    class Meta:
        model = Stock
        fields = ['id', 'size', 'color', 'quantity']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    subcategory = SubCategorySerializer()
    gender = GenderSerializer(allow_null = True)
    brand = BrandSerializer(allow_null = True)
    color = ColorSerializer(allow_null = True)
    images = ImageSerializer(many = True, read_only = True, allow_null= True)
    stocks = serializers.SerializerMethodField()
    pricing = serializers.SerializerMethodField()
    meta = serializers.SerializerMethodField()
    ratingValue = serializers.FloatField(read_only=True, default=0.0)
    totalReviews = serializers.IntegerField(read_only=True, default=0)
    total_sold = serializers.IntegerField(allow_null = True)

    def get_stocks(self, obj):
        stocks = obj.stocks.all()
        size_map = {}
        for stock in stocks:
            size_id = stock.size.id
            if size_id not in size_map:
                size_map[size_id]={
                    "size":{
                        "id":stock.size.id,
                        "name":stock.size.name
                    },
                    "colors":[]
                }
            size_map[size_id]["colors"].append({
                "color":{
                    "id": stock.color.id,
                    "name": stock.color.name,
                    "hexCode":stock.color.rgb_code
                },
                "quanitity": stock.quantity
            })
        return list(size_map.values())
    def get_pricing(self, obj):
        return{
            "actuall_price": float(obj.actual_price),
            "discountPercent":float(obj.discount_percent),
            "finalPrice":float(obj.price),
            "currecy":"PKR"
        }
    
    def get_meta(self, obj):
        return {
            "createdAt": obj.created_at.isoformat() if hasattr(obj, 'created_at') else None,
            "updatedAt": obj.updated_at.isoformat() if hasattr(obj, 'updated_at') else None,
            "isActive": getattr(obj, 'is_active', True)
        }

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category', 'subcategory', 'gender', 'brand', 'color',
            'description', 'pricing', 'images', 'stocks', 'meta', 'ratingValue', 'totalReviews', "total_sold",
        ]
