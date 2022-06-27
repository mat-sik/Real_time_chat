import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from chat_app.models import Message


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        kwargs = self.scope.get("url_route").get("kwargs")
        self.chatroom_id = kwargs.get("chatroom_id")
        self.room_group_name = f"chatroom_{self.chatroom_id}"

        await self.channel_layer.group_add( #type: ignore
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    @database_sync_to_async
    def get_messages(self, chatroom_id):
        return Message.objects.filter(chatroom_id=chatroom_id)

    async def disconnect(self):
        await self.channel_layer.group_discard( #type: ignore
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")
        username = text_data_json.get("username")

        await self.channel_layer.group_send( #type: ignore
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
            }
        )

    async def chat_message(self, event):
        message = event.get("message")
        username = event.get("username")

        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "username": username,
                }
            )
        )
