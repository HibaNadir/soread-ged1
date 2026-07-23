from rest_framework import serializers
from .models import User

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
class UserManagementSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "service",
            "is_active",
        ]
from rest_framework import serializers


class CSVImportSerializer(serializers.Serializer):
    file = serializers.FileField()
    
class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        write_only=True,
        min_length=8
    )