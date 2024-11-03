from django.urls import path
from .views import PostView, TagView

urlpatterns = [
    path('posts/', PostView.as_view(), name='posts'),
    path('posts/<int:post_id>/', PostView.as_view(), name='post_detail'),
    path('tags/', TagView.as_view(), name='tags'),
    path('tags/<int:tag_id>/', TagView.as_view(), name='tag_detail'),
]