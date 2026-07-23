from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

from .models import Space, SpaceMember, SpaceActivity
from documents.models import Document

from .serializers import (
    SpaceSerializer,
    SpaceMemberSerializer,
    SpaceActivitySerializer,
)

class SpaceViewSet(viewsets.ModelViewSet):
    serializer_class = SpaceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Space.objects.filter(
            Q(is_private=False) |
            Q(created_by=self.request.user) |
            Q(spacemember__user=self.request.user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"])
    def add_member(self, request, pk=None):

        space = self.get_object()

    # Seul le créateur de l'espace peut ajouter des membres
        if space.created_by != request.user:
            return Response(
                {"error": "Vous n'êtes pas autorisé à ajouter des membres."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = SpaceMemberSerializer(data=request.data)

        if serializer.is_valid():

            from django.contrib.auth import get_user_model

            User = get_user_model()

            username = serializer.validated_data["username"]
            user = User.objects.get(username=username)

        # Vérifier si l'utilisateur est déjà membre
            if SpaceMember.objects.filter(space=space, user=user).exists():
                return Response(
                    {"error": "Cet utilisateur est déjà membre."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            member = serializer.save(space=space)
            SpaceActivity.objects.create(
                space=space,
                user=request.user,
                action="MEMBER_JOINED",
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @action(detail=True, methods=["get"])
    def members(self, request, pk=None):
        space = self.get_object()

        members = SpaceMember.objects.filter(space=space)
        serializer = SpaceMemberSerializer(members, many=True)

        return Response(serializer.data)
    @action(detail=True, methods=["patch"], url_path="members/(?P<member_id>[^/.]+)/role")
    def update_member_role(self, request, pk=None, member_id=None):

        space = self.get_object()

        try:
            member = SpaceMember.objects.get(id=member_id, space=space)
        except SpaceMember.DoesNotExist:
            return Response(
                {"error": "Membre introuvable."},
                status=status.HTTP_404_NOT_FOUND,
            )

        role = request.data.get("role")

        if role not in ["admin", "editor", "viewer"]:
            return Response(
                {"error": "Rôle invalide."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        member.role = role
        member.save()

        serializer = SpaceMemberSerializer(member)

        return Response(serializer.data)
    @action(detail=True, methods=["delete"], url_path="members/(?P<member_id>[^/.]+)")
    def remove_member(self, request, pk=None, member_id=None):
        
        space = self.get_object()

        try:
            member = SpaceMember.objects.get(id=member_id, space=space)
        except SpaceMember.DoesNotExist:
            return Response(
                {"error": "Membre introuvable."},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        SpaceActivity.objects.create(
            space=space,
            user=request.user,
            action="MEMBER_REMOVED",
        )

        member.delete()

        return Response(
            {"message": "Membre supprimé avec succès."},
            status=status.HTTP_204_NO_CONTENT,
        )
    @action(detail=True, methods=["get"])
    def activities(self, request, pk=None):

        space = self.get_object()

        activities = SpaceActivity.objects.filter(
           space=space
        ).order_by("-created_at")

        serializer = SpaceActivitySerializer(
            activities,
            many=True,
        )

        return Response(serializer.data)
    @action(detail=True, methods=["get"])
    def dashboard(self, request, pk=None):

        space = self.get_object()

        members_count = SpaceMember.objects.filter(
            space=space
        ).count()

        documents_count = Document.objects.filter(
            space=space,
            is_deleted=False
        ).count()

        pinned_count = Document.objects.filter(
            space=space,
            is_pinned=True,
            is_deleted=False
        ).count()

        recent_activity = SpaceActivity.objects.filter(
            space=space
        ).count()

        return Response({
            "space": space.name,
            "members": members_count,
            "documents": documents_count,
            "pinned_documents": pinned_count,
            "recent_activities": recent_activity,
        })