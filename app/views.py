from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login


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
            msg = "Incorrect username or password"
            return render(request, 'app/login_page.html', {'msg': msg})
    return render(request, 'app/login_page.html', {})


def homepage(request):
    if not request.user.is_authenticated:
        return redirect(loginpage)
    return HttpResponse(str(request.user))
