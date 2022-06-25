from django.urls import path

from account.views import ViewLogin, ViewRegister, ViewLogout
from chat_app.views import ViewIndex, ViewRoom, ViewAddFriend

app_name = "chat_app"

urlpatterns = [
    path("", ViewIndex.as_view(), name="index"),
    path("login", ViewLogin.as_view(), name="login"),
    path("register", ViewRegister.as_view(), name="register"),
    path("logout", ViewLogout.as_view(), name="logout"),
    path("add_friend", ViewAddFriend.as_view(), name="add_friend"), 
    path("<str:room_name>", ViewRoom.as_view(), name="room")
]
