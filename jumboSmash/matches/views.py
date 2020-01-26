from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from matches.serializers import MatchIdSerializer
from matches.models import Match


class Unmatch(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        current_user_id = request.user.id
        serializer = MatchIdSerializer(data=request.data)
        if serializer.is_valid():
            match = serializer.validated_data["match"]
            if match.user_1.pk == current_user_id or match.user_2.pk == current_user_id:
                Match.objects.unmatch(match.pk)
                return Response("Unmatched")
            else:
                return Response(
                    "You are not in this match", status=status.HTTP_401_UNAUTHORIZED
                )

        return Response("Invalid request", status=status.HTTP_400_BAD_REQUEST)
