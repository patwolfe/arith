from rest_framework import serializers
from .models import Match, Message


class MatchIdSerializer(serializers.Serializer):
    match = serializers.PrimaryKeyRelatedField(queryset=Match.objects.all())

    def validate(self, data):
        """Confirms user is in match."""
        user = self.context["user"]
        if (data["match"].user_1 != user and data["match"].user_2 != user) or data["match"].unmatched:
            raise serializers.ValidationError("User does not have access to this match.")
        return data


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class SendMessageSerializer(serializers.Serializer):
    match = serializers.PrimaryKeyRelatedField(queryset=Match.objects.all())
    content = serializers.CharField()
