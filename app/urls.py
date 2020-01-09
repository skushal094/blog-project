from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginpage, name='login'),
    path('home/', views.homepage, name='home'),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logoutlink, name="logout"),
    path('profile/', views.profilepage, name="profile"),
    path('changepass/', views.changepwd, name="changepwd"),
    path('likes/<int:blog_id>/', views.likes, name="likes"),
    path('likeflip/<int:blog_id>/', views.likeflip, name="like_flip"),
    path('newblog/', views.newblog, name="newblog"),
    path('myblogs/', views.myblogs, name="myblogs"),
]
