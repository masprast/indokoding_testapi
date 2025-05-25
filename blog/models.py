# from django.contrib.auth import get_user_model
# from django.db import models

# User = get_user_model()


# # Create your models here.
# class Posts(models.Model):
#     title = models.CharField(max_length=80)
#     content = models.TextField()
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     # likes = models.ManyToManyField(User, related_name="liked_post", blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = "Posts"
#         verbose_name = "Post"
#         ordering = ["-created_at"]
#         # lookup_fields =['created_at']

#     def __str__(self):
#         return self.title

#     def number_of_likes(self):
#         return self.likes.count()


# class Likes(models.Model):
#     liked_by = models.ForeignKey(User, on_delete=models.CASCADE)
#     post = models.ForeignKey(Posts, on_delete=models.CASCADE)

#     class Meta:
#         verbose_name = "Like"


# class Comments(models.Model):
#     author = models.CharField(max_length=60)
#     body = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     post = models.ForeignKey(Posts, on_delete=models.CASCADE)

#     class Meta:
#         verbose_name = "Comment"

#     def __str__(self):
#         return f"{self.author} on '{self.post}'"
