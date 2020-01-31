from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from users.serializers import UserIdSerializer
from .models import Interaction, Block


class Skip(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = UserIdSerializer(data=request.data)
        if serializer.is_valid():
            swiped_on = serializer.validated_data["user"]
            Interaction.objects.skip(request.user, swiped_on)
            return Response("Pass!", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Smash(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = UserIdSerializer(data=request.data)
        if serializer.is_valid():
            swiped_on = serializer.validated_data["user"]
            Interaction.objects.smash(request.user, swiped_on)
            return Response("Smash!", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Top5(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = UserIdSerializer(data=request.data, many=True)
        if serializer.is_valid():
            top5_users_raw = serializer.validated_data
            if Interaction.objects.filter(swiper=request.user, top5=True).exists():
                return Response(
                    "User already has top5 requests", status=status.HTTP_400_BAD_REQUEST
                )
            elif len(top5_users_raw) > 5:
                return Response(
                    "Cannot submit more than 5 top5 requests",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                top5_users = []
                [top5_users.append(x) for x in top5_users_raw if x not in top5_users]
                for user in top5_users:
                    Interaction.objects.top5(request.user, user["user"])
                return Response("Top5 submitted!", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetNext(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        return Response("Not implemented")


class Refresh(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        return Response("Not implemented")


class BlockView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = UserIdSerializer(data=request.data)
        if serializer.is_valid():
            blocked = serializer.validated_data["user"]
            Block.objects.block(request.user, blocked)
            return Response("Blocked!", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
