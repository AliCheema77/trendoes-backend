from django.db.models import Avg, Count, Prefetch, FloatField
from django.db.models.functions import Coalesce
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category, SubCategory, Color, Size, Gender, Brand, Image, Stock, Review
from .serializers import ProductSerializer, ReviewSerializer
from .throttles import ProductListSellThrottle, ProductDetailThrottle
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .filters import ProductFilter


class ProductListSellView(generics.ListAPIView):

    
    throttle_classes = [ProductListSellThrottle]
    queryset = Product.objects.filter(is_active=True).annotate(
        ratingValue=Coalesce(Avg('reviews__rating'), 4.5, output_field=FloatField()),
        totalReviews=Coalesce(Count('reviews'), 600)
    ).select_related(
        'category', 'subcategory', 'gender', 'brand', 'color'
    ).prefetch_related(
        'images',
        Prefetch('stocks', queryset=Stock.objects.select_related('size', 'color'))
    )
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    @method_decorator(cache_page(300))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductDetailView(generics.RetrieveAPIView):
    
    serializer_class = ProductSerializer
    throttle_classes = [ProductDetailThrottle]
    queryset = Product.objects.filter(is_active=True).annotate(
        ratingValue=Coalesce(Avg('reviews__rating'), 4.5, output_field=FloatField()),
        totalReviews=Coalesce(Count('reviews'), 1100)
    ).select_related(
        'category', 'subcategory', 'gender', 'brand', 'color'
    ).prefetch_related(
        'images',
        Prefetch('stocks', queryset=Stock.objects.select_related('size', 'color'))
    )
    

class BestProductsListView(APIView):
    throttle_classes = [ProductListSellThrottle]

    @method_decorator(cache_page(600))
    def get(self, request):
        best_seller = Product.objects.order_by('-total_sold')[:5]
        serializer = ProductSerializer(best_seller, many = True, context = {"request":request})
        return Response(serializer.data, status = status.HTTP_200_OK)
    


class ProudctReviewView(APIView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        serializer = ReviewSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Thank you for your honest review"}, status=status.HTTP_201_CREATED)

        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
