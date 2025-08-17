from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserRepository:
    """Repository for user-related DB operations."""

    @staticmethod
    def create_user(**kwargs):
        """Create a new user."""
        return User.objects.create_user(**kwargs)

    @staticmethod
    def get_or_create_token(user):
        """Return existing token or create new one for a user."""
        return Token.objects.get_or_create(user=user)
