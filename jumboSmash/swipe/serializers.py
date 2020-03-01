from rest_framework import serializers
from swipe.models import Interaction

class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = [
            "reacted_to",
            "reaction",
            "swiped_on",
        ]

    def validate(self, data):
        if "reaction" not in data or "reacted_to" not in data:
            raise serializers.ValidationError("smash interactions must contain a reaction")
        return data
