from rest_framework import serializers
from users.models import User, Profile
from django.core.exceptions import ObjectDoesNotExist
from types import SimpleNamespace
import logging


class UserIdSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "preferred_name",
        ]


class ProfileSerializer(serializers.ModelSerializer):
    display_urls = serializers.SerializerMethodField()
    user_data = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        exclude = ["user", "id"]
        read_only_fields = ["approved"]

    def get_display_urls(self, obj):
        return obj.get_display_urls()

    def get_user_data(self, obj):
        return SimpleUserSerializer(obj.user).data

    def validate(self, data):
        """ Confirm new photo order is valid """
        empty_photo = False
        photo_count = 0
        for i in range(0, 6):
            photo = data["photo" + str(i)]
            empty_photo = (photo is None) or empty_photo
            if photo is not None:
                photo_count += 1
                if empty_photo:
                    raise serializers.ValidationError(
                        "Cannot have photos after empty photo slot"
                    )
                if photo < 0 or photo > 11:
                    raise serializers.ValidationError("Photo id out of range")

        if photo_count < 3:
            raise serializers.ValidationError("Profile must have at least 3 photos")
        return data

    def create(self, validated_data):
        "Creates and saves a new pending profile or updates existing profile"
        user = self.context["user"]
        validated_data["user"] = user
        approved_set, pending_set = Profile.objects.get_profiles(user=user)

        if approved_set and approved_set.is_photo_reorder(Profile(**validated_data)):
            new_set = approved_set.update(**validated_data)
        elif pending_set:
            new_set = pending_set.update(**validated_data)
        else:
            new_set = Profile(**validated_data)
            new_set.save()
        return new_set
