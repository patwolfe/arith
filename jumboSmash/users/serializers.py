from rest_framework import serializers
from users.models import User, Profile, Photo

class UserIdSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "preferred_name", "discoverable", "status"]

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ["user", "path", "approved", "order"]

class PhotoField(serializers.Field):
    def to_representation(self, value):
        profile_user_id = str(value.user.id)
        auth_user_id = str(self.context.get("request").user.id)
        same_user = profile_user_id == auth_user_id

        photos = Photo.objects.filter(user=profile_user_id).order_by("order")
        serialized_photos = PhotoSerializer(photos, many=True)
        ret = [None] * 6

        for photo in serialized_photos.data:
            if photo.get("approved"):
                ret[photo.get("order")] = photo
            elif same_user:
                ret[photo.get("order")] = photo
            else:
                pass

        return ret

    def to_internal_value(self, data):
        pass
        # TO DO
        # data = data.strip('rgb(').rstrip(')')
        # red, green, blue = [int(col) for col in data.split(',')]
        # return Color(red, green, blue)

class ProfileSerializer(serializers.ModelSerializer):
    photos = PhotoField(source="*")

    class Meta:
        model = Profile
        fields = ["user", "bio", "photos"]
