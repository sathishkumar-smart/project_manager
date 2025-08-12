from django.urls import path
from .views import RegisterView,LoginView,EmailLoginView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('nomral-login/', LoginView.as_view(), name='login-normal'),
    path('login/', EmailLoginView.as_view(), name='login'),
]
