from urllib import request

from rest_framework import generics, viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.parsers import MultiPartParser
from drf_spectacular.utils import extend_schema

from .models import User
from .serializers import (
    RegisterSerializer,
    CSVImportSerializer,
    ResetPasswordSerializer,
)
import csv
import io

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.all()
    
    @action(detail=True, methods=["patch"])
    def deactivate(self, request, pk=None):

        user = self.get_object()

        user.is_active = False
        user.save(update_fields=["is_active"])

        return Response({
            "message": "Utilisateur désactivé."
        })
    @action(detail=True, methods=["patch"])
    def activate(self, request, pk=None):

        user = self.get_object()

        user.is_active = True
        user.save(update_fields=["is_active"])

        return Response({
            "message": "Utilisateur réactivé."
        })
    
    @action(detail=True, methods=["patch"])
    def reset_password(self, request, pk=None):

        user = self.get_object()

        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user.set_password(serializer.validated_data["new_password"])
        user.save()
    
        return Response({
            "message": "Mot de passe réinitialisé avec succès."
        })
    @extend_schema(
        request=CSVImportSerializer,
        responses={200: None},
    )
    @action(detail=False,methods=["post"],parser_classes=[MultiPartParser],)
    def import_csv(self, request):

        serializer = CSVImportSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        file = serializer.validated_data["file"]

        content = file.read()

        try:
            decoded = content.decode("utf-8")
        except UnicodeDecodeError:
            decoded = content.decode("cp1252")

        csv_file = io.StringIO(decoded)

        reader = csv.DictReader(csv_file)

        created = 0

        for row in reader:

            if User.objects.filter(username=row["username"]).exists():
                continue

            User.objects.create_user(
                username=row["username"],
                email=row["email"],
                password=row["password"],
                first_name=row.get("first_name", ""),
                last_name=row.get("last_name", ""),
                service=row.get("service", ""),
                role=row.get("role", "USER"),
            )

            created += 1

        return Response({
            "message": f"{created} utilisateurs importés."
        })
    