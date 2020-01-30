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
    path('blog/delete/', views.delete_blog, name="delete_blog"),
    path('blog/edit/<int:blog_id>', views.edit_blog, name="edit_blog"),
    path('comments/<int:blog_id>/', views.comments, name="comments"),
    path('comments/delete/<int:comment_id>', views.delete_comment, name="delete_comment"),
    path('comments/likeflip/', views.comment_like_flip, name="comment_like_flip"),
]
