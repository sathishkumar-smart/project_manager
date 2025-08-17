"""
views.py

Handles API endpoints for authentication & registration.
Business logic is delegated to AuthService and DB operations to UserRepository.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny

from .serializers import UserSerializer, EmailAuthTokenSerializer
from .services.auth_service import AuthService


class RegisterView(APIView):
    """
    API endpoint to register a new user.
    Returns user data and an auth token.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user, token = AuthService.register_user(serializer)

        return Response({
            "token": token.key,
            "user": serializer.data
        }, status=status.HTTP_201_CREATED)


class LoginView(ObtainAuthToken):
    """
    API endpoint to login with username & password.
    Returns auth token and user info.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token_key = response.data["token"]

        # AuthService still used for consistency
        token_user = self.serializer_class().Meta.model.objects.get(auth_token__key=token_key)

        return Response({
            "token": token_key,
            "user_id": token_user.id,
            "email": token_user.email
        })


class EmailLoginView(APIView):
    """
    API endpoint to login with email & password instead of username.
    Returns auth token and user info.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = EmailAuthTokenSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        user, token = AuthService.login_user(serializer)

        return Response({
            "token": token.key,
            "user_id": user.id,
            "email": user.email
        })
