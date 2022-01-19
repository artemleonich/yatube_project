from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Group, Post, User


@login_required
def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    template = "posts/index.html"
    context = {
        "page_obj": page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    template = "posts/group_list.html"
    context = {
        "group": group,
        "posts": posts,
        "page_obj": page_obj,
    }
    return render(request, template, context)
