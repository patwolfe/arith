from django.test import TestCase
from matches.models import Match


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
