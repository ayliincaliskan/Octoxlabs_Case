from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

from django.contrib.auth.models import User
from core.helpers import create_task
from .serializers import UserSerializer
from core.utils import messages


class CreateUserAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny] 
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        try:
            create_task(message=messages['USER_CREATE'], title="user", value=user.username)
        except Exception as e:
            print(f"{e}")
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': messages['USER_CREATE'],
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

    def perform_destroy(self, instance):
        try:
            create_task(message=messages['USER_DELETE'], title="user", value=instance.username)
        except Exception as e:
            print(f"{e}")
        instance.delete()


class UserListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
