from rest_framework import serializers
from .models import Folder


class FolderSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Folder
        fields = "__all__"