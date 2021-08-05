from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .forms import CommentForm, PostForm
from .models import Follow, Post, Group, User


def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(request, 'misc/500.html', status=500)


def index(request):
    post = Post.objects.all()
    paginator = Paginator(post, settings.POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'index.html',
        {'page': page}
    )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post = group.posts.all()
    paginator = Paginator(post, settings.POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'group.html',
        {'group': group, 'page': page}
    )


def post_view(request, username, post_id):
    post_view = get_object_or_404(Post, author__username=username, id=post_id)
    form = CommentForm(request.POST or None)
    comments = post_view.comments.all()

    posts_count = post_view.author.posts.count()
    followers_count = Follow.objects.filter(author=post_view.author).count()
    follow_count = Follow.objects.filter(user=post_view.author).count()

    if not request.user.is_authenticated or not Follow.objects.filter(
        author=post_view.author, user=request.user
    ).exists():
        context = {
            'form': form,
            'post_view': post_view,
            'posts_count': posts_count,
            'comments': comments,
            'follow_count': follow_count,
            'followers_count': followers_count,
        }

        return render(request, 'post.html', context)

    context = {
        'form': form,
        'post_view': post_view,
        'posts_count': posts_count,
        'comments': comments,
        'follow_count': follow_count,
        'followers_count': followers_count,
        'following': True,
    }

    return render(request, 'post.html', context)


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()

    return redirect('post', username, post_id)


@login_required
def new_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)

    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()

        return redirect('index')

    return render(
        request,
        'new_post.html',
        {'form': form}
    )


@login_required
def post_edit(request, username, post_id):
    post_edit = get_object_or_404(Post, id=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post_edit
    )

    if request.user != post_edit.author:
        return redirect('post', post_edit.author, post_edit.id)

    if form.is_valid():
        post_edit.save()

        return redirect('post', post_edit.author, post_edit.id)

    return render(
        request,
        'new_post.html',
        {'form': form, 'post_edit': post_edit}
    )


def profile(request, username):
    author = get_object_or_404(User, username=username)

    paginator = Paginator(author.posts.all(), settings.POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    posts_count = author.posts.count()
    followers_count = Follow.objects.filter(author=author).count()
    follow_count = Follow.objects.filter(user=author).count()

    if not request.user.is_authenticated or not Follow.objects.filter(
        author=author, user=request.user
    ).exists():

        context = {
            'author': author,
            'posts_count': posts_count,
            'page': page,
            'follow_count': follow_count,
            'followers_count': followers_count,
        }

        return render(request, 'profile.html', context)

    context = {
        'author': author,
        'posts_count': posts_count,
        'page': page,
        'follow_count': follow_count,
        'followers_count': followers_count,
        'following': True,
    }

    return render(request, 'profile.html', context)


@login_required
def follow_index(request):
    # информация о текущем пользователе доступна в переменной request.user
    # Напишите view-функцию страницы, куда будут выведены посты авторов,
    # на которых подписан текущий пользователь.

    posts = Post.objects.filter(author__following__user=request.user)

    paginator = Paginator(posts, settings.POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, "follow.html", {'page': page})


@login_required
def profile_follow(request, username):
    # view-функция для подписки на интересного автора

    author = get_object_or_404(User, username=username)

    if request.user != author:
        if not Follow.objects.filter(
            author=author, user=request.user
        ).exists():
            Follow.objects.create(author=author, user=request.user)

    followers_count = Follow.objects.filter(author=author).count()
    follow_count = Follow.objects.filter(user=author).count()
    posts_count = author.posts.count()

    paginator = Paginator(author.posts.all(), settings.POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'author': author,
        'posts_count': posts_count,
        'page': page,
        'follow_count': follow_count,
        'followers_count': followers_count,
        'following': True
    }

    return render(request, 'profile.html', context)


@login_required
def profile_unfollow(request, username):
    # для того, чтобы отписаться от надоевшего графомана

    author = get_object_or_404(User, username=username)

    if Follow.objects.filter(author=author, user=request.user).exists():
        Follow.objects.filter(author=author, user=request.user).delete()

    followers_count = Follow.objects.filter(author=author).count()
    follow_count = Follow.objects.filter(user=author).count()
    posts_count = author.posts.count()

    paginator = Paginator(author.posts.all(), settings.POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'author': author,
        'posts_count': posts_count,
        'page': page,
        'follow_count': follow_count,
        'followers_count': followers_count,
    }

    return render(request, 'profile.html', context)
