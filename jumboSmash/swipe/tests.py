from django.test import TestCase
from swipe.models import Interaction
from rest_framework.test import force_authenticate, APIRequestFactory
from users.models import CustomUser as User
from matches.models import Match


class InteractionManagerTests(TestCase):
    fixtures = ["users/dummy_data.json"]

    def test_smash(self):
        """ Smashing """
        swiper = User.objects.get(pk=1)
        swiped_on = User.objects.get(pk=2)
        interaction = Interaction.objects.smash(swiper, swiped_on)

        self.assertEqual(interaction.swiper.id, 1)
        self.assertEqual(interaction.swiped_on.id, 2)

        self.assertEqual(interaction.skip_count, 0)
        self.assertTrue(interaction.smash)

    def test_skip(self):
        """ Skipping """
        swiper = User.objects.get(pk=1)
        swiped_on = User.objects.get(pk=2)
        interaction = Interaction.objects.skip(swiper, swiped_on)

        self.assertEqual(interaction.swiper.id, 1)
        self.assertEqual(interaction.swiped_on.id, 2)

        self.assertEqual(interaction.skip_count, 1)
        self.assertFalse(interaction.smash)

    def test_skip_then_smash(self):
        """ Smashing after a skip """
        swiper = User.objects.get(pk=1)
        swiped_on = User.objects.get(pk=2)
        _ = Interaction.objects.skip(swiper, swiped_on)
        interaction = Interaction.objects.smash(swiper, swiped_on)

        self.assertEqual(interaction.swiper.id, 1)
        self.assertEqual(interaction.swiped_on.id, 2)

        self.assertEqual(interaction.skip_count, 1)
        self.assertTrue(interaction.smash)

    def test_smash_then_skip(self):
        """ Smashing then skipping should not change interaction """
        swiper = User.objects.get(pk=1)
        swiped_on = User.objects.get(pk=2)
        _ = Interaction.objects.smash(swiper, swiped_on)
        interaction = Interaction.objects.skip(swiper, swiped_on)

        self.assertEqual(interaction.swiper.id, 1)
        self.assertEqual(interaction.swiped_on.id, 2)

        self.assertEqual(interaction.skip_count, 0)
        self.assertTrue(interaction.smash)

    def test_match_creation(self):
        """ A match is created by complementary smash swipes """
        swiper = User.objects.get(pk=1)
        swiped_on = User.objects.get(pk=2)
        _ = Interaction.objects.smash(swiper, swiped_on)
        _ = Interaction.objects.smash(swiped_on, swiper)
        # ideally this should probably be a mock not an actual call
        self.assertEqual(len(list(Match.objects.list_matches(swiper.id))), 1)

    def test_no_match_creation(self):
        """ A match is not created with smash + skip swipes"""
        swiper = User.objects.get(pk=1)
        swiped_on = User.objects.get(pk=2)
        _ = Interaction.objects.smash(swiper, swiped_on)
        _ = Interaction.objects.skip(swiped_on, swiper)

        self.assertEqual(len(list(Match.objects.list_matches(swiper.id))), 0)
