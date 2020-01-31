from rest_framework import serializers
from users.models import User, Profile, Photo

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "preferred_name", "discoverable", "status"]

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["user", "bio"]

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ["user", "path", "approved"]

class UserIdSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
