# chat/consumers.py
import logging

from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):
    logger = logging.getLogger(__name__)

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

        if self.validate(text_data_json):
            text_data_json['user'] = self.user.username
            # Re-send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                text_data_json
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
            'user': user
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

    def raise_error(self, error):
        self.logger.warning("[Websocket] %s" % error)
        return False

    def require(self, data, *args):
        for arg in args:
            if arg not in data:
                return self.raise_error("Parameter %s is required for message of type %s" % (arg, data["type"]))
            if data[args] == "":
                return self.raise_error("Parameter %s must be not null for message of type %s" % (arg, data["type"]))
        return True

    def validate(self, data):
        if 'type' not in data:
            return self.raise_error("No type specified")

        message_type = data["type"]
        if message_type == 'chat_message':
            return self.require(data, "message")
        elif message_type == "private_message":
            return self.require(data, "message", "target")
        else:
            return self.raise_error("Type %s is unsupported" % message_type)
