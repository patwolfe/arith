from django.db import models
from users.models import CustomUser as User
from chat.models import Match


class InteractionManager(models.Manager):
    def skip(self, swiper, swiped_on):
        """ Records a left (negative) swipe on a profile """
        interaction, _ = self.get_or_create(swiper=swiper, swiped_on=swiped_on)
        if not interaction.smash:
            # You shouldn't be able to skip when you've already smashed,
            # not sure what the error handling here should be
            interaction.skip_count += 1
            interaction.smash = False
            interaction.save()
        else:
            assert 0, "Interaction already marked 'smash', cannot 'skip'"
        return interaction

    def smash(self, swiper, swiped_on):
        """ Records a right (positive) swipe on a profile """
        interaction, _ = self.get_or_create(swiper=swiper, swiped_on=swiped_on)
        if not interaction.smash:
            # We shouldn't research for a match if the type is already swipe
            # again, this shouldn't be happening so not sure what the best behavior is
            interaction.smash = True
            interaction.save()
            try:
                complement = self.get(swiper=swiped_on, swiped_on=swiper)
                if complement.smash:
                    Match.objects.create_match(swiper.id, swiped_on.id)
            except:
                pass
        else:
            assert 0, "Interaction already marked 'smash', cannot 'smash' again"

        return interaction


class Interaction(models.Model):
    swiper = models.ForeignKey(User, related_name="swiper", on_delete=models.CASCADE)
    swiped_on = models.ForeignKey(
        User, related_name="swiped_on", on_delete=models.CASCADE
    )
    smash = models.BooleanField(null=True)
    skip_count = models.PositiveIntegerField(default=0)

    objects = InteractionManager()


class BlockManager(models.Manager):
    def block(self, blocker, blocked):
        "Creates block"
        block = self.create(blocker=blocker, blocked=blocked)
        block.save()
        return block

    def exists_block(self, user_1, user_2):
        "Returns true if there exists a block in either direction between given users"
        return self.filter(
            models.Q(blocker=user_1, blocked=user_2)
            | models.Q(blocker=user_2, blocked=user_1)
        ).exists()


class Block(models.Model):
    blocker = models.ForeignKey(User, related_name="blocker", on_delete=models.CASCADE)
    blocked = models.ForeignKey(User, related_name="blocked", on_delete=models.CASCADE)
    objects = BlockManager()
