from django.db import models
from users.models import CustomUser as User


class InteractionManager(models.Manager):
    def skip(self, swiper, swipe_target):
        """ Records a left (negative) swipe on a profile """
        interaction, _ = self.get_or_create(swiper=swiper, swipe_target=swipe_target)
        if interaction.choice != Interaction.SwipeType.SMASH:
            # You shouldn't be able to skip when you've already smashed,
            # not sure what the error handling here should be
            interaction.skip_count += 1
            interaction.save()
        return interaction

    def smash(self, swiper, swipe_target):
        """ Records a right (positive) swipe on a profile """
        interaction, _ = self.get_or_create(swiper=swiper, swipe_target=swipe_target)
        interaction.choice = Interaction.SwipeType.SMASH
        interaction.save()
        return interaction


class Interaction(models.Model):
    class SwipeType(models.TextChoices):
        SKIP = "N"
        SMASH = "Y"

    swiper = models.ForeignKey(User, related_name="swiper", on_delete=models.CASCADE)
    swipe_target = models.ForeignKey(
        User, related_name="swipe_target", on_delete=models.CASCADE
    )
    choice = models.CharField(
        max_length=1, choices=SwipeType.choices, default=SwipeType.SKIP
    )
    skip_count = models.PositiveIntegerField(default=0)

    objects = InteractionManager()
