# from django.contrib.auth import get_user_model
# from rest_framework import generics, mixins, permissions, status
# from rest_framework.exceptions import ValidationError
# from rest_framework.response import Response

# from .models import Comments, Likes, Posts
# from .serializers import CommentSerializer, LikeSerializer, PostSerializer

# User = get_user_model()


# # Create your views here.
# class GetPostList(generics.ListCreateAPIView):
#     queryset = Posts.objects.all().order_by("-id")
#     serializer_class = PostSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)


# class UpdatePost(generics.RetrieveUpdateAPIView):
#     serializer_class = PostSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#     def get_queryset(self):
#         id = self.kwargs["pk"]
#         obj = Posts.objects.filter(pk=id)
#         return obj

#     def put(self, request, *args, **kwargs):
#         obj = self.get_queryset()
#         if obj.exists() and obj.first().author == request.user:
#             return self.update(request, *args, **kwargs)
#         else:
#             raise ValidationError(
#                 "Tidak dapat mengubah postingan user lain",
#                 code=status.HTTP_401_UNAUTHORIZED,
#             )


# class PostDestroy(generics.RetrieveDestroyAPIView):
#     queryset = Posts.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def delete(self, request, *args, **kwargs):
#         post = Posts.objects.filter(pk=kwargs["pk"], author=self.request.user)
#         if post.exists():
#             return self.destroy(request, *args, **kwargs)
#         else:
#             raise ValidationError(
#                 "Tidak dapat menghapus postingan user lain",
#                 code=status.HTTP_401_UNAUTHORIZED,
#             )


# class LikesCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
#     serializer_class = LikeSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#     def get_queryset(self):
#         user = self.request.user
#         post = Posts.objects.get(pk=self.kwargs["pk"])
#         return Likes.objects.filter(liked_by=user, post=post)

#     def perform_create(self, serializer):
#         if self.get_queryset().exists():
#             raise ValidationError(
#                 "Post telah disukai", code=status.HTTP_401_UNAUTHORIZED
#             )
#         serializer.save(
#             liked_by=self.request.user, post=Posts.objects.get(pk=self.kwargs["pk"])
#         )

#     def perform_destroy(self, request, *args, **kwargs):
#         if self.get_queryset().exists():
#             self.get_queryset().delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         else:
#             raise ValidationError("Tidak ada data.", code=status.HTTP_404_NOT_FOUND)


# class CommentCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
#     serializer_class = CommentSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         comment = Comments.objects.filter(author=user)
#         return comment

#     def perform_create(self, serializer):
#         print(self.request.data)
#         if self.get_queryset().exists():
#             raise ValidationError("Comment sudah ada", code=status.HTTP_400_BAD_REQUEST)
#         serializer.save(
#             author=self.request.user,
#             post=Posts.objects.get(pk=self.kwargs["pk"]),
#             body=self.request.data,
#         )
#         return Response(
#             {"detail": "Comment berhasil dibuat"}, status=status.HTTP_201_CREATED
#         )

#     def perform_destroy(self, request, *args, **kwargs):
#         if self.get_queryset().exists():
#             self.get_queryset().delete()
#             return Response(
#                 data={"pesan": "comment telah dihapus"}, status=status.HTTP_200_OK
#             )
#         else:
#             # raise ValidationError("Tidak ada data", code=status.HTTP_404_NOT_FOUND)
#             return Response(
#                 {"error": "tidak ada data"}, status=status.HTTP_404_NOT_FOUND
#             )
