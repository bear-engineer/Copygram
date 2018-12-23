from django.urls import path
from . import views

app_name = 'images'
urlpatterns = [
    path('', views.Feed.as_view(), name='feed'),
    path('<int:image_id>/like/', views.LikeImage.as_view(), name='like_image'),
    path('<int:image_id>/comment/', views.CommentOnImage.as_view(), name='comment')
]
