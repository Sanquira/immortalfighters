"""
Module containing Websocket consumers for chat application
"""

import logging
from typing import Dict

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from base.models.ifuser import IFUser
from chat.components.messages import ChatMessage, RoomUnavailableError, ErrorMessage, UserJoinChannelMessage, \
    UserLeaveChannelMessage, PrivateMessage, InvalidMessageError, BaseMessage, UserAlreadyConnectedError, \
    JoinChannelMessage
from chat.components.serializables import ChatUser
from chat.models import Room
from chat.views import check_permission


class ChatConsumer(AsyncJsonWebsocketConsumer):
    """
    Async JSON Consumer for chat application
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connected = False

    logger = logging.getLogger(__name__)
    user_message_types = {
        "chat_message": ChatMessage,
        "private_message": PrivateMessage,
    }
    server_message_types = {
        **user_message_types,
        "user_join_channel": UserJoinChannelMessage,
        "user_leave_channel": UserLeaveChannelMessage
    }
    users = {}

    # pylint: disable=attribute-defined-outside-init
    async def connect(self):
        """
        Method that handles connection of the new client to the server
        """
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope["user"]
        message = await self.pre_join()
        await self.accept()
        if isinstance(message, ErrorMessage):
            await self.raise_error(message, close=True)

        else:
            self.users.setdefault(self.room_name, {})[self.user.username] = self.user
            self.connected = True
            await self.send_json(
                message.to_dict()
            )

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.channel_layer.group_send(
                self.room_group_name,
                UserJoinChannelMessage(user=message.user.to_dict()).to_dict()
            )

    async def disconnect(self, code):
        """Disconnects user from room, if he was properly connected"""
        if self.connected:
            self.connected = False
            self.room_users().pop(self.user.username, {})

            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

            await self.channel_layer.group_send(
                self.room_group_name,
                UserLeaveChannelMessage(self.user.username).to_dict()
            )

    async def receive_json(self, content, **kwargs):
        """Receive message from WebSocket"""
        if self.connected:
            content['user'] = self.user.username
            message = await self.parse_client_message(content)
            if message is not None:
                # Re-send message to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    message.to_dict()
                )

    async def chat_message(self, event):
        """Receive message from room group"""
        message = self.parse_server_message(event)

        # Send message to WebSocket
        await self.send_json(message.to_dict())

    async def user_join_channel(self, event):
        """Receive join_channel message from room group"""
        message = self.parse_server_message(event)

        # Send message to WebSocket
        await self.send_json(message.to_dict())

    # Receive leave_channel message from room group
    async def user_leave_channel(self, event):
        """Receive leave_channel message from room group"""
        message = self.parse_server_message(event)

        # Send message to WebSocket
        await self.send_json(message.to_dict())

    async def private_message(self, event):
        """Receive private message from room group"""
        message = self.parse_server_message(event)

        if message.get("target_user") != self.user.username:
            return

        # Send message to WebSocket
        await self.send_json(message.to_dict())

    async def raise_error(self, error: ErrorMessage, close: bool = False):
        """Raises error for the client and closes socket afterwards"""
        self.logger.error("[Websocket] %s", error)
        await self.send_json(
            error.to_dict(),
            close=close)
        return False

    def parse_server_message(self, data) -> BaseMessage:
        """Parses message that it received from the channel layer group"""
        message_type = data.pop("type")
        return self.server_message_types[message_type](**data)

    async def parse_client_message(self, data):
        """Parses message that the client sent"""
        if 'type' not in data:
            await self.raise_error(InvalidMessageError("No type specified"))
            return None

        message_type = data.pop("type")
        if message_type not in self.user_message_types:
            await self.raise_error(InvalidMessageError("Invalid type specified"))
            return None

        try:
            message = self.user_message_types[message_type](**data)
        except TypeError:
            await self.raise_error(InvalidMessageError("Invalid parameters for type %s" % message_type))
            return None

        if not message.is_valid(self):
            await self.raise_error(InvalidMessageError("Invalid message for type %s" % message_type))
            return None

        return message

    @database_sync_to_async
    def pre_join(self) -> BaseMessage:
        """Checks that user can connect to the room"""
        if not Room.objects.exists():
            return RoomUnavailableError(room=self.room_name)

        room = Room.objects.get(name=self.room_name)
        if not check_permission(room, self.user):
            return RoomUnavailableError(room=self.room_name)

        if self.username_in_room():
            return UserAlreadyConnectedError(user=self.user.username)

        users = list(map(ChatUser, self.room_users().values()))
        return JoinChannelMessage(users, ChatUser(self.user))

    def room_users(self) -> Dict[str, IFUser]:
        """Returns all users that are connected in the room"""
        return self.users.setdefault(self.room_name, {})

    def username_in_room(self):
        """Checks if some user with same username is in room"""
        return self.user.username in self.room_users()
