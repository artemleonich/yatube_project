from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .models import Group
from .models import Post


POSTS_LIMIT = 10


def index(request):
    posts = Post.objects.select_related("author", "group")[:POSTS_LIMIT]
    context = {
        "posts": posts,
    }
    return render(request, "posts/index.html", context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:POSTS_LIMIT]
    context = {
        "group": group,
        "posts": posts,
    }
    return render(request, "posts/group_list.html", context)
