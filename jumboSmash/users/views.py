from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import CustomUser as User


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
    def getUser(self, request):
        """
        Retrieve User object.
        """
    email = request.query_params.get("email", None)
    if email is not None:
        return User.objects.get(email=email)
    else:
        return Response("invalid query")
