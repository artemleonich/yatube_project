from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from .models import Group, Post, User
from .forms import PostForm


POSTS_LIMIT = 10


def index(request):
    posts = Post.objects.select_related("author", "group")
    paginator = Paginator(posts, POSTS_LIMIT)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "posts": posts,
        "page_obj": page_obj,
    }
    return render(request, "posts/index.html", context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, POSTS_LIMIT)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "group": group,
        "page_obj": page_obj,
    }
    return render(request, "posts/group_list.html", context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    count_user_posts = post_list.count()
    paginator = Paginator(post_list, POSTS_LIMIT)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "author": author,
        "count_user_posts": count_user_posts,
        "page_obj": page_obj,
    }
    return render(request, "posts/profile.html", context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = get_object_or_404(User, username=post.author)
    count = user.posts.all().count()
    context = {
        "post": post,
        "count": count,
    }
    return render(request, "posts/post_detail.html", context)


@login_required
def post_create(request):
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        form.save()
        return redirect("posts:profile", post.author)
    return render(request, "posts/create_post.html", {"form": form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(instance=post)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            form.save()
            return redirect("posts:post_detail", post_id=post_id)
        return render(request, "posts/create_post.html", {"form": form})

    is_edit = True
    context = {
        "form": form,
        "is_edit": is_edit,
        "post": post,
    }
    return render(request, "posts/create_post.html", context)
