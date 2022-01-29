from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest


from .models import Group, Post, User
from .forms import PostForm


POSTS_LIMIT = 10


def paginate(cursor, records):
    paginator = Paginator(records, POSTS_LIMIT)
    return paginator.get_page(cursor)


def index(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.select_related("author", "group")
    page_number = request.GET.get("page")
    page_obj = paginate(page_number, posts)
    context = {
        "page_obj": page_obj,
    }
    return render(request, "posts/index.html", context)


def group_posts(request: HttpRequest, slug: str) -> HttpResponse:
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
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
    count_user_posts = author.posts.count()
    page_number = request.GET.get("page")
    page_obj = paginate(page_number, post_list)
    context = {
        "author": author,
        "count_user_posts": count_user_posts,
        "page_obj": page_obj,
    }
    return render(request, "posts/profile.html", context)


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    post = get_object_or_404(Post, id=post_id)
    author = post.author
    author_posts_count = author.posts.count()
    context = {
        "post": post,
        "author_posts_count": author_posts_count,
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
    if post.author != request.user:
        return redirect("posts:post_detail", post_id)
    form = PostForm(request.POST or None, instance=post)
    template = "posts/create_post.html"
    context = {
        "form": form,
        "is_edit": True,
    }
    if not form.is_valid():
        return render(request, template, context)
    form.save()
    return redirect("posts:post_detail", post_id=post.id)
