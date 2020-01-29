from rest_framework import serializers
from .models import Match, Message
from users.models import CustomUser as User


class MatchIdSerializer(serializers.Serializer):
    match = serializers.PrimaryKeyRelatedField(queryset=Match.objects.all())


class MessageSerializer(serializers.Serializer):
    match = serializers.PrimaryKeyRelatedField(queryset=Match.objects.all())
    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    content = serializers.CharField()
    sent = serializers.DateTimeField()
    delivered = serializers.DateTimeField(allow_null=True)
    read = serializers.NullBooleanField()