from django.db import models

# Create your models here.
from comments.models import Comment
from posts.models import Post


class Image(models.Model):
    def directory_path(img, filename):
        return f"images/{filename}"

    image = models.ImageField(upload_to=directory_path)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
