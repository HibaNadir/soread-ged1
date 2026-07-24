from django.urls import path
from .views import EmailOrUsernameTokenView, ProfileView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("token/", EmailOrUsernameTokenView.as_view(), name="account-token"),
    path("me/", ProfileView.as_view(), name="profile"),
]