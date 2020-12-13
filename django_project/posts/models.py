from random import randint
from django.db import models
from datetime import datetime
from django.conf import settings  # Foreign Key
from django.utils import timezone
from django.contrib.auth.models import AbstractUser  # user defined "User" Model

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class User(AbstractUser):
    # age = models.IntegerField(default=0)
    kakao_unique_id = models.CharField(
        max_length=128, blank=True, null=True, default="")
    kakao_access_token = models.CharField(
        max_length=128, blank=True, null=True, default="")
    profile_image = models.ImageField(
        blank=True, null=True, upload_to='profile_image', default="C:\django_project\django_project\media\profile_image\saramara_defaults.jpg")

    gender = models.CharField(
        max_length=128, blank=True, null=True, default="")
    email = models.EmailField(
        max_length=128, blank=True, null=True, default="")
    birthday = models.CharField(
        max_length=128, blank=True, null=True, default="0101")
    birthyear = models.CharField(
        max_length=128, blank=True, null=True, default=str(randint(1950, 2010)))
# blank = ui에서 빈칸 from valid check, null 은 db에서 빈값을 받는 개념


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # settings.py 에 AUTH_USER_MODEL 확인 추천!

    title = models.CharField(max_length=128)
    price = models.CharField(max_length=128, blank=True, null=True)
    brand = models.CharField(max_length=128, blank=True, null=True)
    link = models.CharField(
        max_length=128, blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='date published')
    sara = models.TextField(blank=True, null=True)
    mara = models.TextField(blank=True, null=True)
    # sara mara 는 모델을 many to many 로 변경해야 함
    sara_cnt = models.IntegerField(default=0)
    mara_cnt = models.IntegerField(default=0)
    comment_cnt = models.IntegerField(default=0)
    view_cnt = models.IntegerField(default=0)
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
        return self.pub_date <= timezone.now() - datetime.timedelta(days=1)

    class Meta:
        ordering = ['-id']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created_date']


# Models.py
# 게시글 조회 기록 저장
# HitCount 활용
class ViewCount(models.Model):
    # TODO: author 가 아니라 session 에 로그인 된 유저를 기준으로 정리 해야 함
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, default=None, null=True, on_delete=models.CASCADE)  # 게시글
    view_cnt = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)  # 조회수가 올라갔던 날짜
