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
