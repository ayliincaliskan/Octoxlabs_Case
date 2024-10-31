from django.urls import path
from .views import PostView, TagView

urlpatterns = [
    path('posts/', PostView.as_view(), name='posts'),
    path('tags/', TagView.as_view(), name='tags'),
]