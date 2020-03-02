"""Permission checking for use in chat"""
from base.models.ifuser import IFUser
from chat.models import Room


def check_permission(room: Room, user: IFUser) -> bool:
    """Checks if user has permission for said room"""
    permission = room.permission
    if permission:
        return user.has_perm(permission)
    return True


def list_available_rooms(user: IFUser):
    """Lists all rooms available to a specific user"""
    return list(filter(lambda room: not room.permission or check_permission(room, user), Room.objects.all()))
