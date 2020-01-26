from django.utils import timezone
from django.db import models
from users.models import CustomUser as User


class MatchManager(models.Manager):
    def create_match(self, user_1, user_2):
        """ Makes a match between the two given users """
        match = self.model(user_1=user_1, user_2=user_2)
        match.save()
        return match

    def unmatch(self, match):
        """ Marks given match as 'unmatched' """
        match.unmatched = True
        match.save()
        return match

    def list_matches(self, user_id):
        """ Returns a QuerySet of all matches a user is part of """
        return self.filter(
            (models.Q(user_1=user_id) | models.Q(user_2=user_id))
            & models.Q(unmatched=False)
        )


class Match(models.Model):
    user_1 = models.ForeignKey(User, related_name="user_1", on_delete=models.CASCADE)
    user_2 = models.ForeignKey(User, related_name="user_2", on_delete=models.CASCADE)
    unmatched = models.BooleanField(default=False)
    top5 = models.BooleanField(default=False)

    objects = MatchManager()

    class Meta:
        verbose_name_plural = "Matches"


class MessageManager(models.Manager):
    def create_message(self, match, sender, content):
        """creates a message object."""
        message = self.model(
            match=match, sender=sender, content=content, sent=timezone.now()
        )
        message.save()
        return message

    def list_messages(self, match):
        """Returns a QuerySet of all messages for a given match ordered by time sent."""
        return self.filter(match=match).order_by('sent')


class Message(models.Model):
    match = models.ForeignKey(Match, related_name="match", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    content = models.TextField()
    sent = models.DateTimeField(null=True)
    delivered = models.DateTimeField(null=True)
    read = models.BooleanField(null=True)

    objects = MessageManager()
