# from .models import ImageUpload
from django import forms
from .models import User, Post, Comment
from ckeditor_uploader.widgets import CKEditorUploadingWidget


# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password', 'profile_image')

# # TODO : 추후에 age, gender 추가하려면 여기서 추가하고 html에서 추가하면 끝인지? (posts models 에는 age, gender 이미 있음)


class PostForm(forms.ModelForm):
    ckcontent = forms.CharField(
        widget=CKEditorUploadingWidget())
    # item_image = forms.FileField(
    #     widget=forms.ClearableFileInput(attrs={'multiple': True}))
    # images = forms.ImageField(
    # widget = forms.ClearableFileInput(attrs={'multiple': True}))
    item_image = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))
    # pub_date = forms.DateTimeField(input_formats=['%Y.%m.%d. T%H:%M'])

    class Meta:
        model = Post
        fields = ('title', 'category', 'brand', 'price',
                  'link', 'item_image', 'ckcontent')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['category'].required = True
        self.fields['brand'].required = True
        self.fields['price'].required = True
        self.fields['ckcontent'].required = True


class EditForm(forms.ModelForm):
    ckcontent = forms.CharField(
        widget=CKEditorUploadingWidget())

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
    created_date = forms.DateTimeField(input_formats=['%Y.%m.%d. T%H:%M'])
    # class Meta:
    #     model = Comment
    #     fields = ('post', 'author', 'text', 'created_date')

    #     def __init__(self, *args, **kwargs):
    #         super(CommentForm, self).__init__(*args, **kwargs)
    #         self.fields['text'].required = True
    # # TODO : CommentForm을 html에서 어떻게 사용하지?

    # class LoginForm(forms.ModelForm):
    #     class Meta:
    #         model = User
    #         fields = ['username', 'password']


class UploadFileForm(forms.Form):
    class Meta:
        model = User
        fields = ['profile_image']
        # file = forms.FileField()


class UserForm(forms.ModelForm):
    profile_image = forms.ImageField(
        widget=forms.FileInput(attrs={"id": "image", 'multiple': True}))

    class Meta:
        model = User  # 여기만 바꿈 원래 ImageUpload
        fields = [
            'profile_image',
        ]


class ImageUploadForm(forms.Form):
    images = forms.ImageField()


class FileFieldForm(forms.Form):
    item_image = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))
