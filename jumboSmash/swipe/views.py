from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from users.serializers import UserIdSerializer, UserSerializer
from .models import Interaction, Deck, Swipable
from users.models import CustomUser as User


class Skip(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = UserIdSerializer(data=request.data)
        if serializer.is_valid():
            swipe_target = serializer.validated_data["user"]
            Interaction.objects.skip(request.user, swipe_target)
            return Response("Pass!")
        else:
            return Response("Invalid skip request")


class Smash(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = UserIdSerializer(data=request.data)
        if serializer.is_valid():
            swipe_target = serializer.validated_data["user"]
            Interaction.objects.smash(request.user, swipe_target)
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


class Block(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        return Response("Not implemented")
