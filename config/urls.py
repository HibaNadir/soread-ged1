from django.http import HttpResponse
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
urlpatterns = [

    path("admin/", admin.site.urls),

    path("api/accounts/", include("accounts.urls")),

    path("api/", include("folders.urls")),

    path("api/", include("documents.urls")),
    path("api/", include("spaces.urls")),

    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),

    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),

    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",),
    path('', lambda request: HttpResponse("Bienvenue sur SOREAD GED")),
    
    path("api/", include("notifications.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)