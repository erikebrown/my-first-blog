from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import PostForm, CommentForm
from .models import Post

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(
        published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})
    
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post':post})

def post_new_or_edit(request, post):
    if request.method == 'POST':
        form = PostForm(
            request.POST,
            instance = post
        )
        if form.is_valid():
            # Retrieve values and save post
            post = form.save(commit=False)
            post.author = request.user
            # removed: post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance = post)

    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_new(request):
    return post_new_or_edit(request, None)

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return post_new_or_edit(request, post)

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts':posts})

def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

def login(request):
    pass
    