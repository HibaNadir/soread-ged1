from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User


class EmailOrUsernameTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        identifier = attrs.get("username", "")

        if "@" in identifier:
            user = User.objects.filter(email__iexact=identifier).first()
            if user:
                attrs["username"] = user.username

        return super().validate(attrs)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "service",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User(
            username=validated_data["username"],
            email=validated_data.get("email"),
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
            service=validated_data.get("service"),
            role="USER"
        )

        user.set_password(password)
        user.save()

        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "service",
            "role",
            "date_joined",
        ]
        read_only_fields = ["id", "username", "role", "date_joined"]