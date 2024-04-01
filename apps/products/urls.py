from django.urls import path
from apps.products.views import ProductListAPIView, ProductDetailAPIView, CategoryListAPIView, \
    OrderCardAPIView, CartItemAPIView, CartAPIView

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:id>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('cart/', CartAPIView.as_view(), name='cart'),
    path('cart/item/<int:id>/', CartItemAPIView.as_view(), name='cart-item'),
    path('ordercard/', OrderCardAPIView.as_view(), name='order-card'),
]
