from django import forms
from .models import User, Post, Comment
from ckeditor.widgets import CKEditorWidget


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

# TODO : 추후에 age, gender 추가하려면 여기서 추가하고 html에서 추가하면 끝인지? (posts models 에는 age, gender 이미 있음)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category', 'brand', 'price', 'link', 'ckcontent')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['title'].required = True
        self.fields['brand'].required = True
        self.fields['price'].required = True
        self.fields['ckcontent'].required = True


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('post', 'author', 'text', 'created_date')

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].required = True
# TOOD : CommentForm을 html에서 어떻게 사용하지?


# ??

class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password']


# 여기에 field 넣어주면 무조건 넣어야 하는 필드값으로 인식

# stackoverflow 적용

# https://stackoverflow.com/a/30403969
# required=False


# class PostForm(forms.Form):
#     class Meta:
#         model = Post
#         fields = ['title', 'brand']


# 아래는 구버전

# class PostForm(forms.Form):
#     title = forms.CharField(
#         error_messages={'required': '제목을 입력하세요'}, max_length=128, label='제목')
#     brand = forms.CharField(
#         error_messages={'required': '브랜드를 입력하세요'}, max_length=128, label='브랜드')
#     price = forms.CharField(
#         error_messages={'required': '가격을 입력하세요'}, max_length=128, label='가격')
#     link = forms.CharField(max_length=128, label='링크', required=False)
#     content = forms.CharField(
#         error_messages={'required': '내용을 입력하세요'}, widget=forms.Textarea, label='내용')
#     ckcontent = forms.CharField(widget=CKEditorWidget())
