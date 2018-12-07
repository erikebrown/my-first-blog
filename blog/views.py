from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import PostForm
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
            print('form is valid')
            # Retrieve values and save post
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance = post)

    print('calling render')
    return render(request, 'blog/post_edit.html', {'form': form})

def post_new(request):
    return post_new_or_edit(request, None)

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return post_new_or_edit(request, post)

