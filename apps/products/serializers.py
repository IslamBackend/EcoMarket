from rest_framework import serializers
from apps.products.models import Category, Product


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
