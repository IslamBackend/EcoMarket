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


class OrderCard(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='order')
    address = models.CharField(max_length=125, verbose_name='Address')
    phone_number = models.CharField(max_length=15, verbose_name='Phone Number')
    landmark = models.CharField(max_length=125, verbose_name='Landmark')
    comment = models.CharField(max_length=125, verbose_name='Comment')
