# courses/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.course_list, name='course_list'),
    path('course/<slug:slug>/', views.course_detail, name='course_detail'),
    path('category/<slug:slug>/', views.category_courses, name='category_courses'),
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('my-courses/', views.my_courses, name='my_courses'),
]