from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    avatar = models.ImageField(blank=True, upload_to="accounts/avatar")
