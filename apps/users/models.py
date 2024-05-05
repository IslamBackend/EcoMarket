from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.users.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, verbose_name='Username')
    password = models.CharField(max_length=150, verbose_name='Password')
    email = models.EmailField(max_length=100, unique=True, verbose_name='E-mail')
    otp = models.CharField(max_length=4, blank=True, null=True, verbose_name='otp')
    is_active = models.BooleanField(default=False, verbose_name='Active')
    is_staff = models.BooleanField(default=False, verbose_name='Staff')
    is_superuser = models.BooleanField(default=False, verbose_name='Admin')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date Created')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email


class PasswordResetToken(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    time = models.DateTimeField()
