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

    # def validate_unique(self, exclude=None):
    #     if self.approved:
    #         try:
    #             old_profile = Profile.objects.get(user=self.user.id, approved=self.approved)
    #             old_profile.approved = None
    #             old_profile.save()
    #         except ObjectDoesNotExist:
    #             pass
    #         except MultipleObjectsReturned:
    #             raise ValidationError("Multiple approved profiles found!")
    #     else:
    #         super(Profile, self).validate_unique(exclude)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "approved", "order"], name="unique_user_photos")]

    objects = PhotoManager()


"""
A user initially has no profile and creates a profile for approval
A user can edit their profile which creates a new profile that in unapproved
A user can edit their profile while their last one is unapproved. This deletes the previous unapproved one and a new unapproved profile is created
A user has at most two profiles at any one time, one approved, one not approved
A user is always shown the not approved one as that is the one they want to see and can re-edit
Other users are always shown the approved profile unless the user hides their profile

"""
"""
Photo Management:
Photos are stored in S3
Photos are tracked with a UUID
Users download photos using presigned URLs
Users upload photos using presigned URLs

"""


# class ProfileManager(models.Manager):
#     def edit(self, user_id, profile_data):
#         print(profile_data)
#         if user_id != str(profile_data["user"].id):
#             print("User %s tried editing profile of user %s." % (user_id, profile_data["user"].id))
#             return

#         defaults = {
#             "user": profile_data["user"],
#             "display_name": profile_data["display_name"],
#             "bio": profile_data["bio"],
#             "approved": False,
#             "photo_urls": profile_data["photo_urls"]
#         }
#         profile, created = self.update_or_create(defaults=defaults, user=user_id, approved=False)
#         return profile

# class Profile(models.Model):
#     user = models.ForeignKey(User, related_name="profile", on_delete=models.CASCADE)
#     display_name = models.CharField(max_length=100)
#     bio = models.TextField()
#     approved = models.BooleanField(default=False, null=True)
#     photo_urls = models.TextField()

#     objects = ProfileManager()

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(fields=["user", "approved"], name="")
#         ]

#     def validate_unique(self, exclude=None):
#         if self.approved:
#             try:
#                 old_profile = Profile.objects.get(user=self.user.id, approved=self.approved)
#                 old_profile.approved = None
#                 old_profile.save()
#             except ObjectDoesNotExist:
#                 pass
#             except MultipleObjectsReturned:
#                 raise ValidationError("Multiple approved profiles found!")
#         else:
#             super(Profile, self).validate_unique(exclude)

#     def save(self, *args, **kwargs):
#         print("here")
#         print(args)
#         print(kwargs)
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return "display_name: %s\nbio: %s\napproved: %s\nphoto_urls: %s\n" % (self.display_name, self.bio, self.approved, self.photo_urls)

