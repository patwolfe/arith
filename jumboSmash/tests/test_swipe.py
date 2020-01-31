from django.test import TestCase
from swipe.models import Interaction
from rest_framework.test import force_authenticate, APIRequestFactory
from users.models import CustomUser as User
from chat.models import Match
from swipe.views import Smash, Skip, Top5


class InteractionManagerTests(TestCase):
    fixtures = ["tests/dummy_users.json"]

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

        with self.assertRaises(Exception):
            Interaction.objects.skip(swiper, swiped_on)

        interaction = Interaction.objects.get(swiper=swiper, swiped_on=swiped_on)

        self.assertEqual(interaction.skip_count, 0)
        self.assertTrue(interaction.smash)

    def test_smash_then_smash(self):
        """ Double smashing should trigger assertion """
        swiper = User.objects.get(pk=1)
        swiped_on = User.objects.get(pk=2)
        _ = Interaction.objects.smash(swiper, swiped_on)

        with self.assertRaises(Exception):
            Interaction.objects.smash(swiper, swiped_on)

        interaction = Interaction.objects.get(swiper=swiper, swiped_on=swiped_on)

        self.assertEqual(interaction.skip_count, 0)
        self.assertTrue(interaction.smash)

    def test_match_creation(self):
        """ A match is created by complementary smash swipes """
        swiper = User.objects.get(pk=1)
        swiped_on = User.objects.get(pk=2)
        _ = Interaction.objects.smash(swiper, swiped_on)
        _ = Interaction.objects.smash(swiped_on, swiper)
        # ideally this should probably be a mock not an actual call
        self.assertEqual(len(list(Match.objects.list_matches(swiper))), 1)

    def test_no_match_creation(self):
        """ A match is not created with smash + skip swipes"""
        swiper = User.objects.get(pk=1)
        swiped_on = User.objects.get(pk=2)
        _ = Interaction.objects.smash(swiper, swiped_on)
        _ = Interaction.objects.skip(swiped_on, swiper)

        self.assertEqual(len(list(Match.objects.list_matches(swiper))), 0)

    def test_top5_swipe(self):
        """ Top5 'swipe' """
        swiper = User.objects.get(pk=1)
        swiped_on = User.objects.get(pk=2)
        interaction = Interaction.objects.top5(swiper, swiped_on)

        self.assertTrue(interaction.top5)
        self.assertFalse(interaction.smash)

    def test_top5_swipe_invalid(self):
        """ Top5 cannot be applied to existing interaction """
        swiper = User.objects.get(pk=1)
        swiped_on = User.objects.get(pk=2)
        _ = Interaction.objects.smash(swiper, swiped_on)
        with self.assertRaises(Exception):
            _ = Interaction.objects.top5(swiper, swiped_on)

    def test_top5_match(self):
        """ Matching top5 swipes create match, mark both interactions smash"""
        swiper = User.objects.get(pk=1)
        swiped_on = User.objects.get(pk=2)
        _ = Interaction.objects.top5(swiper, swiped_on)
        interaction = Interaction.objects.top5(swiped_on, swiper)
        complement = Interaction.objects.get(swiper=swiper, swiped_on=swiped_on)

        self.assertTrue(interaction.top5)
        self.assertTrue(interaction.smash)

        self.assertTrue(complement.top5)
        self.assertTrue(complement.smash)

        matches = list(Match.objects.list_matches(swiper))

        self.assertEqual(len(matches), 1)
        self.assertTrue(matches[0].top5)


class InteractionsViewsTest(TestCase):
    fixtures = ["tests/dummy_users.json"]

    def test_smash_valid(self):
        """ Smash endpoint creates smash interaction """
        user = User.objects.get(pk=1)

        factory = APIRequestFactory()
        request = factory.post("swipe/smash/", {"user": 2}, format="json")
        force_authenticate(request, user=user)
        view = Smash.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 201)

        smash = Interaction.objects.get(swiper=user, swiped_on=2)
        self.assertTrue(smash.smash)

    def test_skip_valid(self):
        """ Skip endpoint creates skip interaction """
        user = User.objects.get(pk=1)

        factory = APIRequestFactory()
        request = factory.post("swipe/skip/", {"user": 2}, format="json")
        force_authenticate(request, user=user)
        view = Skip.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 201)

        smash = Interaction.objects.get(swiper=user, swiped_on=2)
        self.assertFalse(smash.smash)

    def test_top5_valid(self):
        """ Top5 endpoint creates top5 interaction """
        user = User.objects.get(pk=1)

        factory = APIRequestFactory()
        request = factory.post("swipe/top5/", [{"user": 2}, {"user": 3}], format="json")
        force_authenticate(request, user=user)
        view = Top5.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 201)

        Interaction.objects.get(swiper=user, swiped_on=2, top5=True)
        Interaction.objects.get(swiper=user, swiped_on=3, top5=True)

    def test_top5_too_many(self):
        """ Top5 endpoint rejects lists of more than 5 users """
        user = User.objects.get(pk=1)

        factory = APIRequestFactory()
        request = factory.post(
            "swipe/top5/",
            [
                {"user": 2},
                {"user": 3},
                {"user": 3},
                {"user": 3},
                {"user": 3},
                {"user": 3},
            ],
            format="json",
        )
        force_authenticate(request, user=user)
        view = Top5.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 400)

    def test_top5_repeats(self):
        """ Top5 endpoint ignores repeats"""
        user = User.objects.get(pk=1)

        factory = APIRequestFactory()
        request = factory.post(
            "swipe/top5/", [{"user": 2}, {"user": 2}], format="json",
        )
        force_authenticate(request, user=user)
        view = Top5.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)

        Interaction.objects.get(swiper=user, swiped_on=2, top5=True)

    def test_top5_multiple_requests(self):
        """ Users can only submit one set of top5 requests """
        user = User.objects.get(pk=1)

        factory = APIRequestFactory()
        request = factory.post("swipe/top5/", [{"user": 2}], format="json")
        force_authenticate(request, user=user)
        view = Top5.as_view()
        response = view(request)

        request_2 = factory.post("swipe/top5/", [{"user": 3}], format="json")
        force_authenticate(request_2, user=user)
        response_2 = view(request_2)

        self.assertEqual(response_2.status_code, 400)

        Interaction.objects.get(swiper=user, swiped_on=2, top5=True)
        with self.assertRaises(Exception):
            Interaction.objects.get(swiper=user, swiped_on=3, top5=True)
