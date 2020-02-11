from django.test import TestCase
from rest_framework.test import force_authenticate, APIRequestFactory
from users.models import User, PhotoSet, ProfileBody
from users.serializers import PhotoSetSerializer, ProfileBodySerializer

def makePhotoSetJSON(user, list, approved=False):
    data = {"approved": approved, "user": user}
    for i in range(0, 6):
        data["photo"+str(i)] = list[i]
    return data


class PhotoSetSerializerTests(TestCase):
    fixtures = ["tests/dummy_users.json", "tests/dummy_profiles.json"]

    def test_valid_photoset_serialization(self):
        """ JSON passes validation"""
        serializer = PhotoSetSerializer(data=makePhotoSetJSON(1, [0, 1, 2, None, None, None]))
        self.assertTrue(serializer.is_valid())

    def test_out_of_range_photoset(self):
        """ Out of range photo ids fail """
        serializer = PhotoSetSerializer(data=makePhotoSetJSON(1, [0, 1, 17, None, None, None]))
        self.assertFalse(serializer.is_valid())

    def test_photo_after_null_photoset(self):
        """ Photo after 'None' fails """
        serializer = PhotoSetSerializer(data=makePhotoSetJSON(1, [0, 1, None, 6, None, None]))
        self.assertFalse(serializer.is_valid())

    def test_too_few_photos(self):
        """ Too few photos raises validation error"""
        order = [3, 1, None, None, None, None]
        serializer = PhotoSetSerializer(data=makePhotoSetJSON(1, order))
        self.assertFalse(serializer.is_valid())

    def test_reorder_creation(self):
        """ Reorderings alter existing approved photosets """
        user = User.objects.get(pk=1)
        order = [3, 1, 2, None, None, None]
        serializer = PhotoSetSerializer(data=makePhotoSetJSON(1, order), context={"user":user})
        self.assertTrue(serializer.is_valid())
        serializer.save()
        set = PhotoSet.objects.get(user=1, approved=True)
        self.assertEqual(set.as_list(), order)
        with self.assertRaises(Exception):
            PhotoSet.get(user=1, approved=False)

    def test_new_photo_creation(self):
        """ Introduction of a new photo_id creates pending photoset, does not alter existing one"""
        user = User.objects.get(pk=1)
        old_order = PhotoSet.objects.get(user=1, approved=True).as_list()
        order = [3, 1, 2, 5, None, None]
        serializer = PhotoSetSerializer(data=makePhotoSetJSON(1, order), context={"user":user})
        self.assertTrue(serializer.is_valid())
        serializer.save()
        old_set = PhotoSet.objects.get(user=1, approved=True)
        new_set = PhotoSet.objects.get(user=1, approved=False)
        self.assertEqual(new_set.as_list(), order)
        self.assertEqual(old_set.as_list(), old_order)

    def test_secondary_edit(self):
        """ Secondary changes edit existing pending photoset"""
        user = User.objects.get(pk=2)
        old_order = PhotoSet.objects.get(user=2, approved=True).as_list()
        order = [3, 1, 2, 5, None, None]
        serializer = PhotoSetSerializer(data=makePhotoSetJSON(2, order), context={"user":user})
        self.assertTrue(serializer.is_valid())
        serializer.save()
        old_set = PhotoSet.objects.get(user=2, approved=True)
        new_set = PhotoSet.objects.get(user=2, approved=False)
        self.assertEqual(new_set.as_list(), order)
        self.assertEqual(old_set.as_list(), old_order)

class ProfileBodySerializerTests(TestCase):
    fixtures = ["tests/dummy_users.json", "tests/dummy_profiles.json"]
    factory = APIRequestFactory()

    def test_bio_update(self):
        """ 'Creating' a new bio updates the previous one"""
        user = User.objects.get(pk=1)
        serializer = ProfileBodySerializer(data={"bio": "hello"}, context={"user":user})
        self.assertTrue(serializer.is_valid())
        serializer.save()
        bio = ProfileBody.objects.get(user=1)
        self.assertEqual(bio.bio, "hello")

    def test_bio_update(self):
        """ 'Creating' a new bio creates a new one if none exist """
        user = User.objects.get(pk=3)
        serializer = ProfileBodySerializer(data={"bio": "hello"}, context={"user":user})
        self.assertTrue(serializer.is_valid())
        serializer.save()
        bio = ProfileBody.objects.get(user=3)
        self.assertEqual(bio.bio, "hello")
