from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from .models import Post, Group


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')

    paginator = Paginator(post_list, 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)

def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)

    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, 'posts/group_list.html', context)

def profile(request, username):
    user_posts = Post.objects.filter(author__username=username)
    c_posts = user_posts.count()
    paginator = Paginator(user_posts, 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {
        'username': username,
        'c_posts': c_posts,
        'user_posts': user_posts,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    c_posts = Post.objects.filter(author=post.author).count()
    context = {
        'post': post,
        'c_posts': c_posts,
    }
    return render(request, 'posts/post_detail.html', context)