from rest_framework import serializers
from .models import Match
from .models import Message


class MatchIdSerializer(serializers.Serializer):
    match = serializers.PrimaryKeyRelatedField(queryset=Match.objects.all())


class MessageIdSerializer(serializers.Serializer):
    message = serializers.PrimaryKeyRelatedField(queryset=Message.objects.all())
