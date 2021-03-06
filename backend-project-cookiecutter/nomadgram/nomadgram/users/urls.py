from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path('explore/', views.ExploreUsers.as_view(), name='explore_users'),
    path('search/', views.Search.as_view(), name='search'),
    path('<int:user_id>/follow/', views.FollowUser.as_view(), name='follow_User'),
    path('<int:user_id>/unfollow/', views.UnFollowUser.as_view(), name='unfollow_user'),
    path('<str:username>/', views.UserProfile.as_view(), name='user_profile'),
    path('<str:username>/followers/', views.UserFollowers.as_view(), name='user_followers'),
    path('<str:username>/following/', views.UserFollowing.as_view(), name='user_following'),
    path('<str:username>/password/', views.ChangePassword.as_view(), name='change_password'),
    path('login/facebook/', views.FacebookLogin.as_view(), name='fb_login')
]
