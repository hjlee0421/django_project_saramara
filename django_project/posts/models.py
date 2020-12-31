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

    @property
    def get_post(self):
        return self.post_set.all()

    @property
    def get_comment(self):
        return self.comment_set.all()


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # settings.py 에 AUTH_USER_MODEL 확인 추천!
    title = models.CharField(max_length=128)
    price = models.CharField(max_length=128, blank=True, null=True)
    brand = models.CharField(max_length=128, blank=True, null=True)
    link = models.CharField(
        max_length=128, blank=True, null=True)
    ckcontent = RichTextUploadingField(blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='date published')
    sara_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="sara_voter")  # [] 의 형태로 사용자를 담는다
    mara_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="mara_Voter")  # [] 의 형태로 사용자를 담는다

    view_cnt = models.IntegerField(default=0)

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

    # 함수를 속성으로 취급하게 하는 데코레이터
    @property
    def comment_cnt(self):
        return self.comment_set.all().count()

    @property
    def sara_cnt(self):
        return self.sara_users.all().count()

    @property
    def mara_cnt(self):
        return self.mara_users.all().count()

    def sara_vote(self, user):

        if user in self.sara_users.all():
            self.sara_users.remove(user)
        elif user in self.mara_users.all():
            self.mara_users.remove(user)
            self.sara_users.add(user)
        else:
            self.sara_users.add(user)

        self.save()

    def mara_vote(self, user):

        if user in self.mara_users.all():
            self.mara_users.remove(user)
        elif user in self.sara_users.all():
            self.sara_users.remove(user)
            self.mara_users.add(user)
        else:
            self.mara_users.add(user)

        self.save()

    class Meta:
        ordering = ['-id']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # or comment 도 부모가 될수있어야 대댓글 여기가 바뀌면 model view html 모두에 변화가있다.
    #
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created_date']


class ViewCount(models.Model):
    loggedin_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, default=None, null=True, on_delete=models.CASCADE)  # 게시글
    view_cnt = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)  # 조회수가 올라갔던 날짜
