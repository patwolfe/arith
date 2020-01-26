from django.test import TestCase
from chat.models import Match
from rest_framework.test import force_authenticate, APIRequestFactory
from users.models import CustomUser as User


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
