from rest_framework import serializers
from users.models import User, ProfileBody, PhotoSet
from django.core.exceptions import ObjectDoesNotExist
from types import SimpleNamespace


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


class ProfileBodySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileBody
        fields = ["bio"]

    def create(self, validated_data):
        profile_body, _ = ProfileBody.objects.get_or_create(user=self.context["user"])
        profile_body.bio = validated_data["bio"]
        profile_body.save()
        return profile_body


class PhotoSetSerializer(serializers.ModelSerializer):
    display_urls = serializers.SerializerMethodField()

    class Meta:
        model = PhotoSet
        fields = "__all__"
        read_only_fields = ["approved", "user"]

    def validate(self, data):
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
            raise serializers.ValidationError("PhotoSet must have at least 3 photos")
        return data

    def get_display_urls(self, obj):
        return obj.get_display_urls()

    def create(self, validated_data):
        "Creates and saves a new pending PhotoSet or updates existing pending set"
        user = self.context["user"]
        validated_data["user"] = user
        new_set = PhotoSet(**validated_data)
        sets = PhotoSet.objects.filter(user=user)
        approved_set = sets.filter(approved=True)
        pending_set = sets.filter(approved=False)
        if approved_set and approved_set.first().is_reorder(new_set):
            approved_set.update(**validated_data)
            return approved_set.first()
        elif pending_set:
            pending_set.update(**validated_data)
            return pending_set.first()
        else:
            new_set.save()
            return new_set


class ProfileSerializer(serializers.Serializer):
    photos = PhotoSetSerializer()
    profile_body = ProfileBodySerializer()
    user = SimpleUserSerializer(required=False)

    def to_representation(self, user_instance):
        data = {}
        data["user"] = SimpleUserSerializer(user_instance).data

        get_approved = user_instance == self.context["user"]
        data["photos"] = PhotoSetSerializer(
            PhotoSet.objects.filter(user=user_instance, approved=get_approved).first()
        ).data
        data["profile_body"] = ProfileBodySerializer(
            ProfileBody.objects.filter(user=user_instance).first()
        ).data

        return data

    def save(self):
        photo_serializer = PhotoSetSerializer(
            data=self.validated_data["photos"], context={"user": self.context["user"]}
        )
        photo_serializer.is_valid()
        photo_serializer.save()

        profile_serializer = ProfileBodySerializer(
            data=self.validated_data["profile_body"],
            context={"user": self.context["user"]},
        )
        profile_serializer.is_valid()
        profile_serializer.save()
