from django.test import TestCase
from swipe.models import Block
from swipe.views import BlockView
from rest_framework.test import force_authenticate, APIRequestFactory
from users.models import User


class BlockManagerTests(TestCase):
    fixtures = ["tests/dummy_users.json"]

    def test_block(self):
        """ block creates block between users"""
        user_1 = User.objects.get(pk=1)
        user_2 = User.objects.get(pk=2)

        _ = Block.objects.block(user_1, user_2)

        block = Block.objects.get(blocker=user_1, blocked=user_2)

    def test_block_exists(self):
        """ exists_block returns true for blocker, blocked"""
        user_1 = User.objects.get(pk=1)
        user_2 = User.objects.get(pk=2)

        _ = Block.objects.block(user_1, user_2)

        self.assertTrue(Block.objects.exists_block(user_1, user_2))

    def test_block_exists_reverse(self):
        """ exists_block returns true for blocker, blocked"""
        user_1 = User.objects.get(pk=1)
        user_2 = User.objects.get(pk=2)

        _ = Block.objects.block(user_1, user_2)

        self.assertTrue(Block.objects.exists_block(user_2, user_1))

    def test_block_exists_false(self):
        """ exists_block returns false for no block"""
        user_1 = User.objects.get(pk=1)
        user_2 = User.objects.get(pk=2)

        self.assertFalse(Block.objects.exists_block(user_1, user_2))

class BlockViewsTest(TestCase):
    fixtures = ["tests/dummy_users.json"]

    def test_block(self):
        """ User can create block through /block """
        user = User.objects.get(pk=1)

        factory = APIRequestFactory()
        request = factory.post("/block/", {"user": 2}, format="json")
        force_authenticate(request, user=user)
        view = BlockView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 200)

        self.assertTrue( Block.objects.exists_block(user, User.objects.get(pk=2)))

