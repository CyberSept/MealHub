from django.db import models
from django.contrib.auth.models import AbstractUser, User


class UserModel(AbstractUser):

    def __str__(self):
        return self.username
