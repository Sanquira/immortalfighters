"""
Tests that server successfully rejects invalid messages
"""
import pytest

from tests.chat.utils import next_error, is_error, next_message_of_type


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_number_type(connected_communicator, user1, room1):
    """Tests sending message with numeric type"""
    communicator = await connected_communicator(user1, room1)

    await communicator.send_json_to({
        "type": 187
    })

    message, _ = await next_error(communicator)
    assert is_error(message, "invalid_message")


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_string_time(connected_communicator, user1, room1):
    """
    Tests sending message with string time.
    The time should be ignored by server and server should use his own time.
    """
    communicator = await connected_communicator(user1, room1)

    await communicator.send_json_to({
        "type": "chat_message",
        "message": "Hi",
        "time": "tetete"
    })

    message, _ = await next_message_of_type(communicator, "chat_message")
    assert message["time"] != "tetete"


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_time_override(connected_communicator, user1, room1):
    """
    Tests that you cannot send message with a specific time.
    The time should be ignored by server and server should use his own time.
    """
    communicator = await connected_communicator(user1, room1)

    await communicator.send_json_to({
        "type": "chat_message",
        "message": "Hi",
        "time": 70
    })

    message, _ = await next_message_of_type(communicator, "chat_message")
    assert message["time"] != 70


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_int_message(connected_communicator, user1, room1):
    """Tests that you cannot send chat_message with integer message"""
    communicator = await connected_communicator(user1, room1)

    await communicator.send_json_to({
        "type": "chat_message",
        "message": 10
    })

    message, _ = await next_error(communicator)
    assert is_error(message, "invalid_message")


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_user_override(connected_communicator, user1, room1):
    """Tests that you cannot inject user who sent the message"""
    communicator = await connected_communicator(user1, room1)

    await communicator.send_json_to({
        "type": "chat_message",
        "message": "test",
        "user": "tutu"
    })

    message, _ = await next_message_of_type(communicator, "chat_message")
    assert message["user"] == user1.username


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_int_target_user(connected_communicator, user1, room1):
    """Tests that you cannot send PM to user specified by an integer"""
    communicator = await connected_communicator(user1, room1)

    await communicator.send_json_to({
        "type": "private_message",
        "message": "test",
        "target_user": -5
    })

    message, _ = await next_error(communicator)
    assert is_error(message, "invalid_message")
