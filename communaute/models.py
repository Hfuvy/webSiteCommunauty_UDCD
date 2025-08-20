# communaute/models.py
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    POST_TYPES = (
        ('question', 'Question'),
        ('discussion', 'Discussion'),
        ('resource', 'Ressource'),
    )
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    post_type = models.CharField(max_length=20, choices=POST_TYPES, default='discussion')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, blank=True, null=True, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    views = models.PositiveIntegerField(default=0)
    is_pinned = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    website = models.URLField(blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    skills = models.CharField(max_length=200, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"Profile of {self.user.username}"