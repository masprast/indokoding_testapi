# from datetime import datetime

# from django.contrib.auth import authenticate, get_user_model
# from rest_framework import serializers, status
# # from rest_framework.authtoken.models import Token
# from rest_framework.exceptions import ValidationError
# from rest_framework_simplejwt.tokens import RefreshToken

# from blog.models import Posts

# # from .models import User
# User = get_user_model()


# class UserSerializer(serializers.ModelSerializer):
#     queryset = User.objects.all()
#     post = serializers.SerializerMethodField(read_only=True)
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ["id", "username", "password", "email", "post"]

#     def get_post(self, obj):
#         return Posts.objects.filter(author_id=obj.id).values_list("title", flat=True)


# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField(label="Username", write_only=True)
#     password = serializers.CharField(
#         label="Password",
#         style={"input_type": "password"},
#         write_only=True,
#         trim_whitespace=False,
#     )

#     def validate(self, attr):
#         username = attr.get("username")
#         password = attr.get("password")

#         if username and password:
#             user = authenticate(
#                 request=self.context.get("request"),
#                 username=username,
#                 password=password,
#             )
#             if user:
#                 # token, created = Token.objects.get_or_create(user=user)
#                 refresh = RefreshToken.for_user(user)
#                 # access=AccessToken.for_user(user)
#                 token = {"refresh": str(refresh), "access": str(refresh.access_token)}
#             else:
#                 msg = "Username atau password salah"
#                 raise ValidationError({"error": msg}, code=status.HTTP_401_UNAUTHORIZED)
#         else:
#             msg = '"Username" dan "Password" HARUS diisi.'
#             raise ValidationError({"error": msg}, code=status.HTTP_400_BAD_REQUEST)
#         attr["user"] = user
#         attr["token"] = token
#         attr["logged_in"] = datetime.now()
#         return attr


from django.contrib.auth import get_user_model
from rest_framework import serializers

from post.models import Comment, Like, Post

PostUser = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostUser
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "date_joined",
        ]
        read_only_fields = ["is_staff", "is_active", "date_joined"]


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = PostUser
        fields = ["username", "email", "password", "first_name", "last_name"]

    def create(self, validated_data):
        user = PostUser.objects.create_user(**validated_data)
        return user


class UserProfilePublicPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "created_at"]


class UserProfilePublicSerializer(serializers.ModelSerializer):
    posts = UserProfilePublicPostSerializer(many=True, read_only=True)

    class Meta:
        model = PostUser
        fields = ["id", "username", "first_name", "last_name", "date_joined", "posts"]
        read_only_fields = fields


class UserProfileAdminCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "content", "post", "created_at"]


class UserProfileAdminLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ["id", "post", "created_at"]


class UserProfileAdminSerializer(serializers.ModelSerializer):
    posts = UserProfilePublicPostSerializer(many=True, read_only=True)
    comments = UserProfileAdminCommentSerializer(many=True, read_only=True)
    likes = UserProfileAdminLikeSerializer(many=True, read_only=True)

    class Meta:
        model = PostUser
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "date_joined",
            "is_active",
            "is_staff",
            "posts",
            "comments",
            "likes",
        ]
        read_only_fields = fields
