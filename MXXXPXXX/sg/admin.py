from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Article, User
# Register your models here.
admin.site.register(Article)
admin.site.register(User, UserAdmin)