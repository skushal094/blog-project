from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import Blog, Like, Comment
from django.db.models import Count, F, Q


def loginpage(request):
    if request.user.is_authenticated:
        return redirect(homepage)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(homepage)
        else:
            messages.add_message(request, messages.WARNING, "Incorrect username or password")
            return render(request, 'app/login_page.html', {})
    return render(request, 'app/login_page.html', {})


def homepage(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO, "Please Login First.")
        return redirect(loginpage)
    blogs = Blog.objects.filter(Q(like__is_deleted=False)).annotate(likes=Count('like__blog_id'))
    this_user_liked = Like.objects.filter(user_id=request.user, is_deleted = False).values('blog_id')
    this_user_liked = list(this_user_liked)
    liked_blogs = set()
    for i in this_user_liked:
        liked_blogs.add(i['blog_id'])
    return render(request, 'app/home.html', {'blogs': blogs, 'liked_blogs': liked_blogs})


def signup(request):
    if request.user.is_authenticated:
        return redirect(homepage)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        cf_password = request.POST.get('cf_password')
        if password == cf_password:
            User.objects.create_user(username, password=password)
            return redirect(loginpage)
        else:
            messages.add_message(request, messages.WARNING, "Passwords do not match")
            return redirect(signup)
    return render(request, 'app/signup.html', {})


def logoutlink(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO, "Please Login First.")
        return redirect(loginpage)
    logout(request)
    return redirect(loginpage)


def profilepage(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO, "Please Login First.")
        return redirect(loginpage)
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        messages.add_message(request, messages.SUCCESS, "Profile updated successfully")
    return render(request, 'app/profile.html', {})


def changepwd(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO, "Please Login First.")
        return redirect(loginpage)
    if request.method == 'POST':
        username = request.user.get_username()
        user = User.objects.get(username=username)
        current = request.POST.get('current')
        newpwd = request.POST.get('newpwd')
        newpwd1 = request.POST.get('newpwd1')
        if newpwd == newpwd1:
            if check_password(current, user.password):
                messages.add_message(request, messages.SUCCESS, "Password changed successfully")
                user.set_password(newpwd)
                user.save()
                return redirect(homepage)
            else:
                messages.add_message(request, messages.WARNING, "Incorrect current password")
        else:
            messages.add_message(request, messages.WARNING, "Passwords do not match")
    return render(request, 'app/changepwd.html', {})


def likes(request, blog_id):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO, "Please Login First.")
        return redirect(loginpage)
    users = Like.objects.all().filter(blog_id=blog_id, is_deleted=False).annotate(name=F('user_id__username'))
    return render(request, 'app/likespage.html', {'users': users})


def likeflip(request, blog_id):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO, "Please Login First.")
        return redirect(loginpage)
    like_entry = Like.objects.filter(blog_id=blog_id, user_id=request.user)
    if not like_entry:
        blog = Blog.objects.get(pk=blog_id)
        new_like = Like.objects.create(blog_id=blog, user_id=request.user)
    else:
        like_entry = like_entry[0]
        if like_entry.is_deleted:
            like_entry.is_deleted = False
        else:
            like_entry.is_deleted =True
        like_entry.save()
    return redirect(homepage)
