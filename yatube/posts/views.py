from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .models import Group
from .models import Post


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
