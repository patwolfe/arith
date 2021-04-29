from mock import patch
from django.test import TestCase
from users.models import User
from rest_framework.test import force_authenticate, APIRequestFactory
from chat.models import Message, Match
from chat.views import SendMessage, GetConversation
from chat.tasks import message_task
from chat.serializers import MessageSerializer


class MessageManagerTest(TestCase):
    fixtures = [
        "tests/dummy_users.json",
        "tests/dummy_matches.json",
        "tests/dummy_messages.json",
    ]

    def test_create_message(self):
        match = Match.objects.get(pk=1)
        user = User.objects.get(pk=1)
        message = Message.objects.create_message(match, user, "u up?")

        self.assertEqual(message.match.id, 1)
        self.assertEqual(message.sender.id, 1)
        self.assertEqual(message.content, "u up?")

    def test_updated_delivered(self):
        message = Message.objects.get(pk=1)
        self.assertIsNone(message.delivered)
        self.assertIsNotNone(Message.objects.update_delivered(1))

    def test_list_messages(self):
        match = Match.objects.get(pk=1)
        list_m = Message.objects.list_messages(match)

        self.assertEqual(len(list_m), 2)
        self.assertEqual(list_m[0].match.id, 1)
        self.assertEqual(list_m[1].match.id, 1)

        # assert delivered by order it is sent
        self.assertEqual(list_m[0].id, 1)
        self.assertEqual(list_m[1].id, 2)

        # assert does not have messages not associated with match
        self.assertNotIn(3, [m.id for m in list_m])


class MessageTaskTest(TestCase):
    fixtures = [
        "tests/dummy_users.json",
        "tests/dummy_matches.json",
        "tests/dummy_messages.json",
    ]

    def test_message_task(self):
        message = Message.objects.get(pk=1)
        self.assertIsNone(message.delivered)
        m_serializer = MessageSerializer(message)

        updated_m = message_task(m_serializer.data)
        self.assertIsNotNone(updated_m.delivered)


class SendMessageViewsTest(TestCase):
    fixtures = [
        "tests/dummy_users.json",
        "tests/dummy_matches.json",
        "tests/dummy_messages.json",
    ]

    @patch("chat.views.message_task.delay")
    def test_send_message_user_in_match(self, message_task):
        user = User.objects.get(pk=1)
        factory = APIRequestFactory()
        request = factory.post(
            "chat/send/", {"match": 1, "content": "hello"}, format="json"
        )
        force_authenticate(request, user)
        view = SendMessage.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["match"], 1)
        self.assertEqual(response.data["sender"], 1)
        self.assertIsNotNone(response.data["sent"])
        message_task.assert_called_once_with(response.data)

    def test_send_message_user_not_in_match(self):
        user = User.objects.get(pk=3)
        factory = APIRequestFactory()
        request = factory.post(
            "chat/send/", {"match": 1, "content": "hello"}, format="json"
        )
        force_authenticate(request, user)
        view = SendMessage.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 403)

    def test_send_message_unmatched(self):
        user = User.objects.get(pk=3)
        factory = APIRequestFactory()
        request = factory.post(
            "chat/send/", {"match": 2, "content": "hello"}, format="json"
        )
        force_authenticate(request, user)
        view = SendMessage.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 403)

    def test_send_message_nonexistent_match(self):
        user = User.objects.get(pk=1)
        factory = APIRequestFactory()
        request = factory.post(
            "chat/send/", {"match": 4, "content": "hello"}, format="json"
        )
        force_authenticate(request, user)
        view = SendMessage.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 404)

    def test_send_message_match_key_missing(self):
        user = User.objects.get(pk=1)
        factory = APIRequestFactory()
        request = factory.post("chat/send/", {}, format="json")
        force_authenticate(request, user)
        view = SendMessage.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 404)


class GetConversationViewsTest(TestCase):
    fixtures = [
        "tests/dummy_users.json",
        "tests/dummy_matches.json",
        "tests/dummy_messages.json",
    ]

    def test_get_conversation_user_in_match(self):
        user = User.objects.get(pk=1)
        factory = APIRequestFactory()
        request = factory.get("chat/convo?match=1")
        force_authenticate(request, user)
        view = GetConversation.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        self.assertEqual(response.data[0]["match"], 1)
        self.assertEqual(response.data[1]["match"], 1)
        self.assertNotIn(2, [m["match"] for m in response.data])

    def test_get_conversation_user_not_in_match(self):
        user = User.objects.get(pk=3)
        factory = APIRequestFactory()
        request = factory.get("chat/convo?match=1")
        force_authenticate(request, user)
        view = GetConversation.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 403)

    def test_get_conversation_unmatched(self):
        user = User.objects.get(pk=3)
        factory = APIRequestFactory()
        request = factory.get("chat/convo?match=2")
        force_authenticate(request, user)
        view = GetConversation.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 403)

    def test_get_conversation_nonexistent_match(self):
        user = User.objects.get(pk=1)
        factory = APIRequestFactory()
        request = factory.get("chat/convo?match=6")
        force_authenticate(request, user)
        view = GetConversation.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 404)

    def test_get_conversation_keyword_missing(self):
        user = User.objects.get(pk=1)
        factory = APIRequestFactory()
        request = factory.get("chat/convo/")
        force_authenticate(request, user)
        view = GetConversation.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 404)
