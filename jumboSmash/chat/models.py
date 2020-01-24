from datetime import datetime
from django.db import models
from matches.models import Match
from users.models import CustomUser as User


class MessageManager(models.Manager):
    def create_message(self, match_id, sender_id, content):
        """creates a message object."""
        match = Match.objects.get(pk=match_id)
        sender = User.objects.get(pk=sender_id)
        # there should be an error if sender is not user_1 or user_2 of match
        # should be checked for at a higher level?
        message = self.model(match=match, sender=sender, content=content, sent=datetime.now())
        message.save()
        return message


class Message(models.Model):
    match = models.ForeignKey(Match, related_name="match", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    content = models.TextField()
    sent = models.DateTimeField(null=True)
    delivered = models.DateTimeField(null=True)
    read = models.BooleanField(null=True)

    objects = MessageManager()
