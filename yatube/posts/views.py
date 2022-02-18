from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest

from .models import Group, Post, User, Comment, Follow
from .forms import PostForm, CommentForm
from .utils import paginate


def index(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.select_related("author", "group")

    page_number = request.GET.get("page")
    page_obj = paginate(page_number, posts)

    context = {
        "page_obj": page_obj,
        "index": True,
    }
    return render(request, "posts/index.html", context)


def group_posts(request: HttpRequest, slug: str) -> HttpResponse:
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related("author")

    page_number = request.GET.get("page")
    page_obj = paginate(page_number, posts)

    context = {
        "group": group,
        "page_obj": page_obj,
    }
    return render(request, "posts/group_list.html", context)


def profile(request: HttpRequest, username: str) -> HttpResponse:
    author = get_object_or_404(User, username=username)

    post_list = author.posts.all()

    page_number = request.GET.get("page")
    page_obj = paginate(page_number, post_list)
    following = (
        request.user.is_authenticated
        and Follow.objects.filter(user=request.user, author=author).exists()
    )

    count_user_posts = author.posts.count()

    context = {
        "author": author,
        "count_user_posts": count_user_posts,
        "page_obj": page_obj,
        "following": following,
    }
    return render(request, "posts/profile.html", context)


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    post = get_object_or_404(Post, id=post_id)
    author = post.author

    author_posts_count = author.posts.count()

    comments = Comment.objects.filter(post_id=post_id)
    form = CommentForm()

    context = {
        "post": post,
        "author_posts_count": author_posts_count,
        "form": form,
        "comments": comments,
    }
    return render(request, "posts/post_detail.html", context)


@login_required
def post_create(request: HttpRequest) -> HttpResponse:
    form = PostForm(request.POST or None)

    if not form.is_valid():
        return render(request, "posts/create_post.html", {"form": form})

    form.instance.author = request.user
    form.save()
    return redirect("posts:profile", request.user.username)


@login_required
def post_edit(request: HttpRequest, post_id: int) -> HttpResponse:
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post,
    )

    if post.author != request.user:
        return redirect("posts:post_detail", post_id)

    template = "posts/create_post.html"
    context = {
        "form": form,
        "is_edit": True,
    }

    if not form.is_valid():
        return render(request, template, context)

    form.save()
    return redirect("posts:post_detail", post_id=post.id)


@login_required
def add_comment(request: HttpRequest, post_id: int) -> HttpResponse:
    form = CommentForm(request.POST or None)
    post = get_object_or_404(Post, id=post_id)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect("posts:post_detail", post_id=post_id)


@login_required
def follow_index(request: HttpRequest) -> HttpResponse:
    """Функция генерирует страницу с постами авторов,
    на которых подписан пользователь."""
    template = "posts/follow.html"
    posts_list = Post.objects.filter(author__following__user=request.user)
    page_obj = paginate(request, posts_list)
    context = {"page_obj": page_obj, "follow": True}
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    """Функция для подписки на авторов."""
    template = "posts:profile"
    author = get_object_or_404(User, username=username)
    user = request.user
    if user != author:
        Follow.objects.get_or_create(user=user, author=author)
        return redirect(template, username=author)
    return redirect(template, username=author.username)


@login_required
def profile_unfollow(request, username):
    """Функция для отписок."""
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect("posts:profile", username=username)
