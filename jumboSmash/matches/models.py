from django.db import models
from users.models import CustomUser as User


class MatchManager(models.Manager):
    def create_match(self, user_id_1, user_id_2):
        """ Makes a match between the two given users """
        user_1 = User.objects.get(pk=user_id_1)
        user_2 = User.objects.get(pk=user_id_2)
        match = self.model(user_1=user_1, user_2=user_2)
        match.save()
        return match

    def unmatch(self, match_id):
        """ Marks given match as 'unmatched' """
        match = self.get(pk=match_id)
        match.unmatched = True
        match.save()
        return match


class Match(models.Model):
    user_1 = models.ForeignKey(User, related_name="user_1", on_delete=models.CASCADE)
    user_2 = models.ForeignKey(User, related_name="user_2", on_delete=models.CASCADE)
    unmatched = models.BooleanField(default=False)
    top5 = models.BooleanField(default=False)

    objects = MatchManager()

    class Meta:
        verbose_name_plural = "Matches"
