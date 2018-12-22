from django.urls import path
from . import views

app_name = 'images'
urlpatterns = [
    path('', views.ListAllImages.as_view(), name='all_images'),
    path('comment/', views.ListAllComment.as_view(), name='all_comment'),
    path('likes/', views.ListAllLikes.as_view(), name='all_likes'),
]
