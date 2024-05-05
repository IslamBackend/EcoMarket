from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, username, password, is_superuser, is_staff, is_active):
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            username=username,
            is_superuser=is_superuser,
            is_staff=is_staff,
            is_active=is_active,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, username, password=None):
        return self._create_user(
            email=email,
            username=username,
            password=password,
            is_superuser=False,
            is_staff=False,
            is_active=False,
        )

    def create_superuser(self, email, username, password=None):
        return self._create_user(
            email=email,
            username=username,
            password=password,
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )
