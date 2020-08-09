from django.db import models
from django.conf import settings  # 추천!
# from django.conf.auth.models import User  # 비추
from django.utils import timezone
from datetime import datetime

# Create your models here.


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 추천!
    title = models.CharField(max_length=128)
    content = models.TextField()
    price = models.CharField(max_length=128, default='NA', null=True)
    brand = models.CharField(max_length=128, default='NA', null=True)
    link = models.CharField(max_length=128, default='NA', null=True)
    pup_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='date published')
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


class Choice(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200, default=["사라", "마라"])
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
