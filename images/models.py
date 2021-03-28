from django.db import models

# Create your models here.
from posts.models import Post


class Image(models.Model):
    def directory_path(img, filename):
        return f"user_{img.post.user.id}/posts/{img.post.id}/images/{filename}"

    image = models.ImageField(upload_to=directory_path)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    #comment = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True)
