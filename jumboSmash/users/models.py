from django.db import models, transaction
from django.db.models import F
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import (
    ObjectDoesNotExist,
    MultipleObjectsReturned,
    ValidationError,
)
from .s3utils import create_presigned_url, create_presigned_post, delete_photos

import datetime
import uuid
import logging

logger = logging.getLogger("django")


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


class User(AbstractUser):
    INACTIVE = "I"
    ACTIVE = "A"
    REPORTED = "R"
    BANNED = "B"
    STATUS_CHOICES = (
        (INACTIVE, "Inactive"),
        (ACTIVE, "Active"),
        (REPORTED, "Reported"),
        (BANNED, "Bannned"),
    )

    username = None
    email = models.EmailField(("email address"), unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=100)
    preferred_name = models.CharField(max_length=30, blank=True, null=True)
    discoverable = models.BooleanField(default=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=INACTIVE)
    id_photo = models.URLField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    def __str__(self):
        return self.email

    def activate(self):
        """ Marks user as active and discoverable """
        if self.status == User.INACTIVE:
            self.status = User.ACTIVE
            self.discoverable = True
            self.save()
        else:
            logger.warning("User {} is not inactive, cannot activate".format(self.id))

    def id_upload_url(self):
        return create_presigned_post("{}/id.jpg".format(self.id))

    def id_photo(self):
        return create_presigned_url("{}/id.jpg".format(self.id))


class ProfileManager(models.Manager):
    def to_aws_key(self, user_id, photo_id):
        url_format = "{}/profile/{}.jpg"
        return url_format.format(user_id, photo_id)

    def get_upload_urls(self, user):
        "Gets all the upload url + fields for given user"
        approved, _ = self.get_profiles(user)

        max_id = approved.max_photo_id + 1 if approved else 0

        urls = []
        for i in range(max_id, max_id + 6):
            urls.append([i, create_presigned_post(self.to_aws_key(user.id, i))])
        return urls

    def get_profiles(self, user):
        """ Returns approved, pending profiles """
        return (
            self.filter(user=user, approved=True).first(),
            self.filter(user=user, approved=False).first(),
        )


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    approved = models.BooleanField(default=False)

    photo0 = models.IntegerField(null=True, blank=True)
    photo1 = models.IntegerField(null=True, blank=True)
    photo2 = models.IntegerField(null=True, blank=True)
    photo3 = models.IntegerField(null=True, blank=True)
    photo4 = models.IntegerField(null=True, blank=True)
    photo5 = models.IntegerField(null=True, blank=True)
    max_photo_id = models.IntegerField(default=0)

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
        """ Updates a profile, deletes removed photos from s3"""

        mfields = iter(self._meta.fields)
        photo_mods = [
            (f.attname, kwargs[f.attname])
            for f in mfields
            if f.attname in kwargs and f.attname.startswith("photo")
        ]

        old_photo_list = self.photo_list()
        logger.info(old_photo_list)

        for fname, fval in photo_mods:
            setattr(self, fname, fval)

        new_photo_list = self.photo_list()
        logger.info(new_photo_list)

        self.delete_photos(new_photo_list, old_photo_list)

        self.max_photo_id = max(self.max_photo_id, kwargs["max_photo_id"])
        self.bio = kwargs["bio"]

        super(Profile, self).save()
        return self

    def approve(self):
        # TODO concurrency, notify
        approved = Profile.objects.filter(user_id=self.user_id, approved=True).first()
        if approved:
            self.delete_photos(self.photo_list(), approved.photo_list())
            approved.delete()

        self.approved = True
        self.save()
        return self

    def reject(self):
        # TODO notify
        self.delete()

    def clean(self):
        photo_list_max = max([x for x in self.photo_list() if x is not None])
        if self.max_photo_id < photo_list_max:
            self.max_photo_id = photo_list_max

    def save(self, **kwargs):
        self.clean()
        return super(Profile, self).save(**kwargs)

    def delete_photos(self, new_photos, old_photos):
        logging.warning("UPDATING PHOTOS")

        to_delete = [x for x in old_photos if x not in new_photos]
        logging.warning(old_photos)
        logging.warning(new_photos)
        logging.warning(to_delete)

        if to_delete:
            delete_photos(
                [Profile.objects.to_aws_key(self.user.id, x) for x in to_delete]
            )


class ReviewProfile(Profile):
    class Meta:
        proxy = True
