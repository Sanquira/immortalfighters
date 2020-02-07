"""
Module containing serializable helper classes
"""
from base.models.ifuser import IFUser


class Serializable:
    """Any serializable object"""

    def __init__(self, **kwargs) -> None:
        self.fields = {**kwargs}

    def to_dict(self):
        """Serializes object into dict"""
        return self.fields

    def add(self, **kwargs):
        """Adds additional fields into object"""
        self.fields = {**self.fields, **kwargs}

    def get(self, key):
        """Returns value from object"""
        return self.fields[key]


class ChatUser(Serializable):
    """Serializable version of IFUser, without all the unnecessary fields"""

    def __init__(self, user: IFUser) -> None:
        super().__init__(name=user.username, color=user.chat_color)
