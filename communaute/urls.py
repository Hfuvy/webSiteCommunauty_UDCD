# communaute/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.community_home, name='community_home'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('new-post/', views.create_post, name='create_post'),
    path('edit-post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('like-post/<int:post_id>/', views.like_post, name='like_post'),
    path('add-comment/<int:post_id>/', views.add_comment, name='add_comment'),
]