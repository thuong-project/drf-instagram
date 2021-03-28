from django.db import models

from users.models import User


class Post(models.Model):
    content = models.TextField(blank=True, max_length=2000)
    number_of_comments = models.PositiveIntegerField(default=0, editable=False)
    number_of_likes = models.PositiveIntegerField(default=0, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True)
