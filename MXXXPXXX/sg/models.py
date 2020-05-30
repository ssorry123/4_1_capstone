from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from django.conf import settings

class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    userid = models.CharField(
        default=objects.name,
        max_length=20,
        null=True,
        unique=True
    )
    email = models.EmailField(
        max_length=255,
        unique=True
    )
    name = models.CharField(
        max_length=20,
        null=False,
        unique=True
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['email']
    def __str__(self):
        return self.name

