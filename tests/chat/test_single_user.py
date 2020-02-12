"""
Tests server interaction with only one user present
"""

import pytest
from channels.testing import WebsocketCommunicator

from tests.chat.utils import is_error, is_valid_message_with_type, next_message, ignore_messages, next_error, \
    next_message_of_type, valid_history
from immortalfighters.routing import application


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_connect_anonymous():
    """
    Tests that you need to be logged in to use chat

    Communication:
        Anon -> TryConnect
        Anon -> NotConnected
    """
    communicator = WebsocketCommunicator(application, "ws/chat/testroom/")
    connected, _ = await communicator.connect()

    assert not connected

    # Close
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_connect_logged_in(user_communicator, user1, room1):
    """
    Tests that you can connect to the room

    Communication:
        User1 -> Connects
        User1 -> Receives join_channel
        User1 -> Receives user_join_channel
    """
    communicator = user_communicator(user1, room1)
    connected, __ = await communicator.connect()

    assert connected
    message = await next_message(communicator)
    assert is_valid_message_with_type(message, "join_channel")
    assert len(message["users"]) == 0
    assert len(message["history"]) == 0
    assert message["user"]["name"] == user1.username

    message = await next_message(communicator)
    assert is_valid_message_with_type(message, "user_join_channel")
    assert message["user"]["name"] == user1.username


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_non_existing_room(user_communicator, user1, non_existing_room):
    """
    Tests that you cannot connect to nonexistent room

    Communication:
        User1 -> TryConnect
        User1 -> Room Unavailable error
    """
    communicator = user_communicator(user1, non_existing_room)
    connected, __ = await communicator.connect()
    assert connected

    message = await next_message(communicator)
    assert is_error(message, "room_unavailable")


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_already_connected(user_communicator, user1, room1):
    """
    Tests that you cannot connect if user is already connected

    Communication:
        User1 -> Connects
        User2 -> TryConnect
        User2 -> User Already Connected error
        User1 -> No join messages
    """
    communicator = user_communicator(user1, room1)
    await communicator.connect()

    await ignore_messages(communicator, 2)

    communicator2 = user_communicator(user1, room1)
    await communicator2.connect()

    message = await next_message(communicator2)
    assert is_error(message, "user_already_connected")

    assert await communicator.receive_nothing()

    await communicator.send_json_to({
        "type": "chat_message",
        "message": "Hi"
    })
    message = await next_message(communicator)
    assert message["message"] == "Hi"


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_users_after_disconnect(user_communicator, user1, user2, room1):
    """
    Tests that after user disconnects, the number of users connected on the server is 0

    Communication:
        User1 -> Connects
        User1 -> Disconnects

        User2 -> Connects
        Number of already connected users == 0
    """
    communicator = user_communicator(user1, room1, autoclean=False)
    await communicator.connect()
    await communicator.disconnect()

    communicator2 = user_communicator(user2, room1)
    await communicator2.connect()

    message = await next_message(communicator2)
    assert is_valid_message_with_type(message, "join_channel")
    assert len(message["users"]) == 0
    assert valid_history(message["history"], 2, ["user_join_channel", "user_leave_channel"])
    assert message["user"]["name"] == user2.username


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_incorrect_type(connected_communicator, user1, room1):
    """
    Tests that user cannot send messages with invalid type

    Communication:
        User1 -> Connects

        User1 -> Send message with incorrect type
        User1 -> Invalid Message error
    """
    communicator = await connected_communicator(user1, room1)

    await communicator.send_json_to({
        "type": "null"
    })

    message, _ = await next_error(communicator)
    assert is_error(message, "invalid_message")


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_no_type_specifed(connected_communicator, user1, room1):
    """
    Tests that user cannot send messages without type

    Communication:
        User1 -> Connects

        User1 -> Send message without type
        User1 -> Invalid Message error
    """
    communicator = await connected_communicator(user1, room1)

    await communicator.send_json_to({
        "message": "Hey there!"
    })

    message, _ = await next_error(communicator)
    assert is_error(message, "invalid_message")


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_invalid_chat_message(connected_communicator, user1, room1):
    """
    Tests that user cannot send invalid chat message

    Communication:
        User1 -> Connects

        User1 -> Sends chat message with empty string
        User1 -> Invalid Message error
    """
    communicator = await connected_communicator(user1, room1)

    await communicator.send_json_to({
        "type": "chat_message",
        "message": ""
    })

    message, _ = await next_error(communicator)
    assert is_error(message, "invalid_message")

    await communicator.send_json_to({
        "type": "chat_message",
        "message": "   "
    })

    message, _ = await next_error(communicator)
    assert is_error(message, "invalid_message")


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_valid_chat_message(connected_communicator, user1, room1):
    """
    Tests that user can send valid chat messages

    Communication:
        User1 -> Connects
        User1 -> Sends chat message
        User1 -> Receives chat message back
    """
    communicator = await connected_communicator(user1, room1)

    await communicator.send_json_to({
        "type": "chat_message",
        "message": "Hi"
    })

    message, ignored_messages = await next_message_of_type(communicator, "chat_message")
    assert message["user"] == user1.username
    assert message["message"] == "Hi"
    assert ignored_messages == 0


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_invalid_private_message(connected_communicator, user1, room1):
    """
    Tests that user cannot send invalid private messages

    Communication:
        User1 -> Connects

        User1 -> Sends PM without target
        User1 -> Invalid Message error

        User1 -> Sends PM to itself
        User1 -> Invalid Message error
    """
    communicator = await connected_communicator(user1, room1)

    await communicator.send_json_to({
        "type": "private_message",
        "message": "Hi"
    })

    message, _ = await next_error(communicator)
    assert is_error(message, "invalid_message")

    await communicator.send_json_to({
        "type": "private_message",
        "message": "Hi",
        "user": user1.username
    })

    message, _ = await next_error(communicator)
    assert is_error(message, "invalid_message")
