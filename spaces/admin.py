from django.contrib import admin
from .models import Space, SpaceMember


@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_by", "is_private", "created_at")
    search_fields = ("name",)
    list_filter = ("is_private",)


@admin.register(SpaceMember)
class SpaceMemberAdmin(admin.ModelAdmin):
    list_display = ("space", "user", "role", "joined_at")
    list_filter = ("role",)