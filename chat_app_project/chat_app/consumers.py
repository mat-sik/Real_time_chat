import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.shortcuts import get_object_or_404

from chat_app.models import Message, ChatRoom


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        kwargs = self.scope.get("url_route").get("kwargs")
        self.chatroom_id = kwargs.get("chatroom_id")
        self.room_group_name = f"chatroom_{self.chatroom_id}"

        self.times_loaded = 1

        self.chatroom_obj = await self.get_chatroom(self.chatroom_id)

        await self.channel_layer.group_add( #type: ignore
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard( #type: ignore
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def get_chatroom(self, chatroom_id):
        return get_object_or_404(ChatRoom, id=chatroom_id)

    @database_sync_to_async
    def create_message(self, message):
        Message.objects.create(
            text=message,
            user=self.scope["user"],
            chatroom=self.chatroom_obj
        )

    @database_sync_to_async
    def get_messages(self):
        end_bound = self.times_loaded*30
        return list(
            Message.objects.filter(
                chatroom=self.chatroom_obj
            ).order_by("-pub_date")[end_bound-30:end_bound].values(
                "user__username",
                "text"
            )
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")
        username = text_data_json.get("username")

        if text_data_json.get("load"):
            self.times_loaded += 1

            loaded_messages = await self.get_messages()
            await self.send(
                text_data=json.dumps(
                    {
                    "load": 1,
                    "loaded_messages": loaded_messages
                    }
                )
            )
        else:
            await self.create_message(message)

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
