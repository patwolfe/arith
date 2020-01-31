from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from users.serializers import UserIdSerializer, UserSerializer
from .models import Interaction, Deck, Swipable, Block
from users.models import CustomUser as User

class Skip(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = UserIdSerializer(data=request.data)
        if serializer.is_valid():
            swiped_on = serializer.validated_data["user"]
            Interaction.objects.skip(request.user, swiped_on)
            return Response("Pass!")
        else:
            return Response("Invalid skip request")


class Smash(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = UserIdSerializer(data=request.data)
        if serializer.is_valid():
            swiped_on = serializer.validated_data["user"]
            Interaction.objects.smash(request.user, swiped_on)
            return Response("Smash!")
        else:
            return Response("Invalid smash request")


class GetNext(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        deck = Swipable.objects.get_next(request.user)
        message = UserSerializer(deck, many=True)
        return Response(message.data)


class Refresh(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        Swipable.objects.build(request.user)
        return Response("Refreshed the deck, swipe away!")


class BlockView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = UserIdSerializer(data=request.data)
        if serializer.is_valid():
            blocked = serializer.validated_data["user"]
            Block.objects.block(request.user, blocked)
            return Response("Blocked!")
        else:
            return Response("Invalid block request")
