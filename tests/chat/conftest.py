"""
Conftest for all chat tests
"""
# pylint: disable=redefined-outer-name,unused-argument
import pytest
from asgiref.sync import sync_to_async
from channels.testing import WebsocketCommunicator
from django.test import Client

from base.models.ifuser import IFUser
from chat.models import Room
from tests.application import application
from tests.chat.utils import ignore_messages


@pytest.fixture
def room1(transactional_db):
    """Test room one"""
    room = Room.objects.create(name="test_room1")
    room.save()
    return room


@pytest.fixture
def room2(transactional_db):
    """Test room two"""
    room = Room.objects.create(name="test_room2")
    room.save()
    return room


@pytest.fixture
def room3(transactional_db):
    """Test room number three"""
    room = Room.objects.create(name="test_room3")
    room.save()
    return room


@pytest.fixture
def non_existing_room():
    """Not persisted room"""
    return Room(name="nope_room")


@pytest.fixture
async def user_communicator(settings):
    """Return communicator for specific user and room"""
    communicators = []
    client = Client()
    force_login = sync_to_async(client.force_login)

    async def _connector(user: IFUser, room: Room, autoclean: bool = True) -> WebsocketCommunicator:
        nonlocal communicators
        await force_login(user)
        scn = settings.SESSION_COOKIE_NAME
        cookies = (b'cookie', '{}={}'.format(scn, client.cookies[scn].value).encode())
        communicator = WebsocketCommunicator(application, "/ws/chat/%s/" % room.name, headers=[cookies])
        if autoclean:
            communicators.append(communicator)
        return communicator

    yield _connector

    for communicator in communicators:
        await communicator.disconnect()


@pytest.fixture
async def connected_communicator(user_communicator, additional_messages: int = 0):
    """Return communicator for specific user and room with filtered initial login messages"""

    async def _connector(user, room, autoclean=True) -> WebsocketCommunicator:
        communicator = await user_communicator(user, room, autoclean)
        await communicator.connect()
        await ignore_messages(communicator, 2 + additional_messages)

        return communicator

    yield _connector
