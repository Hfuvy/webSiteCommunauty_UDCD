# communaute/admin.py
from django.contrib import admin
from .models import Post, Comment, UserProfile

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'post_type', 'course', 'created_at', 'is_pinned')
    list_filter = ('post_type', 'course', 'is_pinned', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('author__username', 'post__title', 'content')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_title')
    search_fields = ('user__username', 'bio', 'skills')