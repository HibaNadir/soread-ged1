from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import FileResponse

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from drf_spectacular.utils import extend_schema
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from notifications.models import Notification
from spaces.models import SpaceMember, SpaceActivity

from .models import (
    Document,
    DocumentVersion,
    DocumentShare,
)

from .serializers import (
    DocumentSerializer,
    DocumentVersionSerializer,
    DocumentShareSerializer,
    ShareDocumentSerializer,
)

User = get_user_model()
class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.owner == request.user


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    parser_classes = (MultiPartParser, FormParser)
    def get_queryset(self):
        queryset = Document.objects.filter(
            owner=self.request.user,
            is_deleted=False
        )

        title = self.request.query_params.get("title")
        space = self.request.query_params.get("space")
        pinned = self.request.query_params.get("pinned")

        if title:
            queryset = queryset.filter(title__icontains=title)

        if space:
            queryset = queryset.filter(space_id=space)

        if pinned is not None:
            if pinned.lower() == "true":
                queryset = queryset.filter(is_pinned=True)
            elif pinned.lower() == "false":
                queryset = queryset.filter(is_pinned=False)

        return queryset

    def perform_create(self, serializer):

        space = serializer.validated_data.get("space")

        if space:
            is_member = SpaceMember.objects.filter(
                space=space,
                user=self.request.user
            ).exists()

            if not is_member:
                raise PermissionDenied(
                    "Vous n'êtes pas membre de cet espace."
                )

        document = serializer.save(owner=self.request.user)

        if document.space:
            SpaceActivity.objects.create(
            space=document.space,
            user=self.request.user,
            document=document,
            action="DOCUMENT_ADDED",
        )

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        document = self.get_object()

        document.is_deleted = True
        document.save(update_fields=["is_deleted"])

        return Response(
            {"message": "Document moved to recycle bin"},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def restore(self, request, pk=None):
        document = self.get_object()

        document.is_deleted = False
        document.save(update_fields=["is_deleted"])

        return Response(
            {"message": "Document restored"},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["get"])
    def download(self, request, pk=None):
        document = self.get_object()

        return FileResponse(
            document.file.open("rb"),
            as_attachment=True,
        )

    @action(detail=False, methods=["get"])
    def search(self, request):
        query = request.GET.get("q")

        documents = self.get_queryset()

        if query:
            documents = documents.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
            )

        serializer = self.get_serializer(documents, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def recycle_bin(self, request):
        documents = Document.objects.filter(
            owner=request.user,
            is_deleted=True,
        )

        serializer = self.get_serializer(documents, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def favorite(self, request, pk=None):
        document = self.get_object()

        document.is_favorite = not document.is_favorite
        document.save(update_fields=["is_favorite"])

        return Response(
            {
                "favorite": document.is_favorite
            }
        )
    @action(detail=True, methods=["post"])
    def pin(self, request, pk=None):
        document = self.get_object()

        document.is_pinned = not document.is_pinned
        document.save(update_fields=["is_pinned"])

        return Response(
            {
                "pinned": document.is_pinned
            }
        )
    
    @action(detail=False, methods=["get"])
    def dashboard(self, request):
        return Response(
            {
                "documents": Document.objects.filter(
                    owner=request.user,
                    is_deleted=False,
                ).count(),

                "favorites": Document.objects.filter(
                    owner=request.user,
                    is_favorite=True,
                ).count(),

                "deleted": Document.objects.filter(
                    owner=request.user,
                    is_deleted=True,
                ).count(),
            }
        )

    # ==========================
    # Versions
    # ==========================

    @action(detail=True, methods=["get"])
    def versions(self, request, pk=None):
        document = self.get_object()

        versions = DocumentVersion.objects.filter(
            document=document
        ).order_by("-version")

        serializer = DocumentVersionSerializer(
            versions,
            many=True,
        )

        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def create_version(self, request, pk=None):
        document = self.get_object()

        version = DocumentVersion.objects.create(
            document=document,
            file=document.file,
            version=document.versions.count() + 1,
            created_by=request.user,
        )

        serializer = DocumentVersionSerializer(version)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["post"])
    def restore_version(self, request, pk=None):
        document = self.get_object()

        version_id = request.data.get("version")

        try:
            version = DocumentVersion.objects.get(
                id=version_id,
                document=document,
            )

            document.file = version.file
            document.save(update_fields=["file"])

            return Response(
                {
                    "message": "Version restored successfully"
                }
            )

        except DocumentVersion.DoesNotExist:
            return Response(
                {
                    "error": "Version not found"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

    # ==========================
    # Partage
    # ==========================
    @extend_schema(
        request=ShareDocumentSerializer,
        responses=DocumentShareSerializer,
    )
    @action(detail=True, methods=["post"])
    def share(self, request, pk=None):

        print("REQUEST DATA =", request.data)

        document = self.get_object()

        user_id = request.data.get("user")
        permission = request.data.get("permission", "READ")

        print("USER ID =", user_id)
        try:
            user = User.objects.get(id=user_id)

        except User.DoesNotExist:
            return Response(
                {
                    "error": "User not found"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        share, created = DocumentShare.objects.update_or_create(
            document=document,
            user=user,
            defaults={
                "permission": permission,
            },
        )
        from notifications.models import Notification

        Notification.objects.create(
        user=user,
        title="Document partagé",
        message=f"Le document '{document.title}' a été partagé avec vous.",
        notification_type="DOCUMENT",
        )
        serializer = DocumentShareSerializer(share)

        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def shared_users(self, request, pk=None):
        document = self.get_object()

        shares = DocumentShare.objects.filter(
            document=document
        )

        serializer = DocumentShareSerializer(
            shares,
            many=True,
        )

        return Response(serializer.data)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "user",
                openapi.IN_QUERY,
                description="ID de l'utilisateur à qui retirer le partage",
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ]
    )
    @action(detail=True, methods=["delete"])
    def remove_share(self, request, pk=None):

        document = self.get_object()

        user_id = request.query_params.get("user")

        if not user_id:
            return Response(
                {"error": "User parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        deleted, _ = DocumentShare.objects.filter(
            document=document,
            user_id=user_id
        ).delete()

        if deleted:
            return Response({"message": "Share removed"})

        return Response(
            {"error": "Share not found"},
            status=status.HTTP_404_NOT_FOUND
        )