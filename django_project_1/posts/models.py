from django.db import models
from django.conf import settings  # 추천!
# from django.conf.auth.models import User  # 비추
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    age = models.IntegerField(default=0)
    gender = models.IntegerField(default=0)


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 추천!
    title = models.CharField(max_length=128)
    content = models.TextField()
    price = models.CharField(max_length=128, default='NA', null=True)
    brand = models.CharField(max_length=128, default='NA', null=True)
    link = models.CharField(
        max_length=128, blank=True, null=True)
    pup_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='date published')
    # blank = ui에서 빈칸 from valid check, null 은 db에서 빈값을 받는 개념
    sara = models.TextField(blank=True, null=True)
    mara = models.TextField(blank=True, null=True)

    CATEGORY_CHOICES = (
        ('상의', '상의'),
        ('하의', '하의'),
        ('신발', '신발'),
        ('기타', '기타'),
    )
    category = models.CharField(
        max_length=128, choices=CATEGORY_CHOICES, default='상의', null=False)
    # image = models.ImageField(??) 사진 갯수 제한?
    # category = 정해진 카테고리에서 선택하게끔
    # content2 = models.TextField(default=None)
    # author = models.ForeignKey(User) 		# 비추
    # author = models.ForeignKey('auth.User') # 비추

    def __str__(self):
        return self.title

    def was_published_recently(self):
        return self.pup_date <= timezone.now() - datetime.timedelta(days=1)

    def sara_cnt(self):
        if self.sara is None:
            return 0
        else:
            return len(self.sara.split(' '))

    def mara_cnt(self):
        if self.mara is None:
            return 0
        else:
            return len(self.mara.split(' '))

    class Meta:
        ordering = ['-id']


class Choice(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    SARAMARA_CHOICES = (
        ('사라', '사라'),
        ('마라', '마라'),
    )
    choice_text = models.CharField(
        max_length=128, choices=SARAMARA_CHOICES, default='사라', null=False)
    # choice_text = models.CharField(max_length=200, default=["사라", "마라"])
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
