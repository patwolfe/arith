from django.db import models
from users.models import CustomUser as User


class InteractionManager(models.Manager):
    def skip(self, swiper, swipee):
        interaction, _ = self.get_or_create(swiper=swiper, swipee=swipee)
        interaction.skip_count += 1
        interaction.save()
        return interaction

    def smash(self, swiper, swipee):
        interaction, _ = self.get_or_create(swiper=swiper, swipee=swipee)
        interaction.choice = Interaction.SwipeType.SMASH
        interaction.save()
        return interaction


class Interaction(models.Model):
    class SwipeType(models.TextChoices):
        SKIP = "N"
        SMASH = "Y"

    swiper = models.ForeignKey(User, related_name="swiper", on_delete=models.CASCADE)
    swipee = models.ForeignKey(User, related_name="swipee", on_delete=models.CASCADE)
    choice = models.CharField(
        max_length=1, choices=SwipeType.choices, default=SwipeType.SKIP
    )
    skip_count = models.PositiveIntegerField(default=0)

    objects = InteractionManager()
