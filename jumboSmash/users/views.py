from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import User, Profile
from users.serializers import UserSerializer, ProfileSerializer
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

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
