from django.test import TestCase
from rest_framework.test import force_authenticate, APIRequestFactory
from users.models import User, Profile
from users.serializers import ProfileSerializer


def makeProfileJSON(user, list, bio="hello", approved=False):
    data = {"approved": approved, "user": user, "bio": bio}
    for i in range(0, 6):
        data["photo" + str(i)] = list[i]
    return data


class ProfileSerializerTests(TestCase):
    fixtures = ["tests/dummy_users.json", "tests/dummy_profiles.json"]

    def test_valid_profile_serialization(self):
        """ JSON passes validation"""
        serializer = ProfileSerializer(
            data=makeProfileJSON(1, [0, 1, 2, None, None, None])
        )
        self.assertTrue(serializer.is_valid())

    def test_out_of_range_photo(self):
        """ Out of range photo ids fail """
        serializer = ProfileSerializer(
            data=makeProfileJSON(1, [0, 1, 17, None, None, None])
        )
        self.assertFalse(serializer.is_valid())

    def test_photo_after_null(self):
        """ Photo after 'None' fails """
        serializer = ProfileSerializer(
            data=makeProfileJSON(1, [0, 1, None, 6, None, None])
        )
        self.assertFalse(serializer.is_valid())

    def test_too_few_photos(self):
        """ Too few photos raises validation error"""
        order = [3, 1, None, None, None, None]
        serializer = ProfileSerializer(data=makeProfileJSON(1, order))
        self.assertFalse(serializer.is_valid())

    def test_reorder_creation(self):
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

    def test_reorder_creation_bio_change(self):
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

    def test_new_photo_creation(self):
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

    def test_secondary_edit(self):
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

# TODO:
# - test for deleted pending
# - test endpoints
# - test same photo id multiple times
