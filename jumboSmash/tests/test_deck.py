from django.test import TestCase
from swipe.models import Interaction, Deck, Swipable

# from rest_framework.test import force_authenticate, APIRequestFactory
from users.models import CustomUser as User


class DeckTests(TestCase):
    fixtures = ["tests/large_test_users.json"]

    #############################################
    ###         TESTS: REFRESH DECK           ###
    #############################################

    def test_first_build(self):
        "Constructing the Swipable.objects for the first time"
        active = User.objects.get(pk=1)
        Swipable.objects.build(active)

        self.assertEqual(Swipable.objects.get(should_see=2).should_see.id, 2)
        self.assertEqual(Swipable.objects.get(should_see=3).should_see.id, 3)

        # I shouldn't show up in my own Swipable.objects
        with self.assertRaises(Swipable.DoesNotExist):
            _ = Swipable.objects.get(should_see=1)

    def test_unsee_refresh(self):
        "Rebuilding the Swipable.objects after refresh - no smashes"
        active = User.objects.get(pk=1)
        Swipable.objects.build(active)

        user_2 = Swipable.objects.get(should_see=2)
        user_2.seen = True
        user_2.save()
        self.assertTrue(Swipable.objects.get(should_see=2).seen)

        Swipable.objects.build(active)
        self.assertFalse(Swipable.objects.get(should_see=2).seen)

    def test_smash_then_refresh(self):
        "Refreshing the Swipable.objects after smashing"
        active = User.objects.get(pk=1)
        Swipable.objects.build(active)
        self.assertEqual(Swipable.objects.get(should_see=3).should_see.id, 3)

        user_3 = Swipable.objects.get(should_see=3)
        user_3.seen = True
        user_3.save()

        _ = Interaction.objects.smash(active, User.objects.get(id=user_3.should_see.id))

        Swipable.objects.build(active)
        self.assertTrue(Swipable.objects.get(should_see=3).seen)

    #############################################
    ###       TESTS: GET USERS TO SWIPE       ###
    #############################################

    def test_get_next(self):
        "Get next should return 10 users, never return same users"
        active = User.objects.get(pk=1)
        Swipable.objects.build(active)
        can_swipe = Swipable.objects.get_next(active)
        self.assertEqual(len(can_swipe), 10)

        # confirm I never get users I've seen already
        already_seen = can_swipe
        while can_swipe:
            can_swipe = Swipable.objects.get_next(active)
            self.assertFalse(any(card for card in can_swipe if card in already_seen))
            map(lambda u: already_seen.append(u), can_swipe)

    # TODO: add tests that check banning/blocking/etc
