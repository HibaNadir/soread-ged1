from django.contrib import admin
from .models import Document, DocumentVersion, DocumentShare


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "owner",
        "folder",
        "is_deleted",
        "is_favorite",
        "created_at",
    )
    list_filter = ("is_deleted", "is_favorite", "created_at")
    search_fields = ("title", "description", "owner__username")


@admin.register(DocumentVersion)
class DocumentVersionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "document",
        "version",
        "created_by",
        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = ("document__title",)


@admin.register(DocumentShare)
class DocumentShareAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "document",
        "user",
        "permission",
        "shared_at",
    )
    list_filter = ("permission",)
    search_fields = (
        "document__title",
        "user__username",
    )