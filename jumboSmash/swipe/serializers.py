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
        if data["reaction"] == None or data["reacted_to"] == None:
            raise serializers.ValidationError("smash interactions must contain a reaction")
        return data
