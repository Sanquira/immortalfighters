"""
The top level conftest for testing Immortal fighters, contains test users and chars
"""

# pylint: disable=redefined-outer-name,unused-argument
import pytest

from base.models.character import Character
from base.models.ifuser import IFUser


@pytest.fixture
def user1(transactional_db):
    """First test user"""
    user = IFUser.objects.create_user(username="User", email="fluffy.pedo.bear@lol.net", password="user")
    user.save()
    return user


@pytest.fixture
def user2(transactional_db):
    """Second test user"""
    user = IFUser.objects.create_user(username="User2", email="pink.fluffy@unicorn.eu", password="user")
    user.save()
    return user


@pytest.fixture
def admin1(transactional_db):
    """First test admin"""
    user = IFUser.objects.create_superuser(username="Admin", email="kiss.my.cheeks@lol.net", password="admin")
    user.save()
    return user


@pytest.fixture
def admin_char1(admin1):
    """First admin character"""
    char = Character(owner=admin1, name="Kitten", health=0, max_health=0)
    char.save()
    return char


@pytest.fixture
def admin_char2(admin1):
    """Second admin character"""
    char = Character(owner=admin1, name="Shitten", health=0, max_health=0)
    char.save()
    return char


@pytest.fixture
def user_char1(user1):
    """First user character"""
    char = Character(owner=user1, name="Dog", health=0, max_health=0)
    char.save()
    return char


@pytest.fixture
def user_char2(user1):
    """Second user character"""
    char = Character(owner=user1, name="Shog", health=0, max_health=0)
    char.save()
    return char
