from django.db import models
from django.conf import settings  # 추천!
# from django.conf.auth.models import User  # 비추

# Create your models here.


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 추천!
    title = models.CharField(max_length=128)
    content = models.TextField()
    # content2 = models.TextField(default=None)
    # author = models.ForeignKey(User) 		# 비추
    # author = models.ForeignKey('auth.User') # 비추
