from django.utils import timezone
from django.test import TestCase
from chat.models import Match
from chat.serializers import MatchIdSerializer
from rest_framework.test import force_authenticate, APIRequestFactory
from users.models import User
from chat.views import Unmatch


def makeMatchJSON(user1, user2, unmatched=False):
    return {"user_1": user1, "user_2": user2, "unmatched": unmatched, "top5": False,
            "user_1_viewed": False, "user_2_viewed": False, "last_active": timezone.now()}


class ModelManagerTests(TestCase):
    fixtures = ["tests/dummy_users.json"]

    def test_make_match_valid(self):
        """ Matches valid users """
        user_1 = User.objects.get(pk=1)
        user_2 = User.objects.get(pk=2)
        match = Match.objects.create_match(user_1, user_2)

        self.assertEqual(match.user_1.id, 1)
        self.assertEqual(match.user_2.id, 2)

        self.assertFalse(match.top5)
        self.assertFalse(match.unmatched)
        self.assertFalse(match.user_1_viewed)
        self.assertFalse(match.user_2_viewed)

    def test_make_match_invalid(self):
        """ Attempt to double-create a match """
        user_1 = User.objects.get(pk=1)
        user_2 = User.objects.get(pk=2)
        match = Match.objects.create_match(user_1, user_2)

        with self.assertRaises(Exception):
            match = Match.objects.create_match(user_2, user_1)

    def test_unmatch_valid(self):
        """ Unmatches valid match """
        user_1 = User.objects.get(pk=1)
        user_2 = User.objects.get(pk=2)

        match = Match.objects.create_match(user_1, user_2)
        match.unmatch()

        self.assertEqual(match.user_1.id, 1)
        self.assertEqual(match.user_2.id, 2)

        self.assertFalse(match.top5)
        self.assertTrue(match.unmatched)

    def test_list(self):
        """ Confirms list_matches returns all matches for a user """
        user_1 = User.objects.get(pk=1)
        user_2 = User.objects.get(pk=2)
        user_3 = User.objects.get(pk=3)
        _ = Match.objects.create_match(user_1, user_2)
        _ = Match.objects.create_match(user_3, user_1)
        _ = Match.objects.create_match(user_3, user_2)

        matches = Match.objects.list_matches(user_1)

        self.assertEqual(len(matches), 2)

        # Confirm matches are the ones we expect
        matches.get(user_2=2)
        matches.get(user_2=3)

    def test_list_unmatch(self):
        """ Confirms list_matches does not return unmatched matches"""
        user_1 = User.objects.get(pk=1)
        user_2 = User.objects.get(pk=2)
        user_3 = User.objects.get(pk=3)
        _ = Match.objects.create_match(user_1, user_2)
        to_unmatch = Match.objects.create_match(user_3, user_1)
        _ = Match.objects.create_match(user_3, user_2)
        to_unmatch.unmatch()

        matches = Match.objects.list_matches(user_1)

        self.assertEqual(len(matches), 1)

        # Confirm matches are the ones we expect
        matches.get(user_2=2)

    def test_top5(self):
        """ Confirms create_top5_match makes a top5 match """
        user_1 = User.objects.get(pk=1)
        user_2 = User.objects.get(pk=2)
        match = Match.objects.create_top5_match(user_1, user_2)
        self.assertTrue(match.top5)


class ModelManagerDummyMatches(TestCase):
    fixtures = ["tests/dummy_users.json", "tests/dummy_matches.json"]

    def test_mark_other_unviewed_second_user(self):
        match = Match.objects.get(pk=2)
        user_1_viewed = match.user_1_viewed

        match.mark_other_unviewed(match.user_1)
        self.assertEqual(match.user_1_viewed, user_1_viewed)
        self.assertFalse(match.user_2_viewed)

    def test_mark_other_unviewed_first_user(self):
        match = Match.objects.get(pk=2)
        user_2_viewed = match.user_2_viewed

        match.mark_other_unviewed(match.user_2)
        self.assertEqual(match.user_2_viewed, user_2_viewed)
        self.assertFalse(match.user_1_viewed)

    def test_mark_viewed_first_user(self):
        match = Match.objects.get(pk=1)
        user_2_viewed = match.user_2_viewed

        match.mark_viewed(match.user_1)
        self.assertTrue(match.user_1_viewed)
        self.assertEqual(user_2_viewed, match.user_2_viewed)

    def test_mark_viewed_second_user(self):
        match = Match.objects.get(pk=1)
        user_1_viewed = match.user_1_viewed

        match.mark_viewed(match.user_2)
        self.assertTrue(match.user_2_viewed)
        self.assertEqual(user_1_viewed, match.user_1_viewed)

    def test_update_last_active(self):
        match = Match.objects.get(pk=1)
        last_active = match.last_active

        match.update_last_active()
        self.assertNotEqual(last_active, match.last_active)


class MatchIDSerializerTest(TestCase):
    fixtures = ["tests/dummy_users.json", "tests/dummy_matches.json"]

    def test_serializer_user_not_in_match(self):
        user = User.objects.get(pk=3)
        serializer = MatchIdSerializer(data={"match": 1}, context={"user": user})
        self.assertFalse(serializer.is_valid())

    def test_serializer_unmatched_match(self):
        user = User.objects.get(pk=2)
        serializer = MatchIdSerializer(data={"match": 2}, context={"user": user})
        self.assertFalse(serializer.is_valid())

    def test_serializer_bad_data(self):
        user = User.objects.get(pk=1)
        serializer = MatchIdSerializer(data={}, context={"user": user})
        self.assertFalse(serializer.is_valid())

    def test_serializer_valid_data(self):
        user = User.objects.get(pk=1)
        serializer = MatchIdSerializer(data={"match": 1}, context={"user": user})
        self.assertTrue(serializer.is_valid())


class ModelViewsTest(TestCase):
    fixtures = ["tests/dummy_users.json", "tests/dummy_matches.json"]
    factory = APIRequestFactory()

    def test_unmatch_valid_1(self):
        """ Confirms user_1 can unmatch match """
        user = User.objects.get(pk=1)

        request = self.factory.post("chat/unmatch/", {"match": 1}, format="json")
        force_authenticate(request, user=user)
        view = Unmatch.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 201)

        match = Match.objects.get(pk=1)
        self.assertTrue(match.unmatched)

    def test_unmatch_valid_2(self):
        """ Confirms user_2 can unmatch match """
        user = User.objects.get(pk=2)

        request = self.factory.post("chat/unmatch/", {"match": 1}, format="json")
        force_authenticate(request, user=user)
        view = Unmatch.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 201)

        match = Match.objects.get(pk=1)
        self.assertTrue(match.unmatched)

    def test_unmatch_invalid_user(self):
        """ User not in match cannot unmatch """
        user = User.objects.get(pk=3)

        request = self.factory.post("chat/unmatch/", {"match": 1}, format="json")
        force_authenticate(request, user=user)
        view = Unmatch.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 400)

        match = Match.objects.get(pk=1)
        self.assertFalse(match.unmatched)
