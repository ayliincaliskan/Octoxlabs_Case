from django.urls import path
from .views import PostView, TagView

urlpatterns = [
    path('post-create/', PostView.as_view(), name='posts'),
    path('post-list/', PostView.as_view(), name='post_list'),
    path('posts/<int:post_id>/', PostView.as_view(), name='post_detail'),
    path('tag-create/', TagView.as_view(), name='tags'),
    path('tag-list/', TagView.as_view(), name='tag_list'),
    path('tags/<int:tag_id>/', TagView.as_view(), name='tag_detail'),
]
