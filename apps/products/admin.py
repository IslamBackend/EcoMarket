from django.contrib import admin

from apps.products.models import Product, Category, OrderCard, CartItem, Cart, OrderedProduct


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category')
    search_fields = ('title',)


@admin.register(Cart)
class CardAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user',)


@admin.register(CartItem)
class CardAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product')
    search_fields = ('cart',)


class OrderedProductInline(admin.TabularInline):
    model = OrderedProduct
    extra = 0


@admin.register(OrderCard)
class OrderCardAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'total_price', 'created_at')
    inlines = [OrderedProductInline]
