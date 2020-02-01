from django.db import models, transaction
from django.db.models import F
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, ValidationError

import datetime
import uuid

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, first_name, last_name):
        user = self.model(email=self.normalize_email(email), first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        return user

    def create_staffuser(self, email, password, first_name, last_name):
        user = self.create_user(email, password, first_name, last_name)
        user.is_staff = True
        user.save()
        return user

    def create_superuser(self, email, password, first_name, last_name):
        user = self.create_user(email, password, first_name, last_name)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class User(AbstractUser):
    INACTIVE = "I"
    ACTIVE   = "A"
    BANNED   = "B"
    STATUS_CHOICES = (
        (INACTIVE, "Inactive"),
        (ACTIVE, "Active"),
        (BANNED, "Bannned")
    )

    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(("email address"), unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=100)
    preferred_name = models.CharField(max_length=30, blank=True, null=True)
    discoverable = models.BooleanField(default=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=INACTIVE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return self.email

class ProfileManager(models.Manager):
    pass

class Profile(models.Model):
    user = models.ForeignKey(User, related_name="profile", on_delete=models.CASCADE)
    bio = models.TextField()

    objects = ProfileManager()

class PhotoManager(models.Manager):
    def reorder(self, obj, new_order):
        qs = self.get_queryset()

        with transaction.atomic():
            if obj.order > int(new_order):
                qs.filter(
                    task=obj.task,
                    order__lt=obj.order,
                    order__gte=new_order
                ).exclude(
                    pk=obj.pk
                ).update(
                    order=F("order") + 1
                )
            else:
                qs.filter(
                    task=obj.task,
                    order__lte=new_order,
                    order__gt=obj.order
                ).exclude(
                    pk=obj.pk
                ).update(
                    order=F("order") - 1
                )

            obj.order = new_order
            obj.save()

class Photo(models.Model):
    user = models.ForeignKey(User, related_name="photo", on_delete=models.CASCADE)
    path = models.TextField()
    approved = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "approved", "order"], name="unique_user_photos")]

    objects = PhotoManager()
