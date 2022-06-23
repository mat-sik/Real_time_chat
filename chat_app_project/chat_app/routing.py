from django.urls import re_path

from chat_app.consumers import ChatRoomConsumer

ws_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatRoomConsumer.as_asgi()), # type: ignore
]