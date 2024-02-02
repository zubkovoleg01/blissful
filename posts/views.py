from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from . forms import PostForm, CommentForm
from .models import Post, Group, Comment, Follow, User


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
    following = False
    if request.user.is_authenticated:
        following = request.user.follower.filter(author__username=username).exists()
    paginator = Paginator(user_posts, 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {
        'username': username,
        'c_posts': c_posts,
        'user_posts': user_posts,
        'page_obj': page_obj,
        'following': following,
        'author': request.user,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    c_posts = Post.objects.filter(author=post.author).count()
    comments = post.comments.all()
    form = CommentForm()
    context = {
        'post': post,
        'c_posts': c_posts,
        'comments': comments,
        'form': form
    }
    return render(request, 'posts/post_detail.html', context)

@login_required
def post_create(request):
    template = 'posts/create_post.html'
    form = PostForm(
        request.POST or None,
        files=request.FILES or None
    )
    if form.is_valid():
        temp_form = form.save(commit=False)
        temp_form.author = request.user
        temp_form.save()
        return redirect(
            'posts:profile', temp_form.author
        )
    return render(request, template, {'form': form})


def post_edit(request, post_id):
    template = 'posts/create_post.html'
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect(
            'posts:post_detail', post_id
        )
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect(
            'posts:post_detail', post_id
        )
    return render(request, template, {
        'form': form, 'is_edit': True, 'post': post
    })


def page_not_found(request, exception):
    return render(request, 'core/404.html', {'path': request.path}, status=404)

@login_required
def add_comment(request, post_id):
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = get_object_or_404(Post, pk=post_id)
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    template = 'posts/follow.html'
    title = 'Публикации избранных авторов'
    posts = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': title,
        'page_obj': page_obj,
    }
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    follow_author = get_object_or_404(User, username=username)
    if follow_author != request.user and (
        not request.user.follower.filter(author=follow_author).exists()
    ):
        Follow.objects.create(
            user=request.user,
            author=follow_author
        )
    return redirect('posts:profile', username)


@login_required
def profile_unfollow(request, username):
    follow_author = get_object_or_404(User, username=username)
    data_follow = request.user.follower.filter(author=follow_author)
    if data_follow.exists():
        data_follow.delete()
    return redirect('posts:profile', username)


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author == request.user:
        post.delete()
    return redirect('posts:profile', post.author.username)


@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment.author == request.user:
        comment.delete()
    return redirect('posts:post_detail', post_id=comment.post.pk)