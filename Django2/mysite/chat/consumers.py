# chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        #Obtains 'room_name' parameter from URL route in chat/routing.py
        # that opened the WebSocket connection to the consumer.
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        #Constructs Channels group name directly from user-specified 
        # room name, no quoting or escaping.
        #Group names may only contain alphanumerics, hyphens, underscores, or periods
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        #Only ASCII alphanumerics, hyphens, and period room names permitted 
        #Limited to a maximum length of 100 (default backend)
        #Constructs group name directly from room name
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        #Accepts WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

