"""Permission checking for use in chat"""
# pylint: disable=unused-argument,fixme
# TODO: Implement permissions for chat
from base.models.ifuser import IFUser
from chat.models import Room


def check_permission(room: Room, user: IFUser) -> bool:
    """Checks if user has permission for said room"""
    return True
