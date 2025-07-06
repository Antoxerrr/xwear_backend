from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token, ObtainAuthToken
from rest_framework.parsers import JSONParser

from . import views


urlpatterns = [
    path('login/', ObtainAuthToken.as_view(parser_classes=(JSONParser,)), name="login"),
    path('register/', views.register_view, name="register"),
    path('profile/', views.user_view, name="user")
]
