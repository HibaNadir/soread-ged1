from rest_framework import serializers
from .models import Document, DocumentVersion, DocumentShare


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

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)

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
    
class ShareDocumentSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    permission = serializers.ChoiceField(
        choices=[
            ("READ", "READ"),
            ("WRITE", "WRITE"),
        ]
    )