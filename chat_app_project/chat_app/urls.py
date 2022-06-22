from django.urls import path

from . import views

app_name = "chat_app"

urlpatterns = [
    path("", views.ViewIndex.as_view(), name="index"),
    path("login", views.ViewLogin.as_view(), name="login"),
    path("register", views.ViewRegister.as_view(), name="register"),
    path("logout", views.ViewLogout.as_view(), name="logout")
]
