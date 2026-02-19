from accounts.views import CustomUserRegistrationView, LoginView, CookieTokenRefreshView,LogoutView
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("user_register/", CustomUserRegistrationView, basename="user_register")
urlpatterns = [
    path("api/", include(router.urls)),
    path("login/", LoginView.as_view()),
    path("refresh-token/", CookieTokenRefreshView.as_view(), name="token-refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
