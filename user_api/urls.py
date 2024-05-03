from django.urls import path
from .views import (
    UserLogin,
    UserLogout,
    UserView,
    UserRegister,
)

urlpatterns = [
    path("signup", UserRegister.as_view()),
    path("login", UserLogin.as_view()),
    path("logout", UserLogout.as_view()),
    path("user", UserView.as_view()),
]
