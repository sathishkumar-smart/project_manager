from django.urls import path
from .views import RegisterView, LoginView, EmailLoginView
from rest_framework.authtoken.views import obtain_auth_token

# URL patterns for user authentication
urlpatterns = [
    # User registration endpoint
    path('register/', RegisterView.as_view(), name='register'),
    
    # Normal login endpoint (username/password)
    path('normal-login/', LoginView.as_view(), name='login-normal'),
    
    # Email-based login endpoint
    path('login/', EmailLoginView.as_view(), name='login'),
    
    # DRF default token authentication endpoint (optional)
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),
]
