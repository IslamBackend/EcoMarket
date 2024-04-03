import uuid

from django.db import models

from apps.users.models import CustomUser


class Category(models.Model):
    title = models.CharField(max_length=125, unique=True, verbose_name='Category Title')
    image = models.ImageField(upload_to='category', verbose_name='Image')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Category')
    title = models.CharField(max_length=125, verbose_name='Product Title')
    image = models.ImageField(upload_to='product', verbose_name='Image')
    price = models.PositiveIntegerField(default=0, verbose_name='Price')
    amount = models.PositiveIntegerField(default=0, verbose_name='Amount')
    description = models.TextField(max_length=255, verbose_name='Description')

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class OrderCard(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, verbose_name='Address')
    phone_number = models.CharField(max_length=15, verbose_name='Phone Number')
    landmark = models.CharField(max_length=255, verbose_name='Landmark')
    comment = models.TextField(blank=True, verbose_name='Comment')
    total_price = models.PositiveIntegerField(default=0, verbose_name='Total Price')
    order_number = models.CharField(max_length=8, unique=True, verbose_name='Order Number')
    created_at = models.DateTimeField(auto_now_add=True)
    cart_items = models.ManyToManyField(CartItem, related_name='orders')

    def save(self):
        if not self.order_number:
            self.order_number = self.generate_uuid()
        super().save()

    def generate_uuid(self):
        return str(uuid.uuid4())[:8]


class OrderedProduct(models.Model):
    order = models.ForeignKey(OrderCard, related_name='ordered_product', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
