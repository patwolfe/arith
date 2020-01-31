from django.test import TestCase
from swipe.models import Interaction, Deck, Swipable

# from rest_framework.test import force_authenticate, APIRequestFactory
from users.models import CustomUser as User


class DeckTests(TestCase):
    fixtures = ["tests/dummy_users.json"]

    #############################################
    ###         TESTS: REFRESH DECK           ###
    #############################################

    def test_first_build(self):
        "Constructing the Swipable.objects for the first time"
        active = User.objects.get(pk=1)
        Swipable.objects.build(active)

        self.assertEqual(Swipable.objects.get(should_see=2).should_see.id, 2)
        self.assertEqual(Swipable.objects.get(should_see=3).should_see.id, 3)
        self.assertEqual(len(list(Swipable.objects.filter(active_user=active))), 2)

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
        "Initial boring test for get_next"
        active = User.objects.get(pk=1)
        Swipable.objects.build(active)
        can_swipe = Swipable.objects.get_next(active)
        self.assertEqual(len(can_swipe), 2)
