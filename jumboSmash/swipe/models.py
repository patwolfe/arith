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


class Deck(models.Manager):
    def build(self, curr_user):
        "(re)Builds the deck for the active user"
        # TODO: exclude inactive users here
        all_users = User.objects.exclude(id__exact=curr_user.id).values("id")
        already_smashed = Interaction.objects.filter(
            swiper__exact=curr_user, smash__exact=True
        ).values("swiped_on")

        deck = all_users.difference(already_smashed)
        for swipable in deck:
            deck_entry, _ = self.get_or_create(
                active_user=curr_user, should_see=User.objects.get(id=swipable["id"])
            )
            deck_entry.seen = False
            deck_entry.save()

    def get_next(self, curr_user):
        "Returns a list of the next 10 users curr_user hasn't seen"
        next_cards = []
        swipable = self.all().filter(active_user=curr_user, seen=False)
        index = 0
        while len(next_cards) < 10 and index < len(swipable):
            if swipable[index].swipe_allowed():
                next_cards.append(swipable[index].should_see)
                swipable[index].seen = True
                swipable[index].save()
            index += 1
        return next_cards


class Swipable(models.Model):
    active_user = models.ForeignKey(
        User, related_name="active_user", on_delete=models.CASCADE
    )
    should_see = models.ForeignKey(
        User, related_name="should_see", on_delete=models.CASCADE
    )
    seen = models.BooleanField(default=False)

    objects = Deck()

    # TODO: check blocked/banned tables
    def swipe_allowed(self):
        return True
