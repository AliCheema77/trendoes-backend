from django.urls import path
from . import views

urlpatterns = [
    path("product", views.ProductListSellView.as_view()),
    path("product/<int:pk>", views.ProductDetailView.as_view()),
    path("best_seller/", views.BestProductsListView.as_view()),
]
