import django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import validators


# Create your models here.


class User(AbstractUser):
    username = models.CharField(error_messages={'unique': 'A user with that username already exists.'},
                                help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                                max_length=150,
                                unique=True,
                                validators=[validators.UnicodeUsernameValidator()],
                                verbose_name='username',

                                )


class UserProfile(models.Model):
    address = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
