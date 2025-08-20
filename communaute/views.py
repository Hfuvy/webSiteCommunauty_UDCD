# communaute/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Comment
from .forms import PostForm, CommentForm

def community_home(request):
    posts = Post.objects.all().order_by('-created_at')
    
    # Filtrer par type de post
    post_type = request.GET.get('type')
    if post_type:
        posts = posts.filter(post_type=post_type)
    
    # Filtrer par cours
    course_id = request.GET.get('course')
    if course_id:
        posts = posts.filter(course_id=course_id)
    
    context = {
        'posts': posts,
    }
    return render(request, 'communaute/community_home.html', context)

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Incrémenter le compteur de vues
    post.views += 1
    post.save()
    
    # Gestion des commentaires
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    
    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'communaute/post_detail.html', context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Votre publication a été créée avec succès!')
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm()
    
    context = {
        'form': form,
    }
    return render(request, 'communaute/create_post.html', context)

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre publication a été modifiée avec succès!')
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    
    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'communaute/edit_post.html', context)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    
    return redirect('post_detail', post_id=post.id)

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("post_detail", pk=post.id)
    else:
        form = CommentForm()

    return redirect("post_detail", pk=post.id)
