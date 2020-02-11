from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from users.models import User, ProfileBody, PhotoSet
from users.serializers import (
    UserIdSerializer,
    SimpleUserSerializer,
    ProfileSerializer,
    PhotoSetSerializer,
)
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.shortcuts import render
import logging


class ListUsers(APIView):
    """
    View to get list of all users
    """

    def get(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class GetProfile(APIView):
    """
    Get a profile and photos for user
    """

    # TODO don't show if banned

    def get(self, request):
        serializer = UserIdSerializer(data=request.query_params)
        if serializer.is_valid():
            requested_user = serializer.validated_data["user"]
            serializer = ProfileSerializer(
                requested_user, context={"user": request.user}
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditProfile(APIView):
    """
    Edit profile for currently logged in user
    """

    def get(self, request):
        return Response(PhotoSet.objects.get_upload_urls(request.user.id))

    def post(self, request):
        user_id = request.user.id
        serializer = ProfileSerializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid()  # Should do some handling here
        serializer.save()
        return Response("what should this respond?")


class CheckUserExists(APIView):
    """
    Endpoint to confirm email is in our list of seniors.
    """

    permissions = [AllowAny]

    def get(self, request):
        email = request.query_params.get("email")
        if not email:
            return render(request, "user_check.html", {})
        try:
            user = User.objects.get(email=email)
            return render(
                request, "successful_check.html", {"email": email, "user": user},
            )
        except:
            return render(request, "failed_check.html", {"email": email})
