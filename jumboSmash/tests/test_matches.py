from django.test import TestCase
from chat.models import Match
from rest_framework.test import force_authenticate, APIRequestFactory
from users.models import CustomUser as User
from chat.views import Unmatch


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

    def test_unmatch_valid(self):
        """ Unmatches valid match """
        user_1 = User.objects.get(pk=1)
        user_2 = User.objects.get(pk=2)

        match = Match.objects.create_match(user_1, user_2)
        unmatch = Match.objects.unmatch(match)

        self.assertEqual(unmatch.user_1.id, 1)
        self.assertEqual(unmatch.user_2.id, 2)

        self.assertFalse(unmatch.top5)
        self.assertTrue(unmatch.unmatched)

    def test_list(self):
        """ Confirms list_matches returns all matches for a user """
        user_1 = User.objects.get(pk=1)
        user_2 = User.objects.get(pk=2)
        user_3 = User.objects.get(pk=3)
        _ = Match.objects.create_match(user_1, user_2)
        _ = Match.objects.create_match(user_3, user_1)
        _ = Match.objects.create_match(user_3, user_2)

        matches = Match.objects.list_matches(1)

        self.assertEqual(len(matches), 2)

        # Confirm matches are the ones we expect
        matches.get(user_2=2)
        matches.get(user_1=3)

    def test_list_unmatch(self):
        """ Confirms list_matches does not return unmatched matches"""
        user_1 = User.objects.get(pk=1)
        user_2 = User.objects.get(pk=2)
        user_3 = User.objects.get(pk=3)
        _ = Match.objects.create_match(user_1, user_2)
        to_unmatch = Match.objects.create_match(user_3, user_1)
        _ = Match.objects.create_match(user_3, user_2)
        unmatched = Match.objects.unmatch(to_unmatch)

        matches = Match.objects.list_matches(1)

        self.assertEqual(len(matches), 1)

        # Confirm matches are the ones we expect
        matches.get(user_2=2)


class ModelViewsTest(TestCase):
    fixtures = ["tests/dummy_users.json", "tests/dummy_matches.json"]

    def test_unmatch_valid_1(self):
        """ Confirms user_1 can unmatch match """
        user = User.objects.get(pk=1)

        factory = APIRequestFactory()
        request = factory.post("/unmatch/", {"match": 1}, format="json")
        force_authenticate(request, user=user)
        view = Unmatch.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 200)

        match = Match.objects.get(pk=1)
        self.assertTrue(match.unmatched)

    def test_unmatch_valid_2(self):
        """ Confirms user_2 can unmatch match """
        user = User.objects.get(pk=2)

        factory = APIRequestFactory()
        request = factory.post("/unmatch/", {"match": 1}, format="json")
        force_authenticate(request, user=user)
        view = Unmatch.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 200)

        match = Match.objects.get(pk=1)
        self.assertTrue(match.unmatched)

    def test_unmatch_invalid_user(self):
        """ User not in match cannot unmatch """
        user = User.objects.get(pk=3)

        factory = APIRequestFactory()
        request = factory.post("/unmatch/", {"match": 1}, format="json")
        force_authenticate(request, user=user)
        view = Unmatch.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 403)

        match = Match.objects.get(pk=1)
        self.assertFalse(match.unmatched)
