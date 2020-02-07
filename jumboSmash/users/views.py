from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import User, Profile
from users.serializers import SimpleUserSerializer, FullUserSerializer
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

class ListUsers(APIView):
    """
    View to get list of all users
    """
    def get(self, request):
        queryset = User.objects.all()
        serializer = SimpleUserSerializer(queryset, many=True)
        return Response(serializer.data)

class GetProfile(APIView):
    """
    Get a profile and photos for user
    """
    # TODO don't show if banned
    def get(self, request):
        user_id = request.query_params.get("id")
        user = User.objects.get(id=user_id)
        serializer = FullUserSerializer(user, context={"request": request})
        return Response(serializer.data)

class EditProfile(APIView):
    """
    Edit profile for currently logged in user
    """
    def post(self, request):
        user_id = request.user.id
        serializer = FullUserSerializer(data=request.data, context={"request": request})
        serializer.is_valid()
        print("-----------------------------------")
        print(serializer.validated_data)
        print("-----------------------------------")
        user = User.objects.edit(user_id, serializer.validated_data)
        ret_serializer = FullUserSerializer(user, context={"request": request})
        return Response(ret_serializer.data)
