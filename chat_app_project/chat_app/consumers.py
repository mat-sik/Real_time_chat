import json

from channels.generic.websocket import AsyncWebsocketConsumer

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        kwargs = self.scope.get("url_route").get("kwargs")
        self.room_name = kwargs.get("room_name")
        self.room_group_name = f"chat_{self.room_name}"

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

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")
        user_name = text_data_json.get("user_name")

        await self.channel_layer.group_send( #type: ignore
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "user_name": user_name,
            }
        )

    async def chat_message(self, event):
        message = event.get("message")
        user_name = event.get("user_name")

        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "user_name": user_name,
                }
            )
        )
