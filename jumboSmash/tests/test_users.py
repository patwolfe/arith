from django.test import TestCase
from users.models import User
from users.views import SetupUser
from rest_framework.test import force_authenticate, APIRequestFactory


class UsersManagersTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email="normal@user.com", first_name="normal", last_name="guy"
        )
        self.assertEqual(user.email, "normal@user.com")
        self.assertIsNone(user.username)

        # check permissions
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(TypeError):
            User.objects.create_user()

    def test_create_staffuser(self):
        admin_user = User.objects.create_staffuser(
            "super@user.com", password="123", first_name="another", last_name="person"
        )
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertIsNone(admin_user.username)

        # check permissions
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertFalse(admin_user.is_superuser)

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            "super@user.com", password="123", first_name="testing", last_name="poop"
        )
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertIsNone(admin_user.username)

        # check permissions
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class UserRetrievalTests(TestCase):
    fixtures = ["tests/dummy_users.json"]

    def test_email_in_db(self):
        email = "js2020@tufts.edu"
        user = User.objects.get(email=email)

        # check correct user retrieved
        self.assertEqual(email, user.email)
        self.assertEqual("Jumbo", user.first_name)
        self.assertEqual("Smash", user.last_name)

    def test_email_not_in_db(self):
        email = "not_in_db@yahoo.com"

        # check user is not in db
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(email=email)


class UserSetupTests(TestCase):
    fixtures = ["tests/dummy_users.json"]
    factory = APIRequestFactory()

    def test_setup(self):
        """ Inactive users can be setup """
        user = User.objects.get(pk=1)

        request = self.factory.post("user/setup/", {"name": "name"}, format="json")
        force_authenticate(request, user=user)
        view = SetupUser.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 204)

        edited_user = User.objects.get(pk=1)

        self.assertEqual(edited_user.preferred_name, "name")

    def test_active_setup(self):
        """ Active users cannot be setup """
        user = User.objects.get(pk=1)
        user.status = User.ACTIVE

        request = self.factory.post("user/setup/", {"name": "name"}, format="json")
        force_authenticate(request, user=user)
        view = SetupUser.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 409)

        unedited_user = User.objects.get(pk=1)

        self.assertIsNone(unedited_user.preferred_name)

    def test_banned_setup(self):
        """ Banned users cannot be setup """
        user = User.objects.get(pk=1)
        user.status = User.BANNED

        request = self.factory.post("user/setup/", {"name": "name"}, format="json")
        force_authenticate(request, user=user)
        view = SetupUser.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 409)

        unedited_user = User.objects.get(pk=1)

        self.assertIsNone(unedited_user.preferred_name)
