from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Post, User  # Choice,

# Register your models here.


# class ChoiceInline(admin.TabularInline):
#     model = Choice
#     extra = 2


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title')
    list_filter = ('title',)
    # inlines = [ChoiceInline]


admin.site.register(Post, PostAdmin)
admin.site.register(User, UserAdmin)

# js 대신에 기본 DJANGO 기능으로 해결 가능
