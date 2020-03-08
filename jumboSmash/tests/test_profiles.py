from django.test import TestCase
from rest_framework.test import force_authenticate, APIRequestFactory
from users.models import User, Profile
from users.serializers import ProfileSerializer
from unittest.mock import patch


def makeProfileJSON(user, list, bio="hello", approved=False):
    data = {"approved": approved, "user": user, "bio": bio}
    for i in range(0, 6):
        data["photo" + str(i)] = list[i]
    return data


@patch("users.models.delete_photos")
class ProfileSerializerTests(TestCase):
    fixtures = ["tests/dummy_users.json", "tests/dummy_profiles.json"]

    def test_valid_profile_serialization(self, mock_delete):
        """ JSON passes validation"""
        serializer = ProfileSerializer(
            data=makeProfileJSON(1, [0, 1, 2, None, None, None])
        )
        self.assertTrue(serializer.is_valid())

    def test_photo_after_null(self, mock_delete):
        """ Photo after 'None' fails """
        serializer = ProfileSerializer(
            data=makeProfileJSON(1, [0, 1, None, 6, None, None])
        )
        self.assertFalse(serializer.is_valid())

    def test_too_few_photos(self, mock_delete):
        """ Too few photos raises validation error"""
        order = [3, 1, None, None, None, None]
        serializer = ProfileSerializer(data=makeProfileJSON(1, order))
        self.assertFalse(serializer.is_valid())

    def test_reorder_creation(self, mock_delete):
        """ Reorderings alter existing approved profile """
        user = User.objects.get(pk=1)
        order = [3, 1, 2, None, None, None]
        serializer = ProfileSerializer(
            data=makeProfileJSON(1, order), context={"user": user}
        )
        self.assertTrue(serializer.is_valid())
        serializer.save()
        approved, pending = Profile.objects.get_profiles(user=user)
        self.assertEqual(approved.photo_list(), order)
        self.assertIsNone(pending)

    def test_reorder_creation_bio_change(self, mock_delete):
        """ Bio changes creates pending profile """
        user = User.objects.get(pk=1)
        old_approved, old_pending = Profile.objects.get_profiles(user=user)

        order = [3, 1, 2, None, None, None]
        serializer = ProfileSerializer(
            data=makeProfileJSON(1, order, bio="sup"), context={"user": user}
        )
        self.assertTrue(serializer.is_valid())
        serializer.save()
        approved, pending = Profile.objects.get_profiles(user=user)
        self.assertEqual(pending.photo_list(), order)
        self.assertEqual(pending.bio, "sup")
        self.assertEqual(old_approved, approved)

    def test_new_photo_creation(self, mock_delete):
        """ Introduction of a new photo_id creates pending profile, does not alter existing one"""
        user = User.objects.get(pk=1)
        old_approved, old_pending = Profile.objects.get_profiles(user=user)

        order = [3, 1, 2, 5, None, None]
        serializer = ProfileSerializer(
            data=makeProfileJSON(1, order), context={"user": user}
        )
        self.assertTrue(serializer.is_valid())
        serializer.save()
        approved, pending = Profile.objects.get_profiles(user=user)
        self.assertEqual(pending.photo_list(), order)
        self.assertEqual(old_approved, approved)

    def test_secondary_edit(self, mock_delete):
        """ Secondary changes edit existing pending profile"""
        user = User.objects.get(pk=2)
        old_approved, old_pending = Profile.objects.get_profiles(user=user)

        order = [3, 1, 2, 5, None, None]
        serializer = ProfileSerializer(
            data=makeProfileJSON(2, order), context={"user": user}
        )
        self.assertTrue(serializer.is_valid())
        serializer.save()
        approved, pending = Profile.objects.get_profiles(user=user)
        self.assertEqual(pending.photo_list(), order)
        self.assertEqual(old_approved, approved)

    def test_photo_repeats(self, mock_delete):
        """ Photo repeats are not allowed """
        user = User.objects.get(pk=1)
        old_approved, old_pending = Profile.objects.get_profiles(user=user)

        order = [3, 1, 2, 5, 5, None]
        serializer = ProfileSerializer(
            data=makeProfileJSON(1, order), context={"user": user}
        )
        self.assertFalse(serializer.is_valid())


class ModelViewsTest(TestCase):
    fixtures = ["tests/dummy_users.json", "tests/dummy_profiles.json"]
    factory = APIRequestFactory()

    def test_get_own_profile_pending(self):
        """ User gets their own pending profile if it exists """
        pass

    def test_get_own_profile_approved(self):
        """ User gets their own approved profile if nothing is pending """
        pass

    def test_get_other_profile_approved(self):
        """ User can see other's approved profiles """
        pass

    def test_get_other_profile_dne(self):
        """ User cannot see other's pending profiles, 404"""
        pass
