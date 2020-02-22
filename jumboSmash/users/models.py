from django.db import models, transaction
from django.db.models import F
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import (
    ObjectDoesNotExist,
    MultipleObjectsReturned,
    ValidationError,
)

import datetime
import uuid


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, first_name, last_name):
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        user.set_unusable_password()
        user.save()
        return user

    def create_staffuser(self, email, password, first_name, last_name):
        user = self.create_user(email, first_name, last_name)
        user.set_password(password)
        user.is_staff = True
        user.save()
        return user

    def create_superuser(self, email, password, first_name, last_name):
        user = self.create_user(email, first_name, last_name)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

    def edit(self, user_id, data):
        user = self.get(id=user_id)
        profile = data.pop("profile")
        photos = data.pop("photos")

        if user.status == User.INACTIVE:
            user.preferred_name = data["preferred_name"]
            user.id_photo = data["id_photo"]

        # TODO only set this if we need to reapprove photos or they are inactive
        user.needs_review = True

        user.discoverable = data["discoverable"]
        Profile.objects.edit(user_id, profile)
        Photo.objects.edit(user_id, photos)

        user.save()
        return user

    def approve(self, user_id):
        user = self.get(id=user_id)

        if user.status == User.INACTIVE:
            user.status = User.ACTIVE
            user.discoverable = True

        Photo.objects.approve(user_id)

        user.needs_review = False
        user.save()

    def reject(self, user_id):
        # TODO trigger email/push notification
        user = self.get(id=user_id)

        if user.status == User.INACTIVE:
            Profile.objects.reject(user_id)
            Photo.objects.reject(user_id)
        elif user.status == User.ACTIVE:
            Photo.objects.reject(user_id)

        user.needs_review = False
        user.save()

    def ban(self, user_id):
        user = self.get(id=user_id)
        user.status = User.BANNED
        user.save()

    def unban(self, user_id):
        user = self.get(id=user_id)
        user.status = User.ACTIVE
        user.save()


class User(AbstractUser):
    INACTIVE = "I"
    ACTIVE = "A"
    REPORTED = "R"
    BANNED = "B"
    STATUS_CHOICES = ((INACTIVE, "Inactive"), (ACTIVE, "Active"), (REPORTED, "Reported"), (BANNED, "Bannned"))

    username = None
    email = models.EmailField(("email address"), unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=100)
    preferred_name = models.CharField(max_length=30, blank=True, null=True)
    discoverable = models.BooleanField(default=False)
    needs_review = models.BooleanField(default=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=INACTIVE)
    id_photo = models.URLField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return self.email


class ProfileManager(models.Manager):
    def edit(self, user_id, data):
        profile, _ = self.get_or_create(user_id=user_id)
        profile.bio = data["bio"]
        profile.save()

    def reject(self, user_id):
        self.filter(user_id=user_id).delete()


class Profile(models.Model):
    user = models.ForeignKey(User, related_name="profile", on_delete=models.CASCADE)
    bio = models.TextField()

    objects = ProfileManager()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user"], name="unique_profile")]

    def get_profile(self):
        return {"user": self.user, "bio": self.bio}


class PhotoManager(models.Manager):
    def get_photos(self, user_id):
        photos = Photo.objects.filter(user_id=user_id)
        approved_photo = None
        unapproved_photo = None

        for photo in photos:
            if photo.approved:
                approved_photo = photo
            else:
                unapproved_photo = photo

        return approved_photo, unapproved_photo

    def edit(self, user_id, data):
        # TODO allow reordering of photos
        # TODO return changed bool
        defaults = {
            "user_id": user_id,
            "approved": False,
            "photo0": data["photo0"],
            "photo1": data["photo1"],
            "photo2": data["photo2"],
            "photo3": data["photo3"],
            "photo4": data["photo4"],
            "photo5": data["photo5"],
        }
        self.update_or_create(user_id=user_id, approved=False, defaults=defaults)

    def approve(self, user_id):
        approved_photo, unapproved_photo = self.get_photos(user_id)

        if unapproved_photo:
            if approved_photo:
                approved_photo.delete()
            unapproved_photo.approved = True
            unapproved_photo.full_clean()
            unapproved_photo.save()
        else:
            print(
                "Tried approving photos for user but no unapproved photos existed".format(
                    user_id
                )
            )

    def reject(self, user_id):
        # TODO trigger email/push notification
        self.filter(user_id=user_id, approved=False).delete()


class Photo(models.Model):
    user = models.ForeignKey(User, related_name="photo", on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    photo0 = models.URLField()
    photo1 = models.URLField()
    photo2 = models.URLField()
    photo3 = models.URLField()
    photo4 = models.URLField()
    photo5 = models.URLField()

    objects = PhotoManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "approved"], name="unique_photo")
        ]

    def __str__(self):
        return "User {} Photos ({})".format(
            self.user, "Approved" if self.approved else "Pending"
        )

    def get_photos(self):
        return {
            "photos": [
                self.photo0,
                self.photo1,
                self.photo2,
                self.photo3,
                self.photo4,
                self.photo5,
            ],
            "approved": self.approved,
        }
