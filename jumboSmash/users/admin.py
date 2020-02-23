from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User, Profile, ProfileReview
from django.utils.html import format_html
from django.urls import re_path, reverse
from django.http import HttpResponseRedirect
from difflib import SequenceMatcher
import logging


def list_photo_urls(profile):
    """ Lists display URLs for a profile, [] if None"""
    if profile:
        order = profile.photo_list()
        urls = profile.get_display_urls()
        photos = [urls[x] for x in order if x is not None]
    else:
        photos = []
    return photos


def wrap_with(text, tag):
    """ Inserts tags (as format string) into string at line breaks"""
    paragraphs = text.split("\n")
    html_list = list(map(lambda x: tag.format(x), paragraphs))
    return "\n".join(html_list)


def gen_diff_html(old_profile, new_profile):
    """ Creates 2 HTML strings to display as bio diff"""
    deleted = '<span class="deleted">{}</span>'
    added = '<span class="added">{}</span>'
    p = "<p>{}</p>"

    old_bio_diff = ""
    new_bio_diff = ""

    if old_profile is None:
        old_bio_diff = ""
        new_bio_diff = new_profile.bio
    else:
        a = old_profile.bio
        b = new_profile.bio
        diffs = SequenceMatcher(a=a, b=b).get_opcodes()
        for opcode, i1, i2, j1, j2 in diffs:
            if opcode == "replace":
                old_bio_diff += wrap_with((a[i1:i2]), deleted)
                new_bio_diff += wrap_with((b[j1:j2]), added)
            elif opcode == "delete":
                old_bio_diff += wrap_with(a[i1:i2], deleted)
            elif opcode == "insert":
                new_bio_diff += wrap_with(b[j1:j2], added)
            elif opcode == "equal":
                old_bio_diff += a[i1:i2]
                new_bio_diff += a[i1:i2]

    return wrap_with(old_bio_diff, p), wrap_with(new_bio_diff, p)


class UserAdmin(UserAdmin):
    list_display = (
        "email",
        "first_name",
        "preferred_name",
        "last_name",
        "discoverable",
        "status",
    )
    ordering = ["email"]

    list_filter = ["status"]
    search_fields = ("email", "first_name", "last_name", "preferred_name")

    fieldsets = ()
    fields = (
        "email",
        "first_name",
        "last_name",
        "status",
        "preferred_name",
        "discoverable",
    )
    add_fieldsets = (
        (
            "About",
            {
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "preferred_name",
                    "discoverable",
                )
            },
        ),
        ("Permissions", {"fields": ("status", "is_staff")}),
    )


admin.site.register(User, UserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "photo0",
        "photo1",
        "photo2",
        "photo3",
        "photo4",
        "photo5",
        "bio",
        "approved",
    ]


admin.site.register(Profile, ProfileAdmin)


class ProfileReviewAdmin(admin.ModelAdmin):
    list_display = ["user", "user_status"]

    def user_status(self, obj):
        return obj.user.get_status_display()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(approved=False)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        profile = Profile.objects.get(id=object_id)
        user = profile.user
        approved_profile, pending_profile = Profile.objects.get_profiles(user=user)
        approved_bio, pending_bio = gen_diff_html(approved_profile, pending_profile)

        approved_photos = list_photo_urls(approved_profile)
        pending_photos = list_photo_urls(pending_profile)

        extra_context = extra_context or {}
        extra_context["user"] = user
        extra_context["approved_photos"] = approved_photos
        extra_context["pending_photos"] = pending_photos
        extra_context["approved_profile"] = approved_profile
        extra_context["pending_profile"] = pending_profile
        extra_context["approved_bio"] = approved_bio
        extra_context["pending_bio"] = pending_bio

        return super().change_view(
            request, object_id, form_url, extra_context=extra_context
        )

    class Media:
        css = {"all": ("users/admin/admin.css",)}

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            re_path(
                r"^(?P<profile_id>.+)/approve/$",
                self.admin_site.admin_view(self.approve),
                name="pending-profile-approve",
            ),
            re_path(
                r"^(?P<profile_id>.+)/approve_and_activate/$",
                self.admin_site.admin_view(self.approve_and_activate),
                name="pending-profile-approve-user-activate",
            ),
            re_path(
                r"^(?P<profile_id>.+)/reject/$",
                self.admin_site.admin_view(self.reject),
                name="pending-profile-reject",
            ),
        ]
        return custom_urls + urls

    def approve(self, request, profile_id, *args, **kwargs):
        profile = Profile.objects.get(pk=profile_id).approve()
        logging.info("User {} profile approved".format(profile.user.id))
        return HttpResponseRedirect("/admin/users/profilereview")

    def reject(self, request, profile_id, *args, **kwargs):
        profile = Profile.objects.get(pk=profile_id).reject()
        logging.info("User {} profile rejected".format(profile.user.id))
        return HttpResponseRedirect("/admin/users/profilereview")

    def approve_and_activate(self, request, profile_id, *args, **kwargs):
        profile = Profile.objects.get(pk=profile_id).approve()
        profile.user.activate()
        logging.info("User {} profile approved, user activated".format(profile.user.id))
        return HttpResponseRedirect("/admin/users/profilereview")


admin.site.register(ProfileReview, ProfileReviewAdmin)
