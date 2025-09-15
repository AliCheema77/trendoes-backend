import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name = "name", lookup_expr = "icontains")
    category = django_filters.CharFilter(field_name= "category__name", lookup_expr= "icontains")
    gender = django_filters.CharFilter(field_name = "gender__name", lookup_expr = "icontains")  
    brand = django_filters.CharFilter(field_name = "brand__name", lookup_expr = "icontains")
    min_price = django_filters.NumberFilter(field_name = "price", lookup_expr = "gte")
    max_price = django_filters.NumberFilter(field_name = "price", lookup_expr = "lte")

    
    class Meta:
        model = Product
        fields = ['name', 'category','gender', 'brand', 'min_price', 'max_price']