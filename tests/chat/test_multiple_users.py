"""
Tests more complicated situations involving multiple users connected
"""
import pytest

from tests.chat.utils import ignore_messages, next_message, is_valid_message_with_type, next_message_of_type


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_login_workflow(user_communicator, user1, user2, room1):
    """
    Tests that login workflow works as expected

     Communication:
        user1 -> Connect
        user1 -> Receives JoinChannel message, with 0 users
        user1 -> Receives UserJoinChannel message containing himself

        user2 -> Connect
        user2 -> Receives JoinChannel message, with 1 user (user1)
        user2 -> Receives UserJoinChannel message containing himself

        user1 -> Receives UserJoinChannel message containing user2
    """
    communicator = user_communicator(user1, room1)
    connected, __ = await communicator.connect()
    assert connected

    # Successful login message
    message = await next_message(communicator)
    assert is_valid_message_with_type(message, "join_channel")
    assert len(message["users"]) == 0

    message = await next_message(communicator)
    assert is_valid_message_with_type(message, "user_join_channel")
    assert message["user"]["name"] == user1.username

    communicator2 = user_communicator(user2, room1)
    connected, __ = await communicator2.connect()
    assert connected

    # Login message with all existing users
    message = await next_message(communicator2)
    assert is_valid_message_with_type(message, "join_channel")
    assert len(message["users"]) == 1
    assert message["users"][0]["name"] == user1.username
    assert message["user"]["name"] == user2.username

    message = await next_message(communicator)
    assert is_valid_message_with_type(message, "user_join_channel")
    assert message["user"]["name"] == user2.username

    message = await next_message(communicator2)
    assert is_valid_message_with_type(message, "user_join_channel")
    assert message["user"]["name"] == user2.username


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_user_disconnect(connected_communicator, user1, user2, room1):
    """
    Tests user disconnecting from the server

     Communication:
        user1 -> Connect
        user2 -> Connect
        user2 -> Disconnect
        user1 -> Receives UserLeaveChannel message
    """
    communicator = await connected_communicator(user1, room1)
    communicator2 = await connected_communicator(user2, room1, autoclean=False)

    # Ignore user_join_channel
    await ignore_messages(communicator, 1)

    await communicator2.disconnect()

    message, ignored_messages = await next_message_of_type(communicator, "user_leave_channel")
    assert ignored_messages == 0
    assert message["user"] == user2.username


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_valid_chat_message(connected_communicator, user1, user2, room1):
    """
    Tests user disconnecting from the server

     Communication:
        user1 -> Connect
        user2 -> Connect

        user1 -> Sends ChatMessage
        user1 -> Receives ChatMessage
        user2 -> Receives ChatMessage
    """
    communicator = await connected_communicator(user1, room1)
    communicator2 = await connected_communicator(user2, room1)

    await communicator.send_json_to({
        "type": "chat_message",
        "message": "Hi"
    })

    message1, _ = await next_message_of_type(communicator, "chat_message")
    message2, _ = await next_message_of_type(communicator2, "chat_message")
    assert message1["user"] == user1.username
    assert message2["message"] == "Hi"


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_simple_pm_message(connected_communicator, user1, user2, room1):
    """
    Tests sending simple private message

     Communication:
        user1 -> Connect
        user2 -> Connect

        user1 -> Sends PrivateMessage to User2
        user2 -> Receives PrivateMessage
        user1 -> Receives nothing
    """
    communicator = await connected_communicator(user1, room1)
    communicator2 = await connected_communicator(user2, room1)

    await ignore_messages(communicator, 1)
    await communicator.send_json_to({
        "type": "private_message",
        "message": "Hi",
        "target_user": user2.username
    })

    assert await communicator.receive_nothing(timeout=1)

    message, _ = await next_message_of_type(communicator2, "private_message")
    assert message["user"] == user1.username
    assert message["target_user"] == user2.username
    assert message["message"] == "Hi"


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_invalid_user_pm_message(connected_communicator, user1, user2, room1):
    """
    Tests sending private messages to non-existing users

     Communication:
        user1 -> Connect
        user2 -> Connect

        user1 -> Sends PrivateMessage to user noone
        user1 -> Receives nothing
        user2 -> Receives nothing
    """
    communicator = await connected_communicator(user1, room1)
    communicator2 = await connected_communicator(user2, room1)

    await ignore_messages(communicator, 1)
    await communicator.send_json_to({
        "type": "private_message",
        "message": "Hi",
        "target_user": "noone"
    })

    assert await communicator.receive_nothing()
    assert await communicator2.receive_nothing()


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_pm_message(connected_communicator, user1, user2, admin_user, room1):
    """
    Tests sending private messages between 3 people

     Communication:
        user1 -> Connect
        user2 -> Connect
        admin_user -> Connect

        user1 -> Sends PrivateMessage to admin_user
        user1 -> Receives nothing
        user2 -> Receives nothing
        admin_user -> Receives PrivateMessage
    """
    communicator = await connected_communicator(user1, room1)

    communicator2 = await connected_communicator(user2, room1)

    communicator3 = await connected_communicator(admin_user, room1)

    await ignore_messages(communicator, 2)
    await ignore_messages(communicator2, 1)
    await communicator.send_json_to({
        "type": "private_message",
        "message": "Hi",
        "target_user": admin_user.username
    })

    assert await communicator.receive_nothing()
    assert await communicator2.receive_nothing()

    message, _ = await next_message_of_type(communicator3, "private_message")
    assert message["user"] == user1.username
    assert message["target_user"] == admin_user.username
    assert message["message"] == "Hi"
