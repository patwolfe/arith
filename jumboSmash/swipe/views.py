from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from users.serializers import UserIdSerializer


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


class List(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        return Response("Not implemented")


class Refresh(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        return Response("Not implemented")
