from rest_framework import serializers
from .models import Match

class MatchIdSerializer(serializers.Serializer):
    match = serializers.PrimaryKeyRelatedField(queryset=Match.objects.all())