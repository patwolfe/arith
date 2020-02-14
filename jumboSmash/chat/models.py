from django.utils import timezone
from django.db import models
from users.models import User


class MatchManager(models.Manager):
    def create_match(self, user_1, user_2):
        """ Makes a match between the two given users """
        users = [user_1, user_2]
        users.sort(key=lambda x: x.id)
        match = self.create(user_1=users[0], user_2=users[1], last_active=timezone.now())
        return match

    def create_top5_match(self, user_1, user_2):
        """ Makes a top5 match between the two given users """
        match = self.create_match(user_1, user_2)
        match.top5 = True
        match.save()
        return match

    def unmatch(self, match):
        """ Marks given match as 'unmatched' """
        match.unmatched = True
        match.save()
        return match

    def mark_other_unviewed(self, match, user):
        """Updates given match to unviewed for the user who is not the one passed through."""
        if user == match.user_1:
            match.user_2_viewed = False
        else:
            match.user_1_viewed = False
        match.save()
        return match

    def mark_viewed(self, match, user):
        """Updates given match to viewed for the user who is passed through."""
        if user == match.user_1:
            match.user_1_viewed = True
        else:
            match.user_2_viewed = True
        match.save()
        return match

    def update_last_active(self, match):
        """Updates last active timestamp of given match to current time."""
        match.last_active = timezone.now()
        match.save()
        return match

    def list_matches(self, user):
        """ Returns a QuerySet of all matches a user is part of in order of last active."""
        return self.filter(
            (models.Q(user_1=user) | models.Q(user_2=user)) & models.Q(unmatched=False)
        ).order_by("-last_active")


class Match(models.Model):
    user_1 = models.ForeignKey(User, related_name="user_1", on_delete=models.CASCADE)
    user_2 = models.ForeignKey(User, related_name="user_2", on_delete=models.CASCADE)
    unmatched = models.BooleanField(default=False)
    top5 = models.BooleanField(default=False)
    user_1_viewed = models.BooleanField(default=False)
    user_2_viewed = models.BooleanField(default=False)
    last_active = models.DateTimeField()

    objects = MatchManager()

    class Meta:
        verbose_name_plural = "Matches"
        unique_together = [["user_1", "user_2"]]


class MessageManager(models.Manager):
    def create_message(self, match, sender, content):
        """creates a message object."""
        message = self.model(
            match=match, sender=sender, content=content, sent=timezone.now()
        )
        message.save()
        return message

    def update_delivered(self, id):
        """retrieves message by id and updates the delivered timestamp."""
        message = self.get(pk=id)
        message.delivered = timezone.now()
        message.save()
        return message

    def recent_message(self, match):
        """retrieves the most recent message for a given match."""
        messages = self.filter(match=match).order_by("-sent")
        if messages:
            return messages[0]
        else:
            return None

    def list_messages(self, match):
        """Returns a QuerySet of all messages for a given match ordered by time sent."""
        return self.filter(match=match).order_by("sent")


class Message(models.Model):
    match = models.ForeignKey(Match, related_name="match", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    content = models.TextField()
    sent = models.DateTimeField(null=True)
    delivered = models.DateTimeField(null=True)
    read = models.BooleanField(null=True)

    objects = MessageManager()
