"""
View file having views to handle user requests.
"""

from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.db.models import F, Case, When, BooleanField, Count, Q
from django.contrib.auth.decorators import login_required
from .models import Blog, Like, Comment


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
    # blogs = Blog.objects.filter(Q(like__is_deleted=False)).annotate(likes=Count('like__blog_id'))
    blogs = Blog.objects.all().filter(is_deleted=False)
    # blogs = blogs.annotate(likes=Case(
    # When(like__is_deleted=False, then=Count('like__blog_id')), default=0),
    # deleted=Case(When(like__is_deleted=True, then=True), default=False,
    # output_field=BooleanField()))
    # .filter(deleted=False)
    # likes = list(Like.objects.all().filter(is_deleted=False).values('blog_id')
    # .annotate(likes=Count('blog_id')))
    blogs = blogs.order_by('-created_at')
    this_user_liked = Like.objects.filter(user_id=request.user, is_deleted=False).values('blog_id')
    this_user_liked = list(this_user_liked)
    liked_blogs = set()
    for i in this_user_liked:
        liked_blogs.add(i['blog_id'])
    total_users = User.objects.all().count()
    return render(request, 'app/home.html', {'blogs': blogs,
                                             'liked_blogs': liked_blogs,
                                             'total_users': total_users})


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
        return redirect(homepage)
    total_users = User.objects.all().count()
    return render(request, 'app/profile.html', {'total_users': total_users})


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
    total_users = User.objects.all().count()
    return render(request, 'app/changepwd.html', {'total_users': total_users})


def likes(request, blog_id):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO, "Please Login First.")
        return redirect(loginpage)
    users = Like.objects.all().filter(blog_id=blog_id, is_deleted=False)\
        .annotate(name=F('user_id__username'))
    total_users = User.objects.all().count()
    try:
        link = request.GET.get('refer')
        return render(request, 'app/likespage.html', {'users': users,
                                                      'refer': link,
                                                      'total_users': total_users})
    except:
        return render(request, 'app/likespage.html', {'users': users,
                                                      'refer': link,
                                                      'total_users': total_users})


def likeflip(request, blog_id):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO, "Please Login First.")
        return redirect(loginpage)
    like_entry = Like.objects.filter(blog_id=blog_id, user_id=request.user)
    blog = Blog.objects.get(pk=blog_id)
    if not like_entry:
        new_like = Like.objects.create(blog_id=blog, user_id=request.user)
        blog.likes += 1
        blog.save()
    else:
        like_entry = like_entry[0]
        if like_entry.is_deleted:
            like_entry.is_deleted = False
            blog.likes += 1
        else:
            like_entry.is_deleted = True
            blog.likes -= 1
        blog.save()
        like_entry.save()
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def newblog(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO, "Please Login First.")
        return redirect(loginpage)
    if request.method == 'POST':
        allowed = ['jpg', 'jpeg', 'png']
        user = request.user
        image = request.FILES['image']
        desc = request.POST.get('desc')
        if str(image).split('.')[-1] in allowed:
            new_blog = Blog.objects.create(author=user, image=image, description=desc)
            messages.add_message(request, messages.SUCCESS,
                                 "Congratulations! Your new blog is live now.")
            return redirect(homepage)
        else:
            messages.add_message(request, messages.ERROR, "Image must be .jpg, .jpeg or .png")
    total_users = User.objects.all().count()
    return render(request, 'app/newblog.html', {'total_users': total_users})


def myblogs(request):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO, "Please Login First.")
        return redirect(loginpage)
    blogs = Blog.objects.all().filter(is_deleted=False, author=request.user).order_by('-created_at')
    this_user_liked = Like.objects.filter(user_id=request.user, is_deleted=False).values('blog_id')
    this_user_liked = list(this_user_liked)
    liked_blogs = set()
    for i in this_user_liked:
        liked_blogs.add(i['blog_id'])
    total_users = User.objects.all().count()
    return render(request, 'app/myblogs.html', {'blogs': blogs,
                                                'liked_blogs': liked_blogs,
                                                'total_users': total_users})


@login_required(login_url='/')
def delete_blog(request):
    blog_id = request.GET.get('blog_id', 0)
    blog = get_object_or_404(Blog, pk=blog_id, is_deleted=False)
    blog.is_deleted = True
    blog.save()
    return HttpResponse("Done")


@login_required(login_url='/')
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id, is_deleted=False, author=request.user)
    if request.method == "POST":
        blog.description = request.POST.get('desc') if request.POST.get('desc') else blog.description
        if request.FILES.get('image', '') != '':
            blog.image = request.FILES.get('image')
        blog.save()
        return redirect(homepage)
    total_users = User.objects.all().count()
    context = {
        'blog': blog,
        'total_users': total_users
    }
    return render(request, 'app/blog_edit.html', context)


@login_required(login_url="/")
def comments(request, blog_id):
    if not request.user.is_authenticated:
        messages.add_message(request, messages.INFO, "Please Login First.")
        return redirect(loginpage)
    # blog = Blog.objects.get(pk=blog_id)
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.method == "POST":
        if request.POST.get('action') == 'add':
            cmt_text = request.POST.get('cmt_text')
            new_cmt = Comment.objects.create(blog_id=blog, user_id=request.user, text=cmt_text)
            blog.comments += 1
            blog.save()
    like = Like.objects.filter(user_id=request.user, blog_id=blog_id, is_deleted=False)
    # case = Case(When(user_id=request.user, then=True), default=False, output_field=BooleanField())
    cmts = Comment.objects.filter(is_deleted=False, blog_id=blog_id).order_by('-created_at')
    my_cmts_liked = Comment.objects.filter(Q(blog_id=blog)).filter(Q(likes_on_comment=request.user))
    total_users = User.objects.all().count()
    return render(request, 'app/comments.html', {'blog': blog,
                                                 'comments': cmts,
                                                 'like': like,
                                                 'total_users': total_users,
                                                 'my_cmts_liked': my_cmts_liked})


@login_required(login_url='/')
def delete_comment(request, comment_id):
    cmt = Comment.objects.get(pk=comment_id)
    cmt.is_deleted = True
    cmt.save()
    blog = Blog.objects.get(pk=cmt.blog_id.pk)
    blog.comments -= 1
    blog.save()
    return HttpResponse("Done")


@login_required(login_url='/')
def comment_like_flip(request):
    cmt_id = request.GET.get('cmt_id')
    cmt = Comment.objects.get(pk=cmt_id)
    if len(Comment.objects.filter(pk=cmt_id, likes_on_comment=request.user)) == 0:
        cmt.likes_on_comment.add(request.user)
        cmt.likes += 1
        cmt.save()
        return HttpResponse(str(cmt.likes))
    else:
        cmt.likes_on_comment.remove(request.user)
        cmt.likes -= 1
        cmt.save()
        return HttpResponse(str(cmt.likes))
