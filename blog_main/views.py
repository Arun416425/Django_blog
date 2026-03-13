from django.shortcuts import render
from blogs.models import Category, Blog
from features.models import About
from django.http import HttpResponse


def home(request):
    categories = Category.objects.all()
    featured_post = Blog.objects.filter(is_featured=True, status="Published")
    posts = Blog.objects.filter(is_featured=False, status="Published")

    try:
        about = About.objects.get()
    except:
        about = None
    context = {
        "categories": categories,
        "featured_post": featured_post,
        "posts": posts,
        "about": about,
    }
    return render(request, "home.html", context)
