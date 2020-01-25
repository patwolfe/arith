from django.test import TestCase
from chat.models import Match
from rest_framework.test import force_authenticate, APIRequestFactory
from users.models import CustomUser as User
from chat.views import Unmatch


class ModelManagerTests(TestCase):
    fixtures = ["tests/dummy_users.json"]

    def test_make_match_valid(self):
        """ Matches valid users """
        match = Match.objects.create_match(1, 2)

        self.assertEqual(match.user_1.id, 1)
        self.assertEqual(match.user_2.id, 2)

        self.assertFalse(match.top5)
        self.assertFalse(match.unmatched)

    def test_make_match_invalid_user(self):
        """ Attempts to match non-existant user """
        with self.assertRaises(Exception):
            match = Match.objects.create_match(1, 5)

    def test_unmatch_valid(self):
        """ Unmatches valid match """

        match = Match.objects.create_match(1, 2)
        unmatch = Match.objects.unmatch(match)

        self.assertEqual(unmatch.user_1.id, 1)
        self.assertEqual(unmatch.user_2.id, 2)

        self.assertFalse(unmatch.top5)
        self.assertTrue(unmatch.unmatched)

    def test_list(self):
        """ Confirms list_matches returns all matches for a user """
        _ = Match.objects.create_match(1, 2)
        _ = Match.objects.create_match(3, 1)
        _ = Match.objects.create_match(3, 2)

        matches = list(Match.objects.list_matches(1))

        self.assertEqual(len(matches), 2)

        self.assertEqual(matches[0].id, 1)

        self.assertEqual(matches[1].id, 2)


class ModelViewsTest(TestCase):
    fixtures = ["tests/dummy_users.json"]

    def test_unmatch_valid_1(self):
        """ Confirms user_1 can unmatch match """
        _ = Match.objects.create_match(1, 2)
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
        _ = Match.objects.create_match(1, 2)
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
        _ = Match.objects.create_match(1, 2)
        user = User.objects.get(pk=3)

        factory = APIRequestFactory()
        request = factory.post("/unmatch/", {"match": 1}, format="json")
        force_authenticate(request, user=user)
        view = Unmatch.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 403)

        match = Match.objects.get(pk=1)
        self.assertFalse(match.unmatched)
