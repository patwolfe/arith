from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.forms import UserCreationForm, UserChangeForm
from users.models import User, Profile
from django.urls import path


class UserAdmin(UserAdmin):
    # add_form = UserCreationForm
    # form = UserChangeForm
    model = User
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "password", "first_name", "last_name")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "first_name", "last_name", "is_staff", "is_active"),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "bio"]

class PhotoAdmin(admin.ModelAdmin):
    list_display = ["user", "path", "approved"]

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
