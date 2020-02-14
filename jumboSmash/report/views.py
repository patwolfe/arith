from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

class ReportView(APIView):
    """Report a user"""
    def get(self, request):
        # permission_classes = [AllowAny]
        return Response("reported")
