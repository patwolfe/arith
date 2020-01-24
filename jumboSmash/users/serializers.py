from rest_framework import serializers
from .models import CustomUser as User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password"]
