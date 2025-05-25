import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODLUE", "test_api.settings")
django.setup()

from post.models import Comment, Like, Post
from user.models import PostUser

print("-- Memulai proses seeding data --")

data = [
    {"user": "rokhayati", "password": "password"},
    {"user": "marjuki", "password": "qwertyuiop"},
    {"user": "bejo", "password": "qwasxz"},
]
for user in data:
    user_created, created = PostUser.objects.get_or_create(
        username=user.user,
        defaults={"email": str(user.user + "@email.org"), "password": user.password},
    )
    if created:
        user_created.set_password(user.password)
        user_created.save()
        print(f"user {user.user} created")
    else:
        print(f"user {user.user} sudah ada")

post1, created = Post.objects.get_or_create(
    title="Dockerizing django",
    content="skrip ini berjalan di dalam docker container",
    author=PostUser.objects.get(pk=1),
)
if created:
    print(f"post {post1.title} oleh {post1.author} berhasil dibuat")
else:
    print(f"post {post1.title} oleh {post1.author} sudah ada")

coment1, created = Comment.objects.get_or_create(
    content="joss", author=PostUser.objects.get(pk=2), post=post1
)
if created:
    print(
        f"comment oleh {coment1.author.username} untuk post {coment1.post.title} berhasil dibuat"
    )
else:
    print(
        f"comment oleh {coment1.author.username} untuk post {coment1.post.title} sudah ada"
    )

like1, created = Like.objects.get_or_create(user=PostUser.objects.get(pk=3), post=post1)
if created:
    print(f"postingan oleh {like1.post.author.username} berhasil disukai")
else:
    print(f"postingan oleh {like1.post.author.username} sudah disukasi")

print("-- Proses seeding data selesai--")

exit()
