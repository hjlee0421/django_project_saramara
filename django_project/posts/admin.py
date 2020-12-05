from django.contrib import admin
from .models import User, Post, Comment, ViewCount


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'kakao_unique_id',
                    'gender', 'birthyear', 'birthday', 'email',)
    list_filter = ('username',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title')
    list_filter = ('title',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'text', 'created_date')
    list_filter = ('post',)


class ViewCountAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'post', 'view_cnt', 'date')
    list_filter = ('post',)


admin.site.register(Post, PostAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ViewCount, ViewCountAdmin)
