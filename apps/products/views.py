from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.products.models import Product, Category, OrderCard, Cart, CartItem
from apps.products.serializers import ProductSerializer, CategorySerializer, ProductDetailSerializer, \
    OrderCardSerializer, CartSerializer


class CategoryListAPIView(APIView):
    def get(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductListAPIView(APIView):
    def get(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailAPIView(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, id=id)
        serializer = ProductDetailSerializer(product, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderCardAPIView(APIView):
    def get(self, request):
        product = OrderCard.objects.all()
        serializer = OrderCardSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartAPIView(APIView):
    def get(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        serializer = CartSerializer(cart)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)


class CartItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_cart_item(self, request, id):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, id=id)
        cart_item, _ = CartItem.objects.get_or_create(cart=cart, product=product)
        return cart_item

    def delete(self, request, id):
        cart_item = self.get_cart_item(request, id)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id):
        cart_item = self.get_cart_item(request, id)
        quantity = request.data.get('quantity', cart_item.quantity)
        cart_item.quantity = quantity
        cart_item.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
