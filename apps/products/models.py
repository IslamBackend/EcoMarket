from django.db import models


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
    price = models.PositiveIntegerField(default=1, verbose_name='Price')
