from django import forms

# 여기에 field 넣어주면 무조건 넣어야 하는 필드값으로 인식

# stackoverflow 적용

# https://stackoverflow.com/a/30403969
# required=False


class PostForm(forms.Form):
    title = forms.CharField(
        error_messages={'required': '제목을 입력하세요'}, max_length=128, label='제목')
    brand = forms.CharField(
        error_messages={'required': '브랜드를 입력하세요'}, max_length=128, label='브랜드')
    price = forms.CharField(
        error_messages={'required': '가격을 입력하세요'}, max_length=128, label='가격')
    link = forms.CharField(max_length=128, label='링크', required=False)
    content = forms.CharField(
        error_messages={'required': '내용을 입력하세요'}, widget=forms.Textarea, label='내용')
