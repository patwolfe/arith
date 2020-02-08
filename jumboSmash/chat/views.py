from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Message, Match
from .serializers import MatchIdSerializer, MessageSerializer, SendMessageSerializer
from .tasks import message_task


class Unmatch(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        current_user_id = request.user.id
        serializer = MatchIdSerializer(data=request.data)
        if serializer.is_valid():
            match = serializer.validated_data["match"]
            if match.user_1.pk == current_user_id or match.user_2.pk == current_user_id:
                Match.objects.unmatch(match)
                return Response("Unmatched", status=status.HTTP_201_CREATED)
            else:
                return Response(
                    "You are not in this match", status=status.HTTP_403_FORBIDDEN
                )

        return Response("Invalid request", status=status.HTTP_400_BAD_REQUEST)


class SendMessage(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = SendMessageSerializer(data=request.data)
        if serializer.is_valid():
            match = serializer.validated_data["match"]
            content = serializer.validated_data["content"]
            if not match.unmatched and (
                match.user_1 == request.user or match.user_2 == request.user
            ):
                message = Message.objects.create_message(match, request.user, content)
                m_serializer = MessageSerializer(message)
                message_task.delay(m_serializer.data)
                return Response(m_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    "User does not have access to this match.",
                    status=status.HTTP_403_FORBIDDEN,
                )
        else:
            return Response("Match does not exist", status=status.HTTP_404_NOT_FOUND)


class GetConversation(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """get all messages for match_id."""
        match_id = request.query_params.get("match", None)
        if match_id:
            try:
                match = Match.objects.get(pk=match_id)
                if not match.unmatched and (
                    match.user_1 == request.user or match.user_2 == request.user
                ):
                    conversation = Message.objects.list_messages(match)
                    serialized = MessageSerializer(conversation, many=True)
                    return Response(serialized.data, status=status.HTTP_200_OK)
                else:
                    return Response(
                        "User does not have access to this conversation.",
                        status=status.HTTP_403_FORBIDDEN,
                    )
            except Match.DoesNotExist:
                return Response("Match does not exist", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("Invalid query.", status=status.HTTP_404_NOT_FOUND)
