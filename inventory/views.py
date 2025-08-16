from django.db.models import Avg, Count, Prefetch, FloatField
from django.db.models.functions import Coalesce
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Product, Category, SubCategory, Color, Size, Gender, Brand, Image, Stock, Review
from .serializers import ProductSerializer
from .throttles import ProductListSellThrottle, ProductDetailThrottle

class ProductListSellView(APIView):
    throttle_classes = [ProductListSellThrottle]

    def get(self, request):
        products = Product.objects.all()

        # Filtering by category, brand, and price range
        category = request.query_params.get('category')
        brand = request.query_params.get('brand')
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        
        if category:
            products = products.filter(category=category)
        if brand:
            products = products.filter(brand=brand)
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)
        # print("inside views for product\n",products)
        serializer = ProductSerializer(products, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        pass

class ProductDetailView(generics.RetrieveAPIView):
    
    serializer_class = ProductSerializer
    throttle_classes = [ProductDetailThrottle]
    queryset = Product.objects.filter(is_active=True).annotate(
        ratingValue=Coalesce(Avg('reviews__rating'), 0.0, output_field=FloatField()),
        totalReviews=Coalesce(Count('reviews'), 0)
    ).select_related(
        'category', 'subcategory', 'gender', 'brand', 'color'
    ).prefetch_related(
        'images',
        Prefetch('stocks', queryset=Stock.objects.select_related('size', 'color'))
    )
    

class BestProductsListView(APIView):
    throttle_classes = [ProductListSellThrottle]

    def get(self, request):
        best_seller = Product.objects.order_by('-total_sold')[:5]
        serializer = ProductSerializer(best_seller, many = True, context = {"request":request})
        return Response(serializer.data, status = status.HTTP_200_OK)