from django.contrib import admin
from .models import Message

#do we need admin site for messages?
admin.site.register(Message)
