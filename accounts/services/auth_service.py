from accounts.repositories.user_repository import UserRepository

class AuthService:
    """Service layer for authentication and user registration logic."""

    @staticmethod
    def register_user(serializer):
        """Register a new user and return (user, token)."""
        user = serializer.save()
        token, _ = UserRepository.get_or_create_token(user)
        return user, token

    @staticmethod
    def login_user(serializer):
        """Login via username/password serializer."""
        user = serializer.validated_data["user"]
        token, _ = UserRepository.get_or_create_token(user)
        return user, token
