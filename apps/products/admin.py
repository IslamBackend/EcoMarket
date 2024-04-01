from django.contrib import admin

from apps.products.models import Product, Category, OrderCard, CartItem, Cart


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category')
    search_fields = ('title',)


@admin.register(OrderCard)
class OrderCardAdmin(admin.ModelAdmin):
    list_display = ('address', 'phone_number')
    search_fields = ('phone_number',)


@admin.register(Cart)
class CardAdmin(admin.ModelAdmin):
    list_display = ('user', 'unique_id')
    search_fields = ('user',)


@admin.register(CartItem)
class CardAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product')
    search_fields = ('cart',)
