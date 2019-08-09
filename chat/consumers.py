# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope["user"]

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'join_channel',
                'user': self.user.username
            }
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'leave_channel',
                'user': self.user.username
            }
        )

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if 'type' not in text_data_json:
            return

        message = text_data_json['message']
        message_type = text_data_json['type']

        msg = {
                'type': message_type,
                'message': message,
                'user': self.user.username
            }
        if message_type == "private_message":
            if 'target' not in text_data_json:
                return
            msg['target'] = text_data_json['target']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            msg
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user = event['user']

        if message == "":
            return

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': "message",
            'message': message,
            'user': user
        }))

    # Receive join_channel message from room group
    async def join_channel(self, event):
        user = event['user']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': "join_channel",
            'user':  user
        }))

    # Receive leave_channel message from room group
    async def leave_channel(self, event):
        user = event['user']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': "leave_channel",
            'user': user
        }))

    # Receive pm from room group
    async def private_message(self, event):
        message = event['message']
        user = event['user']
        target_user = event['target_user']

        if message == "" or target_user != self.user.username:
            return

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': "pm",
            'message': message,
            'user': user
        }))
