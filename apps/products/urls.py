from django.urls import path
from apps.products.views import ProductListAPIView, ProductDetailAPIView, CategoryListAPIView, \
    AddToCartAPIView, CartItemAPIView, CartAPIView, OrderCartAPIView, OrderNumberAPIView, \
    HistoryAPIView, HistoryDetailAPIView

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:id>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('cart/', CartAPIView.as_view(), name='cart'),
    path('cart/add/<int:id>/', AddToCartAPIView.as_view(), name='add-to-cart'),
    path('cart/item/<int:id>/', CartItemAPIView.as_view(), name='cart-item'),
    path('ordercard/', OrderCartAPIView.as_view(), name='order-card'),
    path('ordercard/number/', OrderNumberAPIView.as_view(), name='order-number'),
    path('history/', HistoryAPIView.as_view(), name='history'),
    path('history/<int:id>/', HistoryDetailAPIView.as_view(), name='history-detail'),
]
