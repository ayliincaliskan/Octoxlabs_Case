from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

import json
from .models import Post, Tag
from .serializers import PostSerializer, TagSerializer
from core.helpers import redis_connection

r = redis_connection()

class PostView(APIView):
    def get(self, request):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save()  # saved to db
            try:
                task = {
                    "action": "Post created",
                    "post_title": post.title,
                }
                r.rpush("task_queue", json.dumps(task))
            except Exception as e:
                print(f"{e}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagView(APIView):
    def get(self, request):
        queryset = Tag.objects.all()
        serializer = TagSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() # saved to db
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)