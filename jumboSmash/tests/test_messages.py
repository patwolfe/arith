from django.test import TestCase
from chat.models import Message


class MessageManagerTest(TestCase):
    fixtures = ["tests/dummy_users.json", "tests/dummy_matches.json"]

    def test_create_message_valid(self):
        message = Message.objects.create_message(1, 1, "u up?")

        self.assertEqual(message.match.id, 1)
        self.assertEqual(message.sender.id, 1)

        self.assertEqual(message.content, "u up?")
