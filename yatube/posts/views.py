from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render


from .models import Group
from .models import Post
from .models import User
from .forms import PostForm


POSTS_LIMIT = 10


def index(request):
    post_list = Post.objects.all().order_by("-pub_date")
    paginator = Paginator(post_list, POSTS_LIMIT)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    posts = Post.objects.select_related("author", "group")[:POSTS_LIMIT]
    context = {
        "posts": posts,
        "page_obj": page_obj,
    }
    return render(request, "posts/index.html", context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group)
    paginator = Paginator(posts, POSTS_LIMIT)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "group": group,
        "posts": posts,
        "page_obj": page_obj,
    }
    return render(request, "posts/group_list.html", context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=author).all()
    count_user_posts = post_list.count()
    paginator = Paginator(post_list, POSTS_LIMIT)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    title = username
    context = {
        "author": author,
        "count_user_posts": count_user_posts,
        "page_obj": page_obj,
        "title": title,
    }
    return render(request, "posts/profile.html", context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = get_object_or_404(User, username=post.author)
    count = Post.objects.filter(author_id=user).all().count()
    context = {
        "post": post,
        "count": count,
    }
    return render(request, "posts/post_detail.html", context)


def post_create(request):
    template = "posts/create_post.html"
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            return redirect("posts:profile", post.author)
        return render(request, template, {"form": form})
    form = PostForm()
    title = "Добавить запись"
    return render(request, template, {"form": form, "title": title})


def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(instance=post)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            return redirect("posts:post_detail", post_id=post_id)
        return render(request, "posts/create_post.html", {"form": form})

    is_edit = True
    context = {
        "form": form,
        "is_edit": is_edit,
    }
    return render(request, "posts/create_post.html", context)
