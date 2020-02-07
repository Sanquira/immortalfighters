"""
Module containing all messages that can happen in chat application
"""

from datetime import datetime
from typing import List

from chat.components.serializables import ChatUser, Serializable


class BaseMessage(Serializable):
    """Generic message, common ancestor of all other messages"""

    def __init__(self, message_type: str, time: int = -1, **kwargs) -> None:
        super().__init__(type=message_type, **kwargs)
        if isinstance(time, int) and time > 0:
            self.time = datetime.fromtimestamp(time)
        else:
            self.time = datetime.now()

    # pylint: disable=unused-argument,no-self-use
    def is_valid(self, consumer: 'ChatConsumer') -> bool:
        """Checks if message that client sent is valid"""
        return True

    def to_dict(self) -> dict:
        return {"time": self.time.timestamp(), **super().to_dict()}


class ChatMessage(BaseMessage):
    """Chat text message"""

    def __init__(self, message: str, user: str, time: int = -1) -> None:
        super().__init__(message_type="chat_message", message=message, user=user, time=time)

    def is_valid(self, consumer: 'ChatConsumer'):
        return isinstance(self.get("message"), str) \
               and self.get("message").strip()


class PrivateMessage(BaseMessage):
    """Chat message addressed only to a specific user"""

    def __init__(self, message: str, user: str, target_user: str, time: int = -1) -> None:
        super().__init__(message_type="private_message", message=message, user=user, target_user=target_user, time=time)

    def is_valid(self, consumer: 'ChatConsumer'):
        return isinstance(self.get("message"), str) \
               and isinstance(self.get("target_user"), str) \
               and self.get("message").strip()


class JoinChannelMessage(BaseMessage):
    """
    Message that is sent to user after a successful join.
    Contains all users that are in the room before this tried to connect.
    """

    def __init__(self, users: List[ChatUser], user: ChatUser) -> None:
        super().__init__(message_type="join_channel")
        self.users = users
        self.user = user

    def to_dict(self):
        new_dict = {
            "user": self.user.to_dict(),
            "users": list(map(lambda x: x.to_dict(), self.users))
        }
        return {**new_dict, **super().to_dict()}


class UserJoinChannelMessage(BaseMessage):
    """Message indicating new user has joined the channel"""

    def __init__(self, user, time: int = -1) -> None:
        super().__init__(message_type="user_join_channel", time=time, user=user)
        self.user = user


class UserLeaveChannelMessage(BaseMessage):
    """Message indicating user has left the channel"""

    def __init__(self, user: str, time: int = -1) -> None:
        super().__init__(message_type="user_leave_channel", user=user, time=time)


# Errors

class ErrorMessage(BaseMessage):
    """Generic error, common ancestor of all errors"""

    def __init__(self, error_type: str, **kwargs) -> None:
        super().__init__(message_type="error", error_type=error_type, **kwargs)


class RoomUnavailableError(ErrorMessage):
    """
    Signals that user cannot connect into room, it either doesn't exists or he doesn't have permissions for that room
    """

    def __init__(self, room: str) -> None:
        super().__init__(error_type="room_unavailable", room=room)


class UserAlreadyConnectedError(ErrorMessage):
    """Signals that user with same username is already connected"""

    def __init__(self, user: str) -> None:
        super().__init__(error_type="user_already_connected", user=user)


class InvalidMessageError(ErrorMessage):
    """Signals that the message not valid"""

    def __init__(self, message: str) -> None:
        super().__init__(error_type="invalid_message", message=message)
