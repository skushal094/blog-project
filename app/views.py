from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import check_password


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
    return render(request, 'app/home.html')


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
