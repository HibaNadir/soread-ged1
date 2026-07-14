from rest_framework import serializers
from .models import Document, DocumentVersion, DocumentShare
from .models import DocumentVersion, DocumentShare


class DocumentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Document
        fields = "__all__"
        read_only_fields = (
            "owner",
            "created_at",
            "updated_at",
        )


class DocumentVersionSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.username")

    class Meta:
        model = DocumentVersion
        fields = "__all__"
        read_only_fields = (
            "created_by",
            "created_at",
        )


class DocumentShareSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = DocumentShare
        fields = "__all__"
        read_only_fields = (
            "shared_at",
        )
        class DocumentVersionSerializer(serializers.ModelSerializer):
         created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = DocumentVersion
        fields = [
            "id",
            "document",
            "file",
            "version",
            "created_by",
            "created_at",
        ]
        read_only_fields = [
            "version",
            "created_by",
            "created_at",
        ]


class DocumentShareSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = DocumentShare
        fields = [
            "id",
            "document",
            "user",
            "permission",
            "shared_at",
        ]
        read_only_fields = [
            "shared_at",
        ]