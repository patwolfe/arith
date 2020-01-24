from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager
import datetime


class CustomUserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, email, password):
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_staffuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
