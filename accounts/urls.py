from django.urls import path

from .views import (
    RegisterView,
    UserViewSet,
)

user_list = UserViewSet.as_view({
    "get": "list",
    "post": "create",
})

user_detail = UserViewSet.as_view({
    "get": "retrieve",
    "put": "update",
    "patch": "partial_update",
    "delete": "destroy",
})

# Nouvelles routes
user_activate = UserViewSet.as_view({
    "patch": "activate",
})

user_deactivate = UserViewSet.as_view({
    "patch": "deactivate",
})

user_import_csv = UserViewSet.as_view({
    "post": "import_csv",
})

user_reset_password = UserViewSet.as_view({
    "patch": "reset_password",
})

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),

    path("users/", user_list, name="users"),

    path("users/<int:pk>/", user_detail, name="user-detail"),

    # Ajoute ces deux lignes
    path(
        "users/<int:pk>/activate/",
        user_activate,
        name="user-activate",
    ),

    path(
        "users/<int:pk>/deactivate/",
        user_deactivate,
        name="user-deactivate",
    ),
    path(
        "users/import_csv/",
        user_import_csv,
        name="user-import-csv",
    ),
    path(
        "users/<int:pk>/reset_password/",
        user_reset_password,
        name="user-reset-password",
    ),
]