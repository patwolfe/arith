from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from users.models import User, Profile
from users.serializers import (
    UserIdSerializer,
    SimpleUserSerializer,
    ProfileSerializer,
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
    Get a profile for given user
    """

    # TODO don't show if banned <- or should this be blocked elsewhere

    def get(self, request):
        user_serializer = UserIdSerializer(data=request.query_params)
        user_serializer.is_valid(raise_exception=True)
        requested_user = user_serializer.validated_data["user"]
        approved, pending = Profile.objects.get_profiles(requested_user)
        if requested_user == request.user:
            serializer = ProfileSerializer(pending)
        else:
            serializer = ProfileSerializer(approved)
        return Response(serializer.data)


class EditProfile(APIView):
    """
    Edit profile for currently logged in user
    """

    def get(self, request):
        return Response({"d": Profile.objects.get_upload_urls(request.user.id)})

    def post(self, request):
        user_id = request.user.id
        serializer = ProfileSerializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        return Response("what should this respond")


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
