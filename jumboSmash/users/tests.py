from django.test import TestCase
from django.contrib.auth import get_user_model

class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="normal@user.com", password="123")
        self.assertEqual(user.email, "normal@user.com")
        self.assertIsNone(user.username)

        # check permissions
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(TypeError):
            User.objects.create_user()

    def test_create_staffuser(self):
        User = get_user_model()
        admin_user = User.objects.create_staffuser("super@user.com", password="123")
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertIsNone(admin_user.username)

        # check permissions
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertFalse(admin_user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser("super@user.com", password="123")
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertIsNone(admin_user.username)

        # check permissions
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class UserRetrievalTests(TestCase):
    fixtures = ['users/dummy_data.json']

    def test_email_in_db(self):
        User = get_user_model()
        email = "js2020@tufts.edu"
        user = User.objects.get(email=email)

        # check correct user retrieved
        self.assertEqual(email, user.email)
        self.assertEqual("Jumbo", user.first_name)
        self.assertEqual("Smash", user.last_name)

    def test_email_not_in_db(self):
        User = get_user_model()
        email = "not_in_db@yahoo.com"

        # check user is not in db
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(email=email)
