from django.contrib import admin
from .models import Match


class MatchAdmin(admin.ModelAdmin):
    list_display = ["id", "user_1", "user_2"]


admin.site.register(Match, MatchAdmin)
