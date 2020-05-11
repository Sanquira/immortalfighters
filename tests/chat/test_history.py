"""
Tests that verify that chat is handling history correctly
"""
# pylint: disable=redefined-outer-name
import pytest

from chat.components.messages import UserJoinChannelMessage, PrivateMessage, ChatMessage
from tests.chat.utils import next_message, is_valid_message_with_type, create_history_record, \
    valid_history


@pytest.fixture
def room3(room3, user2, user1, admin1):
    """Create history for room 3"""
    create_history_record(room3,
                          UserJoinChannelMessage(user=user1.username, time=1))
    create_history_record(room3,
                          UserJoinChannelMessage(user=user2.username, time=2))
    create_history_record(room3,
                          PrivateMessage(user=admin1.username, target_user=user1.username, time=3, message="Test"))
    create_history_record(room3,
                          ChatMessage(user=admin1.username, time=4, message="Test"))
    create_history_record(room3,
                          ChatMessage(user=user1.username, time=5, message="Test"))
    return room3


@pytest.fixture
def room2(room2, user2, user1):
    """Create history for room 2"""
    create_history_record(room2,
                          UserJoinChannelMessage(user=user1.username, time=1))
    create_history_record(room2,
                          ChatMessage(user=user2.username, time=2, message="Test"))
    return room2


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_history_with_pm(user_communicator, user1, room3):
    """Tests that you will correctly receive private messages in history if user is involved"""
    communicator = await user_communicator(user1, room3)
    connected, __ = await communicator.connect()

    assert connected
    message = await next_message(communicator)
    assert is_valid_message_with_type(message, "join_channel")
    assert valid_history(message["history"], 3, ["private_message", "chat_message", "chat_message"])


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_history_without_pm(user_communicator, user2, room3):
    """Tests that when the private message didn't involve the use that they are not included in history"""
    communicator = await user_communicator(user2, room3)
    connected, __ = await communicator.connect()

    assert connected
    message = await next_message(communicator)
    assert is_valid_message_with_type(message, "join_channel")
    assert valid_history(message["history"], 3, ["user_join_channel", "chat_message", "chat_message"])


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_different_room_history(user_communicator, user2, room1, room2):
    """Tests that different room have different histories"""
    communicator = await user_communicator(user2, room2)
    connected, __ = await communicator.connect()

    assert connected
    message = await next_message(communicator)
    assert is_valid_message_with_type(message, "join_channel")
    assert valid_history(message["history"], 2, ["user_join_channel", "chat_message"])

    await communicator.disconnect()

    communicator = await user_communicator(user2, room1)
    connected, __ = await communicator.connect()

    assert connected
    message = await next_message(communicator)
    assert is_valid_message_with_type(message, "join_channel")
    assert valid_history(message["history"], 0)
