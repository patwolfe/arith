from rest_framework import serializers
from users.models import User, Profile, Photo
from django.core.exceptions import ObjectDoesNotExist

class UserIdSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "preferred_name", "discoverable", "status", "id_photo"]

class PhotoURLsField(serializers.Field):
    def to_representation(self, value):
        return [value.photo0, value.photo1, value.photo2, value.photo3, value.photo4, value.photo5]

    def to_internal_value(self, data):
        ret = {
            "photo0": data[0],
            "photo1": data[1],
            "photo2": data[2],
            "photo3": data[3],
            "photo4": data[4],
            "photo5": data[5]
        }
        return ret

class PhotoSerializer(serializers.ModelSerializer):
    urls = PhotoURLsField(source="*")

    class Meta:
        model = Photo
        fields = ["approved", "urls"]

class PhotoField(serializers.Field):
    def to_representation(self, value):
        profile_user_id = str(value.id)
        auth_user_id = str(self.context.get("request").user.id)
        same_user = profile_user_id == auth_user_id

        approved_photos, unapproved_photos = Photo.objects.get_photos(profile_user_id)
        photos = None

        if approved_photos:
            photos = approved_photos

        if unapproved_photos and same_user:
            photos = unapproved_photos

        serialized_photos = PhotoSerializer(photos)
        return serialized_photos.data if photos else None

    def to_internal_value(self, data):
        serializer = PhotoSerializer(data=data)
        serializer.is_valid()
        return {
            "photos": serializer.validated_data
        }

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ["bio"]

class ProfileField(serializers.Field):
    def to_representation(self, value):
        user_id = value.id
        profile = None

        try:
            profile = Profile.objects.get(user=user_id)
        except ObjectDoesNotExist:
            pass

        serialized_profile = ProfileSerializer(profile)

        return serialized_profile.data if profile else None

    def to_internal_value(self, data):
        serializer = ProfileSerializer(data=data)
        serializer.is_valid()
        serializer.errors
        return {
            "profile": serializer.validated_data
        }


class FullUserSerializer(SimpleUserSerializer):
    profile = ProfileField(source="*")
    photos = PhotoField(source="*")

    class Meta:
        model = User
        fields = SimpleUserSerializer.Meta.fields + ["profile", "photos"]
        extra_kwargs = {
            'id': {'read_only': False},
            'email': {'validators': []},
        }
