from django.db import models

# Create your models here.
from posts.models import Post
from users.models import User


class Comment(models.Model):
    content = models.TextField(max_length=2000, blank=True)
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('Comment', null=True, on_delete=models.CASCADE)
    number_of_comments = models.PositiveIntegerField(default=0, editable=False)
    number_of_likes = models.PositiveIntegerField(default=0, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)