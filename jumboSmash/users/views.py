from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from users.models import User, Profile
from users.serializers import UserSerializer, ProfileSerializer
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.shortcuts import render


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

    def get(self, request):
        user_id = request.query_params.get("id")
        profile = Profile.objects.get(user=user_id)
        serializer = ProfileSerializer(profile, context={"request": request})
        return Response(serializer.data)


class EditProfile(APIView):
    """
    Edit profile for currently logged in user
    """

    def post(self, request):
        return Response()


class CheckUserExists(APIView):
    """
    Endpoint to confirm email is in our list of seniors.
    """

    permissions = [AllowAny]

    def get(self, request):
        email = request.query_params.get("email")
        if not email:
            return render(request, "user_check.html", {})

        # try:
        user = User.objects.get(email=email)
        print(UserSerializer(user).data)
        return render(request, "successful_check.html", {"email": email, "user": user},)
        # except:
        #    return render(request, "failed_check.html", {"email": email})
