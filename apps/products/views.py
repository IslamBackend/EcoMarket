from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.products.models import Product, Category, Cart, CartItem, OrderCard, OrderedProduct
from apps.products.serializers import ProductSerializer, CategorySerializer, ProductDetailSerializer, \
    OrderCardSerializer, CartSerializer, HistorySerializer, HistoryDetailSerializer


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


class CartAPIView(APIView):
    def get(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        serializer = CartSerializer(cart)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)


class AddToCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, id=id)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class CartItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_cart_item(self, request, id):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, id=id)
        cart_item, _ = CartItem.objects.get_or_create(cart=cart, product=product)
        return cart_item

    def post(self, request, id):
        cart_item = self.get_cart_item(request, id)
        quantity = request.data.get('quantity')
        if quantity is not None and int(quantity) >= 0:
            cart_item.quantity = quantity
            cart_item.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("Invalid quantity", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        cart_item = self.get_cart_item(request, id)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        serializer = OrderCardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        validated_data['user'] = request.user

        order = OrderCard.objects.create(**validated_data)

        total_price = 0
        for cart_item in cart.items.all():
            ordered_product = OrderedProduct(order=order, product=cart_item.product, quantity=cart_item.quantity)
            ordered_product.save()
            total_price += cart_item.product.price * cart_item.quantity

        order.total_price = total_price
        order.save()

        order.cart_items.set(cart.items.all())

        cart.items.all().delete()

        return Response(status=status.HTTP_201_CREATED)


class OrderNumberAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        last_order = OrderCard.objects.filter(user=request.user).last()
        if last_order:
            return Response({
                "order_number": last_order.order_number,
                "created_at": last_order.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No orders found"}, status=status.HTTP_404_NOT_FOUND)


class HistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        history = OrderCard.objects.filter(user=request.user)
        serializer = HistorySerializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HistoryDetailAPIView(APIView):
    def get(self, request, id):
        history = OrderCard.objects.get(id=id)
        serializer_context = {'request': request}
        serializer = HistoryDetailSerializer(history, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)
