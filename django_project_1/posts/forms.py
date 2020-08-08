from django import forms


class PostForm(forms.Form):
    title = forms.CharField(
        error_messages={'required': '제목을 입력하세요'}, max_length=128)
    content = forms.CharField(
        error_messages={'required': '제목을 입력하세요'}, widget=forms.Textarea)
