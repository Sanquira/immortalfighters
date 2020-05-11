"""
Module containing serializable helper classes
"""
import typing

from utils.serializable import Serializable

if typing.TYPE_CHECKING:
    from base.models.ifuser import IFUser


# pylint: disable=too-few-public-methods
class ChatUser(Serializable):
    """Serializable version of IFUser, without all the unnecessary fields"""

    def __init__(self, user: 'IFUser') -> None:
        self.name = user.username
        self.color = user.chat_color
