from django.test import TestCase
from swipe.models import Interaction
from rest_framework.test import force_authenticate, APIRequestFactory
from users.models import CustomUser as User


class InteractionManagerTests(TestCase):
    fixtures = ["users/dummy_data.json"]

    def test_smash_swipe_new(self):
        swiper = User.objects.get(pk=1)
        swipee = User.objects.get(pk=2)
        interaction = Interaction.objects.smash(swiper, swipee)

        self.assertEqual(interaction.swiper.id, 1)
        self.assertEqual(interaction.swipee.id, 2)

        self.assertEqual(interaction.skip_count, 0)
        self.assertEqual(interaction.choice, Interaction.SwipeType.SMASH)

    def test_skip_swipe_new(self):
        swiper = User.objects.get(pk=1)
        swipee = User.objects.get(pk=2)
        interaction = Interaction.objects.skip(swiper, swipee)

        self.assertEqual(interaction.swiper.id, 1)
        self.assertEqual(interaction.swipee.id, 2)

        self.assertEqual(interaction.skip_count, 1)
        self.assertEqual(interaction.choice, Interaction.SwipeType.SKIP)

    def test_skip_then_smash_swipe(self):
        swiper = User.objects.get(pk=1)
        swipee = User.objects.get(pk=2)
        _ = Interaction.objects.skip(swiper, swipee)
        interaction = Interaction.objects.smash(swiper, swipee)

        self.assertEqual(interaction.swiper.id, 1)
        self.assertEqual(interaction.swipee.id, 2)

        self.assertEqual(interaction.skip_count, 1)
        self.assertEqual(interaction.choice, Interaction.SwipeType.SMASH)
