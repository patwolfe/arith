from django.test import TestCase
from rest_framework.test import force_authenticate, APIRequestFactory
from django.contrib.auth import get_user_model
from users.models import User
from users.views import UpdateToken


class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
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
        User = get_user_model()
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
        User = get_user_model()
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


class UserViewTests(TestCase):
    fixtures = ["tests/dummy_users.json"]
    factory = APIRequestFactory()

    def test_update_token_valid(self):
        user = User.objects.get(pk=1)

        request = self.factory.post("user/push_token/", {"token": '12345678910'}, format="json")
        force_authenticate(request, user=user)
        view = UpdateToken.as_view()
        response = view(request)

        updated_user = User.objects.get(pk=1)
        self.assertEqual(updated_user.push_token, '12345678910')
        self.assertEqual(response.status_code, 200)

    def test_update_token_request_not_str(self):
        user = User.objects.get(pk=1)

        request = self.factory.post("user/push_token/", {"token": 12345678910}, format="json")
        force_authenticate(request, user=user)
        view = UpdateToken.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 404)

    def test_update_token_request_empty(self):
        user = User.objects.get(pk=1)

        request = self.factory.post("user/push_token/", {}, format="json")
        force_authenticate(request, user=user)
        view = UpdateToken.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 404)