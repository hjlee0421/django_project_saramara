from django.contrib import admin
from .models import Post, Choice

# Register your models here.


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title')
    inlines = [ChoiceInline]


admin.site.register(Post, PostAdmin)
