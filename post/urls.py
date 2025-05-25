from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, LikeViewSet, PostViewSet

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "<int:post_pk>/comments/",
        CommentViewSet.as_view({"get": "list", "post": "create"}),
    ),
    path(
        "<int:post_pk>/comments/<int:pk>",
        CommentViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
    path(
        "<int:post_pk>/likes/", LikeViewSet.as_view({"get": "list", "post": "create"})
    ),
    path(
        "<int:post_pk>/likes/<int:pk>/",
        LikeViewSet.as_view({"get": "retrieve", "delete": "destroy"}),
    ),
    path(
        "<int:post_pk>/comments/<int:pk>",
        LikeViewSet.as_view(
            {
                "get": "retrieve",
                "delete": "destroy",
            }
        ),
    ),
]
