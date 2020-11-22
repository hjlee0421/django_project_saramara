from rest_framework import serializers
from .models import User, Post, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'gender', 'age')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'price', 'brand', 'link', 'pub_date', 'sara',
                  'mara', 'sara_cnt', 'mara_cnt', 'comment_cnt', 'view_cnt', 'ckcontent', 'category')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'text', 'created_date')
