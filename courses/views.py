# courses/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Category, Lesson, Enrollment
from django.db.models import Q

def home(request):
    featured_courses = Course.objects.filter(is_featured=True, is_active=True)[:6]
    recent_courses = Course.objects.filter(is_active=True).order_by('-created_at')[:6]
    
    context = {
        'featured_courses': featured_courses,
        'recent_courses': recent_courses,
    }
    return render(request, 'courses/home.html', context)

def course_list(request):
    courses = Course.objects.filter(is_active=True)
    categories = Category.objects.all()
    
    # Filtrage par catégorie
    category_slug = request.GET.get('category')
    if category_slug:
        courses = courses.filter(category__slug=category_slug)
    
    # Filtrage par niveau
    level = request.GET.get('level')
    if level:
        courses = courses.filter(level=level)
    
    # Recherche
    query = request.GET.get('q')
    if query:
        courses = courses.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    context = {
        'courses': courses,
        'categories': categories,
    }
    return render(request, 'courses/course_list.html', context)

def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_active=True)
    lessons = course.lessons.all().order_by('order')
    
    # Vérifier si l'utilisateur est inscrit
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    
    context = {
        'course': course,
        'lessons': lessons,
        'is_enrolled': is_enrolled,
    }
    return render(request, 'courses/course_detail.html', context)

def category_courses(request, slug):
    category = get_object_or_404(Category, slug=slug)
    courses = Course.objects.filter(category=category, is_active=True)
    
    context = {
        'category': category,
        'courses': courses,
    }
    return render(request, 'courses/category_courses.html', context)

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, is_active=True)
    
    # Vérifier si l'utilisateur est déjà inscrit
    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user,
        course=course
    )
    
    if created:
        course.students_count += 1
        course.save()
    
    return redirect('my_courses')

@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(student=request.user)
    
    context = {
        'enrollments': enrollments,
    }
    return render(request, 'courses/my_courses.html', context)

@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course = lesson.course
    
    # Vérifier si l'utilisateur est inscrit au cours
    enrollment = Enrollment.objects.filter(student=request.user, course=course).first()
    if not enrollment:
        return redirect('course_detail', slug=course.slug)
    
    # Marquer la leçon comme complétée si ce n'est pas déjà fait
    if lesson not in enrollment.completed_lessons.all():
        enrollment.completed_lessons.add(lesson)
        # Calculer le progrès
        total_lessons = course.lessons.count()
        completed_lessons = enrollment.completed_lessons.count()
        enrollment.progress = int((completed_lessons / total_lessons) * 100)
        enrollment.save()
    
    # Récupérer les leçons précédentes et suivantes
    lessons = list(course.lessons.all().order_by('order'))
    current_index = lessons.index(lesson)
    previous_lesson = lessons[current_index - 1] if current_index > 0 else None
    next_lesson = lessons[current_index + 1] if current_index < len(lessons) - 1 else None
    
    context = {
        'lesson': lesson,
        'course': course,
        'previous_lesson': previous_lesson,
        'next_lesson': next_lesson,
        'enrollment': enrollment,
    }
    return render(request, 'courses/lesson_detail.html', context)