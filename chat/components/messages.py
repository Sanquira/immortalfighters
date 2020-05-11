"""
Module containing all messages that can happen in chat application
"""

from datetime import datetime
from typing import List

import typing

from chat.components.serializables import Serializable

if typing.TYPE_CHECKING:
    from chat.consumers import ChatConsumer
    from chat.components.serializables import ChatUser


class BaseMessage(Serializable):
    """Generic message, common ancestor of all other messages"""

    def __init__(self, message_type: str, time: int = -1) -> None:
        self.type = message_type
        self.time = datetime.now()
        if isinstance(time, int) and time > 0:
            self.time = datetime.fromtimestamp(time)

    # pylint: disable=unused-argument,no-self-use
    def is_valid(self, consumer: 'ChatConsumer') -> bool:
        """Checks if message that client sent is valid"""
        return True

    def to_dict(self) -> dict:
        return {
            **super().to_dict(),
            "time": self.time.timestamp()
        }


class ChatMessage(BaseMessage):
    """Chat text message"""

    def __init__(self, message: str, user: str, time: int = -1) -> None:
        super().__init__(message_type="chat_message", time=time)
        self.message = message
        self.user = user

    def is_valid(self, consumer: 'ChatConsumer'):
        return isinstance(self.message, str) and self.message.strip()


class PrivateMessage(BaseMessage):
    """Chat message addressed only to a specific user"""

    def __init__(self, message: str, user: str, target_user: str, time: int = -1) -> None:
        super().__init__(message_type="private_message", time=time)
        self.message = message
        self.user = user
        self.target_user = target_user

    def is_valid(self, consumer: 'ChatConsumer'):
        return isinstance(self.message, str) and isinstance(self.target_user, str) and self.message.strip()


class JoinChannelMessage(BaseMessage):
    """
    Message that is sent to user after a successful join.
    Contains all users that are in the room before this tried to connect.
    """

    def __init__(self, users: List['ChatUser'], user: 'ChatUser', history: List[str]) -> None:
        super().__init__(message_type="join_channel")
        self.history = history
        self.users = users
        self.user = user

    def to_dict(self):
        return {
            **super().to_dict(),
            "user": self.user.to_dict(),
            "users": list(map(lambda x: x.to_dict(), self.users))
        }


class UserJoinChannelMessage(BaseMessage):
    """Message indicating new user has joined the channel"""

    def __init__(self, user, time: int = -1) -> None:
        super().__init__(message_type="user_join_channel", time=time)
        self.user = user


class UserLeaveChannelMessage(BaseMessage):
    """Message indicating user has left the channel"""

    def __init__(self, user: str, time: int = -1) -> None:
        super().__init__(message_type="user_leave_channel", time=time)
        self.user = user


# Errors

class ErrorMessage(BaseMessage):
    """Generic error, common ancestor of all errors"""

    def __init__(self, error_type: str) -> None:
        super().__init__(message_type="error")
        self.error_type = error_type


class RoomUnavailableError(ErrorMessage):
    """
    Signals that user cannot connect into room, it either doesn't exists or he doesn't have permissions for that room
    """

    def __init__(self, room: str) -> None:
        super().__init__(error_type="room_unavailable")
        self.room = room


class UserAlreadyConnectedError(ErrorMessage):
    """Signals that user with same username is already connected"""

    def __init__(self, user: str) -> None:
        super().__init__(error_type="user_already_connected")
        self.user = user


class InvalidMessageError(ErrorMessage):
    """Signals that the message not valid"""

    def __init__(self, message: str) -> None:
        super().__init__(error_type="invalid_message")
        self.message = message
