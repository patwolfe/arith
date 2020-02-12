from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User, Profile
from django.utils.html import format_html
from django.urls import re_path, reverse
from django.http import HttpResponseRedirect


class UserAdmin(UserAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "preferred_name",
        "discoverable",
        "status",
        "needs_review",
    )
    ordering = ("needs_review", "email")

    list_filter = ("needs_review", "status")
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

    def change_view(self, request, object_id, form_url="", extra_context=None):
        approved_set, pending_set = Profile.objects.get_profiles(user=object_id)

        if approved_set:
            order = approved_set.photo_list()
            urls = approved_set.get_display_urls()
            approved_photos = [urls[x] for x in order if x is not None]
        else:
            approved_photos = []

        if pending_set:
            order = pending_set.photo_list()
            urls = pending_set.get_display_urls()
            pending_photos = [urls[x] for x in order if x is not None]
        else:
            pending_photos = []

        extra_context = extra_context or {}
        user = User.objects.get(id=object_id)
        extra_context["user_status"] = user.status
        extra_context["needs_review"] = user.needs_review
        extra_context["id_photo"] = user.id_photo
        extra_context["profiles"] = (Profile.objects.filter(user=object_id).first(),)
        extra_context["approved_photos"] = approved_photos
        extra_context["pending_photos"] = pending_photos
        return super(UserAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context
        )

    class Media:
        css = {"all": ("users/admin/admin.css",)}

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            re_path(
                r"^(?P<user_id>.+)/approve/$",
                self.admin_site.admin_view(self.approve),
                name="pending-user-approve",
            ),
            re_path(
                r"^(?P<user_id>.+)/reject/$",
                self.admin_site.admin_view(self.reject),
                name="pending-user-reject",
            ),
            re_path(
                r"^(?P<user_id>.+)/ban/$",
                self.admin_site.admin_view(self.ban),
                name="pending-user-ban",
            ),
            re_path(
                r"^(?P<user_id>.+)/unban/$",
                self.admin_site.admin_view(self.unban),
                name="pending-user-unban",
            ),
        ]
        return custom_urls + urls

    def approve(self, request, user_id, *args, **kwargs):
        User.objects.approve(user_id)
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    def reject(self, request, user_id, *args, **kwargs):
        User.objects.reject(user_id)
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    def ban(self, request, user_id, *args, **kwargs):
        User.objects.ban(user_id)
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

    def unban(self, request, user_id, *args, **kwargs):
        User.objects.unban(user_id)
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


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
