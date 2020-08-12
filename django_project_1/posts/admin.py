from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Post, Choice, User

# Register your models here.


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title')
    inlines = [ChoiceInline]


admin.site.register(Post, PostAdmin)
admin.site.register(User, UserAdmin)
