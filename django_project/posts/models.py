from django.db import models
# Build user defined "User" Model
from django.contrib.auth.models import AbstractUser
from django.conf import settings  # Foreign Key
from datetime import datetime
from django.utils import timezone
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# class User(AbstractUser):
# class Post(models.Model):
# class Comment(models.Model):


class User(AbstractUser):
    gender = models.IntegerField(default=0)
    age = models.IntegerField(default=0)
    # kakao_account
    # email
    # - email : ####@###.com (string)
    # birthday
    # - birthday : MMDD (string)
    # birthyear
    # - birthyear : YYYY (string)
    # gender
    # - gender : female/male (string)


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 추천!
    # author = models.ForeignKey(User) 		# 비추
    # author = models.ForeignKey('auth.User') # 비추
    title = models.CharField(max_length=128)
    # content = models.TextField()
    price = models.CharField(max_length=128, blank=True,  null=True)
    brand = models.CharField(max_length=128, blank=True,  null=True)
    link = models.CharField(
        max_length=128, blank=True, null=True)
    pup_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='date published')
    # blank = ui에서 빈칸 from valid check, null 은 db에서 빈값을 받는 개념
    sara = models.TextField(blank=True, null=True)
    mara = models.TextField(blank=True, null=True)
    sara_cnt = models.IntegerField(default=0)
    mara_cnt = models.IntegerField(default=0)
    ckcontent = RichTextUploadingField(blank=True, null=True)

    CATEGORY_CHOICES = (
        ('상의', '상의'),
        ('하의', '하의'),
        ('신발', '신발'),
        ('기타', '기타'),
    )
    category = models.CharField(
        max_length=128, choices=CATEGORY_CHOICES, default='상의', null=False)
    # category = 정해진 카테고리에서 선택하게끔

    def __str__(self):
        return self.title

    def was_published_recently(self):
        return self.pup_date <= timezone.now() - datetime.timedelta(days=1)

    class Meta:
        ordering = ['-id']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_date']
