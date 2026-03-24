from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .serializers import SignupSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Signup view
class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = SignupSerializer

# Login view uses built-in JWT view
class UserLoginView(TokenObtainPairView):
    permission_classes = [AllowAny]