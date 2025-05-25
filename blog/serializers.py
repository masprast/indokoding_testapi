# from datetime import datetime

# from rest_framework import serializers

# from .models import Comments, Likes, Posts


# class PostSerializer(serializers.ModelSerializer):
#     author = serializers.ReadOnlyField(source="author.username")
#     # author_id = serializers.ReadOnlyField(source="author.id")
#     likes = serializers.SerializerMethodField(read_only=True)
#     comments = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = Posts
#         fields = [
#             "id",
#             "title",
#             "created_at",
#             "author",
#             # "author_id",
#             "content",
#             "comments",
#             "likes",
#         ]

#     def update(self, instance, validated_data):
#         instance.title = validated_data.get("title", instance.title)
#         instance.content = validated_data.get("content", instance.content)
#         instance.updated_at = datetime.now()
#         instance.save()
#         return instance

#     def get_comments(self, post):
#         return Comments.objects.filter(post=post).count()

#     def get_likes(self, post):
#         return Likes.objects.filter(post=post).count()


# class LikeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Likes
#         fields = "__all__"

#     def get_post(self, likes):
#         return Posts.objects.filter(author=self.request.user)


# class CommentSerializer(serializers.ModelSerializer):
#     author = serializers.ReadOnlyField(source="author.username")
#     body = serializers.CharField(write_only=True)
#     post = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = Comments
#         fields = ["author", "post", "body"]

#     def get_post(self, comment):
#         return Posts.objects.filter(author=self.request.user)
