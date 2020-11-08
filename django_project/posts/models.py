from django.db import models
from django.conf import settings  # 추천!
# from django.conf.auth.models import User  # 비추
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import AbstractUser

from ckeditor.fields import RichTextField


# class User(AbstractUser):
# class Post(models.Model):
# class User(AbstractUser):


# User 가 posts model꺼를 사용함
# TODO : Views 에 def/class 만들어서 detail 페이지에서 댓글 submit 하면 아래방식으로 저장해야 함

'''
In [15]: from posts.models import Post, Comment, User

In [16]: User.objects.all()
Out[16]: <QuerySet [<User: hjlee0421>, <User: testtesttest>]>

In [17]: User.objects.first()
Out[17]: <User: hjlee0421>

In [18]: user = User.objects.first()

In [19]: post
Out[19]: <Post: 테스트2>

In [20]: comment = Comment(post=post, author=user, text='comment text')

In [21]: comment.save()

In [22]: post.comment_set.all()
Out[22]: <QuerySet [<Comment: Comment object (1)>]>

In [23]: comment = Comment(post=post, author=user, text='comment text2')

In [24]: comment.save()

In [25]: post.comment_set.all()
Out[25]: <QuerySet [<Comment: Comment object (1)>, <Comment: Comment object (2)>]>

In [26]: 

In [26]: exit
'''


class User(AbstractUser):
    gender = models.IntegerField(default=0)
    age = models.IntegerField(default=0)


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
    ckcontent = RichTextField(blank=True, null=True)

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
