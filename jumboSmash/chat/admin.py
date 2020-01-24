from django.contrib import admin
from .models import Message, Match


class MessageAdmin(admin.ModelAdmin):
    list_display = ["id", "match", "content", "sent", "delivered", "read"]


admin.site.register(Message, MessageAdmin)


class MatchAdmin(admin.ModelAdmin):
    list_display = ["id", "user_1", "user_2"]


admin.site.register(Match, MatchAdmin)
