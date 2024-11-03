from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import generics, status

from django.contrib.auth.models import User
from core.helpers import redis_connection
from .serializers import UserSerializer
from core.utils import messages
import json


class CreateUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        try:
            r = redis_connection()
            task = {
                "action": messages['USER_CREATE'],
                "user": user.username
            }
            r.rpush("task_queue", json.dumps(task))
        except Exception as e:
            print(f"{e}")
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': messages['USER_CREATE'],
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

    def perform_destroy(self, instance):
        try:
            r = redis_connection()
            task = {
                "action": messages['USER_DELETE'],
                "user": instance.username
            }
            r.rpush("task_queue", json.dumps(task))
        except Exception as e:
            print(f"{e}")
        instance.delete()


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
