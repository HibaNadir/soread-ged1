from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Space, SpaceMember
from .models import Space, SpaceMember, SpaceActivity

User = get_user_model()


class SpaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Space
        fields = "__all__"
        read_only_fields = ("created_by", "created_at")


class SpaceMemberSerializer(serializers.ModelSerializer):

    username = serializers.CharField(write_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SpaceMember
        fields = (
            "id",
            "space",
            "user",
            "username",
            "role",
            "joined_at",
        )
        read_only_fields = (
            "joined_at",
            "space",
            "user",
        )

    def create(self, validated_data):
        username = validated_data.pop("username")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"username": "Utilisateur introuvable."}
            )

        return SpaceMember.objects.create(
            user=user,
            **validated_data
        )
class SpaceActivitySerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField()
    document = serializers.StringRelatedField()

    class Meta:
        model = SpaceActivity
        fields = [
            "id",
            "user",
            "document",
            "action",
            "created_at",
        ]