from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User, Profile, Photo

class UserAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "preferred_name", "discoverable", "status", "is_staff")
    ordering = ("email",)

    list_filter = ("status", "is_staff")
    search_fields = ("email", "first_name", "last_name", "preferred_name")
    
    fieldsets = (
        ("About", {"fields": ("email", "password", "first_name", "last_name", "preferred_name", "discoverable")}),
        ("Permissions", {"fields": ("status", "is_staff")})
    )
    add_fieldsets = (
        ("About", {"fields": ("email", "password1", "password2", "first_name", "last_name", "preferred_name", "discoverable")}),
        ("Permissions", {"fields": ("status", "is_staff")})
    )


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "bio")

class PhotoAdmin(admin.ModelAdmin):
    list_display = ("user", "path", "approved", "order")
    ordering = ("user", "order", "-approved")

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Photo, PhotoAdmin)
