from django.urls import path
from .views import CreateUserAPIView
from rest_framework_simplejwt.views import (
    TokenRefreshView, 
    TokenObtainPairView, 
    TokenVerifyView
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path('user-create/', CreateUserAPIView.as_view(), name='create_user'),
]