from celery import shared_task
from .models import Message

@shared_task
def message_task(message):
    return Message.objects.update_delivered(message["id"])