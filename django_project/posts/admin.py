from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Post, User, Comment

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title')
    list_filter = ('title',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'text')
    list_filter = ('post',)


admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)


# js 대신에 기본 DJANGO 기능으로 해결 가능
