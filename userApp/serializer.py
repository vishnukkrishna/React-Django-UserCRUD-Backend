from rest_framework import serializers
from userApp.models import User, Notes


class UserSerializer(serializers.ModelSerializer):
    # Model is passed to serializer
    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "profile_img"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ["title", "description", "rating"]
