from django.db import models, transaction
from django.db.models import F
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import (
    ObjectDoesNotExist,
    MultipleObjectsReturned,
    ValidationError,
)
from .s3utils import create_presigned_url, create_presigned_post

import datetime
import uuid
import logging


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, first_name, last_name):
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        user.save()
        return user

    def create_staffuser(self, email, password, first_name, last_name):
        user = self.create_user(email, first_name, last_name)
        user.is_staff = True
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, first_name, last_name):
        user = self.create_user(email, first_name, last_name)
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
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

        Profile.objects.approve(user_id)

        user.needs_review = False
        user.save()

    def reject(self, user_id):
        # TODO trigger email/push notification
        user = self.get(id=user_id)

        if user.status == User.INACTIVE:
            ProfileBody.objects.reject(user_id)
            Profile.objects.reject(user_id)
        elif user.status == User.ACTIVE:
            Profile.objects.reject(user_id)

        user.needs_review = False
        user.save()

    def ban(self, user_id):
        user = self.get(id=user_id)
        user.last_status = user.status
        user.status = User.BANNED
        user.save()

    def unban(self, user_id):
        user = self.get(id=user_id)
        user.status = user.last_status
        user.save()


class User(AbstractUser):
    INACTIVE = "I"
    ACTIVE = "A"
    BANNED = "B"
    STATUS_CHOICES = ((INACTIVE, "Inactive"), (ACTIVE, "Active"), (BANNED, "Bannned"))

    username = None
    email = models.EmailField(("email address"), unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=100)
    preferred_name = models.CharField(max_length=30, blank=True, null=True)
    discoverable = models.BooleanField(default=False)
    needs_review = models.BooleanField(default=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=INACTIVE)
    last_status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=INACTIVE
    )
    id_photo = models.URLField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return self.email


class ProfileManager(models.Manager):
    def to_aws_key(self, user_id, photo_id):
        url_format = "{}/profile/{}.jpg"
        return url_format.format(user_id, photo_id)

    def get_upload_urls(self, user_id):
        "Gets all the upload url + fields for given user"
        urls = []
        for i in range(6, 12):
            urls.append([i, create_presigned_post(self.to_aws_key(user_id, i))])
        return urls

    def approve(self, user_id):
        pending_set = self.filter(user_id=user_id, approved=True).first()
        if pending_set:
            self.filter(user_id=user_id, approved=True).delete()
            pending_set.approved = True
            pending_set.save()
            return pending_set
        else:
            logging.warning(
                "Cannot approve photos for user {}, no pending photos exist".format(
                    user_id
                )
            )

    def reject(self, user_id):
        # TODO trigger email/push notification
        self.filter(user_id=user_id, approved=False).delete()

    def get_profiles(self, user):
        return (
            self.filter(user=user, approved=True).first(),
            self.filter(user=user, approved=False).first(),
        )


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    approved = models.BooleanField(default=False)

    photo0 = models.IntegerField(null=True)
    photo1 = models.IntegerField(null=True)
    photo2 = models.IntegerField(null=True)
    photo3 = models.IntegerField(null=True)
    photo4 = models.IntegerField(null=True)
    photo5 = models.IntegerField(null=True)

    bio = models.TextField()

    objects = ProfileManager()

    # Note 0-5 are approved, 6-11 are reserved for uploads
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "approved"], name="unique_profile")
        ]

    def __str__(self):
        return "User {} Profile ({})".format(
            self.user, "Approved" if self.approved else "Pending"
        )

    def photo_list(self):
        """ Returns list of photo ids """
        list = []
        for i in range(0, 6):
            list.append(getattr(self, "photo" + str(i)))
        return list

    def get_display_urls(self):
        """ Gets display urls for photos in set and returns them as a id:url mapping """
        urls = {}
        for photo in self.photo_list():
            if photo:
                urls[photo] = create_presigned_url(
                    Profile.objects.to_aws_key(self.user.id, photo)
                )
        return urls

    def is_photo_reorder(self, profile2):
        """ Returns true if the profile2 is the same as the current profile just with photos rearranged """
        curr_img_list = self.photo_list()
        # should check for duplicates
        for img in profile2.photo_list():
            if img is not None and img not in curr_img_list:
                return False
        return self.bio == profile2.bio

    def update(self, **kwargs):
        mfields = iter(self._meta.fields)
        mods = [(f.attname, kwargs[f.attname]) for f in mfields if f.attname in kwargs]
        for fname, fval in mods:
            setattr(self, fname, fval)
        super(Profile, self).save()
        return self


class ReviewProfile(Profile):
    class Meta:
        proxy = True
