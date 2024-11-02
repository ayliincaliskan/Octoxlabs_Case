from core.helpers import redis_connection
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import generics, status

from django.contrib.auth.models import User
from .serializers import UserSerializer
import json


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            return Response({
                "token": response.data['access'],
                "message": "Giriş başarılı!"
            }, status=status.HTTP_200_OK)
        return response


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
                "action": "User created",
                "user": user.username
            }
            r.rpush("task_queue", json.dumps(task))
        except Exception as e:
            print(f"{e}")
        # Token oluşturma
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'User created successfully.',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)