from django.urls import path

from account.views import ViewLogin, ViewRegister, ViewLogout
from chat_app.views import ( 
    ViewDeletePending, ViewDeleteSent, ViewDeleteFriend, 
    ViewIndex, ViewChatRoom, ViewAddFriend, 
    ViewAddChatRoom
)

app_name = "chat_app"

urlpatterns = [
    path("", ViewIndex.as_view(), name="index"),
    path("login", ViewLogin.as_view(), name="login"),
    path("register", ViewRegister.as_view(), name="register"),
    path("logout", ViewLogout.as_view(), name="logout"),
    path("add_friend", ViewAddFriend.as_view(), name="add_friend"),
    path("add_room", ViewAddChatRoom.as_view(), name="add_room"),
    path("<int:chatroom_id>", ViewChatRoom.as_view(), name="room"),
    path("delete_friend/<int:chatroom_users_id>", ViewDeleteFriend.as_view(), name="del_friend"),
    path("delete_pending>/<int:chatroom_users_id>", ViewDeletePending.as_view(), name="del_pending"),
    path("delete_sent>/<int:chatroom_users_id>", ViewDeleteSent.as_view(), name="del_sent"),
]
