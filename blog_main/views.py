from django.shortcuts import render, redirect
from blogs.models import Category, Blog
from features.models import About
from django.http import HttpResponse
from blogs.forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib import messages


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


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created successfully!")
            return redirect("login")
        else:
            print(form.errors)
    else:
        form = RegistrationForm()
    context = {
        "form": form,
    }
    return render(request, "register.html", context)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
            return redirect('dashboard')    
    form = AuthenticationForm()
    context = {
        "form": form,
    }
    return render(request, "login.html", context)

def logout(request):
    auth.logout(request)
    return redirect('home')
