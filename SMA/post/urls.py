from django.urls import path
from post import views

urlpatterns = [
    path('',views.index,name="index"),
    path('settings',views.settings,name='settings'),
    path('signup',views.signup,name='signup'),
    path('upload',views.upload,name='upload'),
    path('follow',views.follow,name='follow'),
    path('search',views.search,name='search'),
    path('like-post',views.like_post,name='like-post'),
    path('profile/<str:pk>',views.profile,name='profile'),
    path('signin',views.signin,name='signin'),
    path('logout',views.logout,name='logout'),
  
]