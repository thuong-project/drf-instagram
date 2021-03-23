from django.contrib.auth.models import AbstractUser
from django.db import models

from .helper import user_directory_path


class User(AbstractUser):
    address = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to=user_directory_path, blank=True)
