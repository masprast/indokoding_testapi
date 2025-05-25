from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
# from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from test_api.permissions import IsOwnerOrReadOnly

from .models import Comment, Like, Post
from .serializers import (CommentSerializer, LikeSerializer,
                          PostOwnerSerializer, PostPublicSerializer)

PostUser = get_user_model()


# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostPublicSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return PostPublicSerializer

        if self.action in ["retrieve", "update", "partial_update", "destroy"]:
            try:
                obj = self.get_object()
                if (
                    self.request.user.is_authenticated
                    and self.request.user == obj.author
                ):
                    return PostOwnerSerializer
            except Exception:
                return PostPublicSerializer

        return PostPublicSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop("partial", False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return Response(serializer.data)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        # if self.request.user.is_authenticated:
        #     return self.queryset.filter(user=self.request.user) | self.queryset.filter(
        #         user=self.kwargs["post_pk"]
        #     )
        # return self.queryset.none()
        post_pk = self.kwargs.get("post_pk")
        if post_pk:
            return Like.objects.filter(post__pk=post_pk)
        return Like.objects.all()

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_pk")
        if not post_id:
            return Response(
                {"error": "post id HARUS diisi"}, status=status.HTTP_400_BAD_REQUEST
            )
            # raise ValidationError(
            #     {"error": "Post id HARUS diisi"}, code=status.HTTP_400_BAD_REQUEST
            # )
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            # raise ValidationError(
            #     {"error": "tidak ada data"}, code=status.HTTP_404_NOT_FOUND
            # )
            return Response(
                {"error": "tidak ada data"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer.save(user=self.request.user, post=post)
        return Response(
            {"detail": f"berhasil like post {post_id}"}, status=status.HTTP_202_ACCEPTED
        )

    # def perform_destroy(self, instance):
    #     if instance.user != self.request.user:
    #         raise ValidationError(
    #             {"error": "hanya dapat diakses oleh owner"},
    #             code=status.HTTP_401_UNAUTHORIZED,
    #         )
    #     instance.delete()
    def destroy(self, request, post_pk=None, pk=None):
        # instance = self.get_object()
        # self.perform_destroy(instance)
        # return Response({"detail": "unlike berhasil"}, status=status.HTTP_202_ACCEPTED)
        if post_pk is None:
            return Response({"error": "post id HARUS diisi"})
        try:
            instance = self.get_object()
        except Like.DoesNotExist:
            return Response(
                {"error": "tidak ada data"}, status=status.HTTP_404_NOT_FOUND
            )

        self.perform_destroy(instance)
        return Response({"detail": "berhasil unlike"}, status=status.HTTP_202_ACCEPTED)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by("-created_at")
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get("post_pk")
        if post_id:
            return self.queryset.filter(post=post_id)
        return self.queryset

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_pk")
        if not post_id:
            # raise ValidationError(
            #     {"error": "Post id HARUS diisi"}, code=status.HTTP_400_BAD_REQUEST
            # )
            return Response(
                {"error": "post id HARUS diisi"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            # raise ValidationError(
            #     {"error": "tidak ada data"}, code=status.HTTP_404_NOT_FOUND
            # )
            return Response(
                {"error": "tidak ada data"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer.save(author=self.request.user, post=post)
        return Response(
            {"detail": "comment berhasil dibuat"}, status=status.HTTP_201_CREATED
        )

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            # raise ValidationError(
            #     {"error": "hanya dapat diakses oleh owner"},
            #     code=status.HTTP_401_UNAUTHORIZED,
            # )
            return Response(
                {"error": "hanya dapat diakses oleh user bersangkutan"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        instance.delete()
        return Response(
            {"detail": "berhasil hapus comment"}, status=status.HTTP_204_NO_CONTENT
        )
