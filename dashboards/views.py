from django.shortcuts import render, redirect, get_object_or_404
from blogs.models import Category, Blog
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm, BlogpostForm
from django.template.defaultfilters import slugify


@login_required(login_url="login")
def dashboard(request):
    category_count = Category.objects.all().count()
    blogs_count = Blog.objects.all().count()

    context = {"category_count": category_count, "blogs_count": blogs_count}
    return render(request, "dashboard/dashboard.html", context)


def categories(request):
    return render(request, "dashboard/categories.html")


def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("categories")
    else:
        form = CategoryForm()
    context = {
        "form": form,
    }
    return render(request, "dashboard/add_category.html", context)


def edit_category(request, pk):
    category = get_object_or_404(Category, id=pk)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("categories")
    else:
        form = CategoryForm(instance=category)
    context = {
        "form": form,
        "category": category,
    }
    return render(request, "dashboard/add_category.html", context)


def delete_category(request, pk):
    category = get_object_or_404(Category, id=pk)
    if request.method == "POST":
        category.delete()
        return redirect("categories")

    context = {
        "category": category,
    }

    return render(request, "dashboard/delete_category.html", context)


def posts(request):
    posts = Blog.objects.all()
    context = {
        "posts": posts,
    }
    return render(request, "dashboard/posts.html", context)


def add_post(request):
    if request.method == "POST":
        form = BlogpostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            title = form.cleaned_data["title"]
            post.slug = slugify(title) + "-" + str(post.id)
            post.save()
            return redirect("posts")

    form = BlogpostForm()
    context = {"form": form}
    return render(request, "dashboard/add_post.html", context)


def edit_post(request, pk):
    post = get_object_or_404(Blog, id=pk)
    if request.method == "POST":
        form = BlogpostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            title = form.cleaned_data["title"]
            post.slug = slugify(title) + "-" + str(post.id)
            post.save()
            return redirect("posts")

    form = BlogpostForm(instance=post)
    context = {
        "form": form,
        "post": post,
    }
    return render(request, "dashboard/edit_post.html", context)

def delete_post(request, pk):
    post = get_object_or_404(Blog, id=pk)
    post.delete()
    return redirect('posts')