from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from .views import (UserProfileAdminView, UserProfilePublicVew,
                    UserRegisterView, UserViewSet)

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
urlpatterns = [
    path("", include(router.urls)),
    path(
        "profile/<str:username>/", UserProfilePublicVew.as_view(), name="user_profile"
    ),
    path(
        "admin/profile/<str:username>/",
        UserProfileAdminView.as_view(),
        name="user_profile_admin",
    ),
    path("register/", UserRegisterView.as_view(), name="register"),
    path(
        "login/",
        TokenObtainPairView.as_view(),
        name="login",
    ),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
