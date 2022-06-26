from django.urls import re_path

from chat_app.consumers import ChatRoomConsumer

ws_urlpatterns = [
    re_path(r"ws/chat/(?P<chatroom_id>\d+)/$", ChatRoomConsumer.as_asgi()), # type: ignore
]