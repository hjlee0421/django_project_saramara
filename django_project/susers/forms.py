from django import forms
from django.contrib.auth.models import User
from posts.models import User


# class UserForm(forms.ModelForm):

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']

# # TODO : 추후에 age, gender 추가하려면 여기서 추가하고 html에서 추가하면 끝인지? (posts models 에는 age, gender 이미 있음)


# class LoginForm(forms.ModelForm):

#     class Meta:
#         model = User
#         fields = ['username', 'password']
