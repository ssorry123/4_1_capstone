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

class Writing(models.Model):
    title = models.CharField(max_length=100, verbose_name='기사 제목')
    pub_date = models.DateTimeField(default=timezone.now, verbose_name='작성일')
    scrap = models.IntegerField(default=0, verbose_name='스크랩 수')
    text = models.CharField(max_length=1000, verbose_name='기사 내용')
    #photo = models.ImageField(blank=True, upload_to="image", verbose_name='사진')
    #저장할지 url만 저장할지 몰라서 일단 주석처리
    def __str__(self):
        return self.title