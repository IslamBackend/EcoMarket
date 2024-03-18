from rest_framework import serializers

from apps.products.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title', 'image')


class ProductSerializer(serializers.ModelSerializer):
    products_category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'products_category', 'title', 'image', 'price',)

    def get_products_category(self, obj):
        return obj.category.title
