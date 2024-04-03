from rest_framework import serializers
from apps.products.models import Category, Product, OrderCard, Cart, CartItem, OrderedProduct


class ImageURLMixin:
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None


class CategorySerializer(serializers.ModelSerializer, ImageURLMixin):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'title', 'image')

    def get_image(self, obj):
        return self.get_image_url(obj)


class ProductSerializer(serializers.ModelSerializer, ImageURLMixin):
    products_category = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'products_category', 'title', 'image', 'price', 'amount')

    def get_products_category(self, obj):
        return obj.category.title

    def get_image(self, obj):
        return self.get_image_url(obj)


class ProductDetailSerializer(serializers.ModelSerializer, ImageURLMixin):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'image', 'price', 'amount')

    def get_image(self, obj):
        return self.get_image_url(obj)


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('id', 'cart', 'product', 'quantity')


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('user', 'items', 'total_price')

    def get_total_price(self, obj):
        total_price = 0
        for item in obj.items.all():
            total_price += item.product.price * item.quantity
        return total_price


class OrderCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderCard
        fields = ('address', 'phone_number', 'landmark', 'comment')
        read_only_fields = ('user', 'total_price', 'order_number', 'created_at', 'cart_items')


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderCard
        fields = ('order_number', 'total_price')


class OrderedProductSerializer(serializers.ModelSerializer, ImageURLMixin):
    product_title = serializers.CharField(source='product.title', read_only=True)
    product_price = serializers.IntegerField(source='product.price', read_only=True)
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = OrderedProduct
        fields = ('product_title', 'product_image', 'product_price', 'quantity')

    def get_product_image(self, obj):
        return self.get_image_url(obj.product)


class HistoryDetailSerializer(serializers.ModelSerializer):
    cart_items = serializers.SerializerMethodField()

    class Meta:
        model = OrderCard
        fields = ('order_number', 'created_at', 'total_price', 'cart_items')

    def get_cart_items(self, obj):
        ordered_products = obj.ordered_product.all()
        context = {'request': self.context.get('request')}
        serialized_products = OrderedProductSerializer(ordered_products, many=True, context=context)
        return serialized_products.data
