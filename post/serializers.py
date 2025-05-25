from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

from .models import Comment, Like, Post


class LikeSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Like
        fields = ["id", "user", "post", "created_at"]
        read_only_fields = ["user", "post", "created_at"]

    def create(self, validated_data):
        post_pk = self.context["view"].kwargs.get("post_pk")
        if not post_pk:
            raise ValidationError(
                {"error": "Post id HARUS diisi"}, code=status.HTTP_400_BAD_REQUEST
            )
        try:
            post = Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            raise ValidationError(
                {"error": "tidak ada data"}, code=status.HTTP_404_NOT_FOUND
            )

        if Like.objects.filter(post=post, user=self.context["request"].user).exists():
            raise ValidationError(
                {"error": "postingan sudah di-like"}, code=status.HTTP_400_BAD_REQUEST
            )

        validated_data.pop("post", None)
        validated_data.pop("user", None)
        return Like.objects.create(
            post=post, user=self.context["request"].user, **validated_data
        )


class CommentSerializer(serializers.ModelSerializer):
    # author = UserSerializer(read_only=True)
    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "post", "author", "content", "created_at", "updated_at"]
        read_only_fields = ["author", "post", "created_at", "updated_at"]

    def create(self, validated_data):

        post_pk = self.context["view"].kwargs.get("post_pk")
        if not post_pk:
            raise ValidationError(
                {"error": "Post id HARUS diisi"}, code=status.HTTP_400_BAD_REQUEST
            )
        try:
            post = Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            raise ValidationError(
                {"error": "tidak ada data"}, code=status.HTTP_404_NOT_FOUND
            )

        validated_data.pop("post", None)
        validated_data.pop("author", None)

        return Comment.objects.create(
            post=post, author=self.context["request"].user, **validated_data
        )


class CommentForPostOwnerSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "author", "content", "created_at", "updated_at"]
        read_only_fields = ["author", "created_at", "updated_at"]


class PostPublicSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "author",
            "comments_count",
            "likes_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "author",
            "comments_count",
            "likes_count",
            "created_at",
            "updated_at",
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()


class PostOwnerSerializer(serializers.ModelSerializer):
    liked_by = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "author",
            "comments",
            "liked_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "author",
            "comments",
            "liked_by",
            "created_at",
            "updated_at",
        ]

    def get_liked_by(self, obj):
        return [like.user.username for like in obj.likes.select_related("user")]

    def get_comments(self, obj):
        comments_queryset = (
            obj.comments.all().select_related("author").order_by("-created_at")
        )
        return CommentForPostOwnerSerializer(
            comments_queryset, many=True, context=self.context
        ).data


