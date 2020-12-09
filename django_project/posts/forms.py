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
        self.fields['category'].required = True
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
# TODO : CommentForm을 html에서 어떻게 사용하지?


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
