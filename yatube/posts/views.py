from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from .models import Group, Post, User
from .forms import PostForm


POSTS_LIMIT = 10


def page_obj(request, posts):
    paginator = Paginator(posts, POSTS_LIMIT)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)


def index(request):
    context = {
        "page_obj": page_obj(request, Post.objects.all()),
    }
    return render(request, "posts/index.html", context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    context = {
        "group": group,
        "page_obj": page_obj(request, group.posts.all()),
    }
    return render(request, "posts/group_list.html", context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    count_user_posts = author.posts.count()
    context = {
        "author": author,
        "count_user_posts": count_user_posts,
        "page_obj": page_obj(request, author.posts.all()),
    }
    return render(request, "posts/profile.html", context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    author = post.author
    count = author.posts.count()
    context = {
        "post": post,
        "count": count,
    }
    return render(request, "posts/post_detail.html", context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        form.instance.author = request.user
        form.save()
        return redirect("posts:profile", request.user.username)
    return render(request, "posts/create_post.html", {"form": form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect("posts:post_detail", post_id)
    form = PostForm(request.POST or None, instance=post)

    if form.is_valid():
        form.save()
        return redirect("posts:post_detail", post_id=post.id)
    return render(
        request,
        "posts/create_post.html",
        {
            "form": form,
            "is_edit": True,
        },
    )
