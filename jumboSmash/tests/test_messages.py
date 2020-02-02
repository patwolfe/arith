from django.test import TestCase
from users.models import User
from chat.models import Message, Match


class MessageManagerTest(TestCase):
    fixtures = ["tests/dummy_users.json", "tests/dummy_matches.json", "tests/dummy_messages.json"]

    def test_create_message(self):
        match = Match.objects.get(pk=1)
        user = User.objects.get(pk=1)
        message = Message.objects.create_message(match, user, "u up?")

        self.assertEqual(message.match.id, 1)
        self.assertEqual(message.sender.id, 1)
        self.assertEqual(message.content, "u up?")

    def test_list_message(self):
        match = Match.objects.get(pk=1)
        list_m = Message.objects.list_messages(match)

        self.assertEqual(len(list_m), 2)
        self.assertEqual(list_m[0].match.id, 1)
        self.assertEqual(list_m[1].match.id, 1)

        #assert delivered by order it is sent
        self.assertEqual(list_m[0].id, 1)
        self.assertEqual(list_m[1].id, 2)

