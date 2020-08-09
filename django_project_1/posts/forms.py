from django import forms


class PostForm(forms.Form):
    title = forms.CharField(
        error_messages={'required': '제목을 입력하세요'}, max_length=128, label='제목')
    brand = forms.CharField(
        error_messages={'required': '브랜드를 입력하세요'}, max_length=128, label='브랜드')
    price = forms.CharField(
        error_messages={'required': '가격을 입력하세요'}, max_length=128, label='가격')
    link = forms.CharField(max_length=128, label='링크')
    content = forms.CharField(
        error_messages={'required': '내용을 입력하세요'}, widget=forms.Textarea, label='내용')
