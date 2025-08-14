from rest_framework import generics, permissions
from .serializers import UserSerializer

class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permissions_classes = [permissions.AllowAny]


