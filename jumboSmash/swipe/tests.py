from django.test import TestCase
from swipe.models import Interaction
from rest_framework.test import force_authenticate, APIRequestFactory
from users.models import CustomUser as User


class InteractionManagerTests(TestCase):
    fixtures = ["users/dummy_data.json"]

    def test_smash(self):
        swiper = User.objects.get(pk=1)
        swipe_target = User.objects.get(pk=2)
        interaction = Interaction.objects.smash(swiper, swipe_target)

        self.assertEqual(interaction.swiper.id, 1)
        self.assertEqual(interaction.swipe_target.id, 2)

        self.assertEqual(interaction.skip_count, 0)
        self.assertEqual(interaction.choice, Interaction.SwipeType.SMASH)

    def test_skip(self):
        swiper = User.objects.get(pk=1)
        swipe_target = User.objects.get(pk=2)
        interaction = Interaction.objects.skip(swiper, swipe_target)

        self.assertEqual(interaction.swiper.id, 1)
        self.assertEqual(interaction.swipe_target.id, 2)

        self.assertEqual(interaction.skip_count, 1)
        self.assertEqual(interaction.choice, Interaction.SwipeType.SKIP)

    def test_skip_then_smash(self):
        swiper = User.objects.get(pk=1)
        swipe_target = User.objects.get(pk=2)
        _ = Interaction.objects.skip(swiper, swipe_target)
        interaction = Interaction.objects.smash(swiper, swipe_target)

        self.assertEqual(interaction.swiper.id, 1)
        self.assertEqual(interaction.swipe_target.id, 2)

        self.assertEqual(interaction.skip_count, 1)
        self.assertEqual(interaction.choice, Interaction.SwipeType.SMASH)

    def test_smash_then_skip(self):
        swiper = User.objects.get(pk=1)
        swipe_target = User.objects.get(pk=2)
        _ = Interaction.objects.smash(swiper, swipe_target)
        interaction = Interaction.objects.skip(swiper, swipe_target)

        self.assertEqual(interaction.swiper.id, 1)
        self.assertEqual(interaction.swipe_target.id, 2)

        self.assertEqual(interaction.skip_count, 0)
        self.assertEqual(interaction.choice, Interaction.SwipeType.SMASH)
