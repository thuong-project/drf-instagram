from django.contrib.auth.models import AbstractUser
from django.db import models
from .helper import user_directory_path


class User(AbstractUser):
    avatar = models.ImageField(upload_to=user_directory_path, blank=True)

