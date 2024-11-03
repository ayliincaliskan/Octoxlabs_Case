from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

import json
from .models import Post, Tag
from .serializers import PostSerializer, TagSerializer
from core.helpers import redis_connection
from core.utils import messages

r = redis_connection()

class PostView(GenericAPIView):
    serializer_class = PostSerializer

    def get_queryset(self, post_id):
        if post_id:
            return Post.objects.filter(id=post_id)
        return Post.objects.all()

    def get(self, request, post_id=None):
        queryset = self.get_queryset(post_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save()
            task = {
                "action": messages["POST_CREATE"],
                "post_title": post.title,
            }
            r.rpush("task_queue", json.dumps(task))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, post_id=None):
        if post_id is not None:
            try:
                post = Post.objects.get(id=post_id)
                serializer = self.get_serializer(post, data=request.data)
                if serializer.is_valid():
                    post = serializer.save()
                    task = {
                        "action": messages["POST_UPDATE"],
                        "post_title": post.title,
                    }
                    r.rpush("task_queue", json.dumps(task))
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Post.DoesNotExist:
                return Response(messages["POST_NOT_FOUND"], status=status.HTTP_404_NOT_FOUND)
        return Response(messages["POST_ID_REQUIRE"], status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id=None):
        if post_id is not None:
            try:
                post = Post.objects.get(id=post_id)
                task = {
                    "action": messages["POST_DELETE"],
                    "post_title": post.title,
                }
                r.rpush("task_queue", json.dumps(task))
                post.delete()
                return Response(messages["POST_DELETE"], status=status.HTTP_204_NO_CONTENT)
            except Post.DoesNotExist:
                return Response(messages["POST_NOT_FOUND"], status=status.HTTP_404_NOT_FOUND)
        return Response(messages["POST_ID_REQUIRE"], status=status.HTTP_400_BAD_REQUEST)


class TagView(GenericAPIView):
    serializer_class = TagSerializer

    def get_queryset(self, tag_id):
        if tag_id:
            return Tag.objects.filter(id=tag_id)
        return Tag.objects.all()

    def get(self, request, tag_id=None):
        queryset = self.get_queryset(tag_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            tag = serializer.save()
            task = {
                "action": messages["TAG_CREATE"],
                "tag_name": tag.name,
            }
            r.rpush("task_queue", json.dumps(task))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, tag_id=None):
        if tag_id is not None:
            try:
                tag = Tag.objects.get(id=tag_id)
                serializer = self.get_serializer(tag, data=request.data)
                if serializer.is_valid():
                    tag = serializer.save()
                    task = {
                        "action": messages["TAG_UPDATE"],
                        "tag_name": tag.name,
                    }
                    r.rpush("task_queue", json.dumps(task))
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Tag.DoesNotExist:
                return Response(messages["TAG_NOT_FOUND"], status=status.HTTP_404_NOT_FOUND)
        return Response(messages["TAG_ID_REQUIRE"], status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, tag_id=None):
        if tag_id is not None:
            try:
                tag = Tag.objects.get(id=tag_id)
                task = {
                        "action": messages["TAG_DELETE"],
                        "tag_name": tag.name,
                    }
                r.rpush("task_queue", json.dumps(task))
                tag.delete() 
                return Response(messages["TAG_DELETE"], status=status.HTTP_204_NO_CONTENT)
            except Tag.DoesNotExist:
                return Response(messages["TAG_NOT_FOUND"], status=status.HTTP_404_NOT_FOUND)
        return Response(messages["TAG_ID_REQUIRE"], status=status.HTTP_400_BAD_REQUEST)
