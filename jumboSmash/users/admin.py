from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User, Profile, Photo
from django.utils.html import format_html
from django.urls import re_path, reverse
from django.http import HttpResponseRedirect

class UserAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "preferred_name", "discoverable", "status", "is_staff")
    ordering = ("email",)

    list_filter = ("status", "status", "is_staff")
    search_fields = ("email", "first_name", "last_name", "preferred_name")
    
    fieldsets = ()
    fields = ("email", "first_name", "last_name", "status", "preferred_name", "discoverable")
    add_fieldsets = (
        ("About", {"fields": ("email", "password1", "password2", "first_name", "last_name", "preferred_name", "discoverable")}),
        ("Permissions", {"fields": ("status", "is_staff")})
    )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        user = User.objects.get(id=object_id)
        extra_context['user_status'] = user.status
        extra_context['id_photo'] = user.id_photo
        extra_context['profiles'] = map(lambda profile: profile.get_profile(), Profile.objects.filter(user=object_id))
        extra_context['photo_sets'] = map(lambda photo_set: photo_set.get_photos(), Photo.objects.filter(user=object_id))
        return super(UserAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)

    class Media: 
        css = {'all': ('users/admin/admin.css',)}

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            re_path(
                r'^(?P<user_id>.+)/approve/$',
                self.admin_site.admin_view(self.approve),
                name='pending-user-approve',
            ),
            re_path(
                r'^(?P<user_id>.+)/reject/$',
                self.admin_site.admin_view(self.reject),
                name='pending-user-reject',
            ),
            re_path(
                r'^(?P<user_id>.+)/ban/$',
                self.admin_site.admin_view(self.ban),
                name='pending-user-ban',
            ),
            re_path(
                r'^(?P<user_id>.+)/unban/$',
                self.admin_site.admin_view(self.unban),
                name='pending-user-unban',
            )
        ]
        return custom_urls + urls

    def approve(self, request, user_id, *args, **kwargs):
        User.objects.approve(user_id)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def reject(self, request, user_id, *args, **kwargs):
        User.objects.reject(user_id)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def ban(self, request, user_id, *args, **kwargs):
        User.objects.ban(user_id)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def unban(self, request, user_id, *args, **kwargs):
        User.objects.unban(user_id)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

admin.site.register(User, UserAdmin)
