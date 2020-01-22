from django.test import TestCase
from matches.models import Match
from matches.views import Unmatch
from rest_framework.test import force_authenticate, APIRequestFactory
from users.models import CustomUser as User


class ModelManagerTests(TestCase):
    fixtures = ["users/dummy_data.json"]

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
        match = Match.objects.unmatch(match.pk)

        self.assertEqual(match.user_1.id, 1)
        self.assertEqual(match.user_2.id, 2)

        self.assertFalse(match.top5)
        self.assertTrue(match.unmatched)

    def test_unmatch_invalid(self):
        """ Attempts to unmatch non-existant match """
        with self.assertRaises(Match.DoesNotExist):
            match = Match.objects.unmatch(1)

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
    fixtures = ["users/dummy_data.json"]

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

        self.assertEqual(response.status_code, 401)

        match = Match.objects.get(pk=1)
        self.assertFalse(match.unmatched)
