from django.contrib import admin
from .models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ["id", "match", "content", "sent", "delivered", "read"]


admin.site.register(Message, MessageAdmin)
