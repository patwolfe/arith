from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser as User
from .serializers import UserSerializer


class CheckUser(APIView):
    """
    View to check is email is in users
    """

    def get(self, request, format=None):
        """
        Returns "true"/"false" depending on if email corresponds to user.
        """
        email = request.query_params.get("email", None)
        if email is not None:
            try:
                user = User.objects.get(email=email)
                return Response("true")
            except User.DoesNotExist:
                return Response("false")
        return Response("invalid query")

class RetrieveUser(APIView):
    """
    View to get user by email
    """
    def get(self, request, format=None):
        """
        Retrieve serialized User object.
        """
        email = request.query_params.get("email", None)
        if email is not None:
            try:
                user = User.objects.get(email=email)
                serialized = UserSerializer(user)
                return Response(serialized.data)
            except User.DoesNotExist:
                return Response("User not found")
        else:
            return Response("invalid query")
