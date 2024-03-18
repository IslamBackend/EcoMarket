from rest_framework.generics import ListAPIView

from apps.products.models import Product, Category
from apps.products.serializers import ProductSerializer, CategorySerializer


class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

