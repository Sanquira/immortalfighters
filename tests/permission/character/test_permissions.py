"""
Tests for using permissions in character permission system
"""
from permissions.models import TestModel, CharacterPermissions
from permissions.utils import AbstractPermissionSystem
from tests.permission.conftest import PERMISSION_ONE, PERMISSION_TWO, PERMISSION_UNUSED

def test_default_permission_manager(model2):
    """Tests that manager is automatically created if he is not provided"""
    assert model2.manager is not None


def test_subclasses():
    """Tests that subclasses implement permission system"""
    assert issubclass(TestModel, AbstractPermissionSystem)
    assert issubclass(CharacterPermissions, AbstractPermissionSystem)


def test_add_permission(model1, admin_char1, user_char1, admin_char2):
    """Tests that you can add a new permission"""
    model1.add_permission(admin_char1, PERMISSION_ONE)
    assert model1.has_permission(admin_char1, PERMISSION_ONE)
    assert not model1.has_permission(user_char1, PERMISSION_ONE)
    assert not model1.has_permission(admin_char2, PERMISSION_ONE)


def test_remove_permission(model1, user_char1):
    """Tests that you can remove a permission"""
    model1.remove_permission(user_char1, PERMISSION_TWO)
    assert not model1.has_permission(user_char1, PERMISSION_TWO)


def test_remove_non_existing_permission(model1, user_char1, admin_char1):
    """Tests that you can remove nonexistent permission"""
    model1.remove_permission(user_char1, PERMISSION_UNUSED)
    assert not model1.has_permission(user_char1, PERMISSION_UNUSED)
    model1.remove_permission(admin_char1, PERMISSION_UNUSED)
    assert not model1.has_permission(admin_char1, PERMISSION_UNUSED)


def test_list_permissions(model1, user_char1, admin_char2):
    """Tests that you can list all permissions"""
    assert len(model1.list_permissions(user_char1)) == 1
    assert len(model1.list_permissions(admin_char2)) == 0


def test_has_permission(model1, user_char1):
    """Tests permission check"""
    assert model1.has_permission(user_char1, PERMISSION_TWO)
