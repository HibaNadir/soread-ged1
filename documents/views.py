from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.decorators import action
from django.http import FileResponse
from django.db.models import Q

from .models import Document, DocumentVersion, DocumentShare
from .serializers import (
    DocumentSerializer,
    DocumentVersionSerializer,
    DocumentShareSerializer,
)


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.owner == request.user


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        return Document.objects.filter(
            owner=self.request.user,
            is_deleted=False
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)
    def destroy(self, request, *args, **kwargs):
        document = self.get_object()

        document.is_deleted = True
        document.save(update_fields=["is_deleted"])

        return Response(
            {"message": "Document moved to recycle bin"},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"])
    def restore(self, request, pk=None):
        document = self.get_object()

        document.is_deleted = False
        document.save(update_fields=["is_deleted"])

        return Response(
            {"message": "Document restored"},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["get"])
    def download(self, request, pk=None):
        document = self.get_object()

        return FileResponse(
            document.file.open("rb"),
            as_attachment=True
        )

    @action(detail=False, methods=["get"])
    def search(self, request):
        query = request.GET.get("q")

        documents = self.get_queryset()

        if query:
            documents = documents.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query)
            )

        serializer = self.get_serializer(documents, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def recycle_bin(self, request):
        documents = Document.objects.filter(
            owner=request.user,
            is_deleted=True
        )

        serializer = self.get_serializer(documents, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def favorite(self, request, pk=None):
        document = self.get_object()

        document.is_favorite = not document.is_favorite
        document.save(update_fields=["is_favorite"])

        return Response({
            "favorite": document.is_favorite
        })

    @action(detail=False, methods=["get"])
    def dashboard(self, request):
        return Response({
            "documents": Document.objects.filter(
                owner=request.user,
                is_deleted=False
            ).count(),

            "favorites": Document.objects.filter(
                owner=request.user,
                is_favorite=True
            ).count(),

            "deleted": Document.objects.filter(
                owner=request.user,
                is_deleted=True
            ).count(),
        })
    @action(detail=True, methods=["get"])
    def versions(self, request, pk=None):
        document = self.get_object()

        versions = DocumentVersion.objects.filter(
            document=document
        ).order_by("-version")

        serializer = DocumentVersionSerializer(
            versions,
            many=True
        )

        return Response(serializer.data)
    
    @action(detail=True, methods=["post"])
    def create_version(self, request, pk=None):

        document = self.get_object()

        version = DocumentVersion.objects.create(
            document=document,
            file=document.file,
            version=document.versions.count() + 1,
            created_by=request.user
        )

        serializer = DocumentVersionSerializer(version)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
    

    @action(detail=True, methods=["post"])
    def restore_version(self, request, pk=None):

        document = self.get_object()

        version_id = request.data.get("version")

        try:
            version = DocumentVersion.objects.get(
                id=version_id,
                document=document
            )

            document.file = version.file
            document.save(update_fields=["file"])

            return Response({
                "message": "Version restored successfully"
            })

        except DocumentVersion.DoesNotExist:
            return Response(
                {"error": "Version not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
    
    @action(detail=True, methods=["post"])
    def share(self, request, pk=None):
        from accounts.models import User

        document = self.get_object()

        user_id = request.data.get("user")
        permission = request.data.get("permission", "READ")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        share, created = DocumentShare.objects.update_or_create(
            document=document,
            user=user,
            defaults={
                "permission": permission
            }
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
            many=True
        )

        return Response(serializer.data)


    @action(detail=True, methods=["delete"])
    def remove_share(self, request, pk=None):

        document = self.get_object()

        user_id = request.data.get("user")

        deleted, _ = DocumentShare.objects.filter(
            document=document,
            user_id=user_id
        ).delete()

        if deleted:
            return Response({
                "message": "Share removed"
            })

        return Response(
            {"error": "Share not found"},
            status=status.HTTP_404_NOT_FOUND
        )