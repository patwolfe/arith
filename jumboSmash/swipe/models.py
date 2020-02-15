from django.db import models
from users.models import User
from chat.models import Match
import random


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
                    Match.objects.create_match(swiper, swiped_on)
            except:
                pass
        else:
            assert 0, "Interaction already marked 'smash', cannot 'smash' again"

        return interaction

    def top5(self, swiper, swiped_on):
        """ Records a top5 """
        interaction, created = self.get_or_create(swiper=swiper, swiped_on=swiped_on)
        if created:
            interaction.top5 = True
            interaction.save()
            try:
                complement = self.get(swiper=swiped_on, swiped_on=swiper)
                if complement.top5:
                    interaction.smash = True
                    interaction.save()
                    complement.smash = True
                    complement.save()
                    Match.objects.create_top5_match(swiper, swiped_on)
            except Interaction.DoesNotExist:
                pass
            except Exception as e:
                print(e)
        else:
            assert 0, "Cannot top5 an existing interaction"

        return interaction

    def build_deck(self, active_user):
        "Create all interactions for current user and mark smash=NULL"
        all_users = (
            User.objects.exclude(id__exact=active_user.id)
            .filter(status__exact=User.ACTIVE)
            .values("pk")
        )
        already_smashed = self.filter(
            swiper__exact=active_user, smash__exact=True
        ).values("swiped_on")

        deck = all_users.difference(already_smashed)
        for other in deck:
            interaction, _ = self.get_or_create(
                swiper=active_user, swiped_on=User.objects.get(pk=other["pk"])
            )
            interaction.smash = None
            interaction.save()

    def pull_new_users(self, active_user):
        "Add newly registered users to the deck, returns True if any new users were added"
        new_users = (
            User.objects.filter(status__exact=User.ACTIVE)
            .exclude(pk=active_user.pk)
            .values("pk")
            .difference(self.filter(swiper__exact=active_user).values("swiped_on"))
        )
        for newbie in new_users:
            interaction, _ = self.get_or_create(
                swiper=active_user, swiped_on=User.objects.get(pk=newbie["pk"])
            )
            interaction.smash = None
            interaction.save()
        # return True if there were new users added to the Deck
        return new_users.exists()

    def get_next(self, active_user):
        "Retrieve 10 users to swipe on"
        deck = list(self.filter(swiper__exact=active_user, smash__exact=None))
        next = []
        count = 0
        while len(next) < 10 and count < len(deck):
            try:
                rand_index = random.randint(1, len(deck) - 1)
            except:
                rand_index = 0
            if deck[rand_index].swipable() and deck[rand_index] not in next:
                next.append(deck[rand_index])
            count += 1
        # When we run out of users, check for newly active users
        # - if the list was empty, try again with new users added
        if len(next) == 0 and self.pull_new_users(active_user):
            return self.get_next(active_user)
        return next


class Interaction(models.Model):
    swiper = models.ForeignKey(User, related_name="swiper", on_delete=models.CASCADE)
    swiped_on = models.ForeignKey(
        User, related_name="swiped_on", on_delete=models.CASCADE
    )
    smash = models.BooleanField(null=True)
    top5 = models.BooleanField(default=False)
    skip_count = models.PositiveIntegerField(default=0)

    objects = InteractionManager()

    def swipable(self):
        return not (
            Block.objects.exists_block(self.swiper, self.swiped_on)
            # or self.swiper.status == User.BANNED
            or self.swiped_on.status == User.BANNED
        )

    class Meta:
        unique_together = [["swiper", "swiped_on"]]


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
