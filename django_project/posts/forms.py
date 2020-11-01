from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Post
# 여기에 field 넣어주면 무조건 넣어야 하는 필드값으로 인식

# stackoverflow 적용

# https://stackoverflow.com/a/30403969
# required=False


# class PostForm(forms.Form):
#     class Meta:
#         model = Post
#         fields = ['title', 'brand']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'brand', 'price', 'link', 'ckcontent')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['brand'].required = True
        self.fields['price'].required = True
        self.fields['ckcontent'].required = True

# TO-DO : 아래를 위에 방식으로 변경하여 ASK 화면 만들기

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
