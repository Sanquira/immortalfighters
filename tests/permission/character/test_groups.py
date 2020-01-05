"""
Tests for using groups in character permission system
"""
# pylint: disable=unused-argument
from permissions.models import Group
from tests.permission.character.conftest import GROUP_TWO, GROUP_PERMISSION, GROUP_ONE, GROUP_PERMISSION_TWO
from tests.permission.conftest import PERMISSION_UNUSED


def test_create_group(model1, group1, admin_char1):
    """Tests creation of the new group"""
    group2 = model1.create_group(GROUP_TWO)
    group2.add_subject(admin_char1)
    group2.add_permission(GROUP_PERMISSION)
    assert len(model1.list_groups()) == 2
    assert model1.has_permission(admin_char1, GROUP_PERMISSION)


def test_has_group(model1, group1):
    """Tests existence of existing rooms"""
    assert model1.has_group(GROUP_ONE)
    assert not model1.has_group(GROUP_TWO)


def test_get_group_by_name(model1, group1):
    """Tests fetching group by name"""
    group = model1.get_group_by_name(GROUP_ONE)
    assert group is not None
    assert isinstance(group, Group)


def test_remove_permission(model1, group1, user_char1):
    """Tests that you can remove permission from a group and it applies to all members"""
    group1.remove_permission(GROUP_PERMISSION)
    assert not model1.has_permission(user_char1, GROUP_PERMISSION)


def test_remove_non_existing_permission(model1, group1, user_char1):
    """Tests that you can remove non existing permission from the group"""
    group1.remove_permission(PERMISSION_UNUSED)
    assert not model1.has_permission(user_char1, PERMISSION_UNUSED)


def test_list_groups(model1, group1):
    """Tests list of all groups"""
    assert len(model1.list_groups()) == 1


def test_list_permissions(group1):
    """Tests list of permissions for a group"""
    assert len(group1.list_permissions()) == 1


def test_add_permission(model1, group1, user_char1):
    """Tests adding permission to the group"""
    group1.add_permission(GROUP_PERMISSION_TWO)
    assert len(group1.list_permissions()) == 2
    assert model1.has_permission(user_char1, GROUP_PERMISSION_TWO)


def test_remove_group(model1, group1):
    """Tests removing group"""
    group1.delete()
    assert len(model1.list_groups()) == 0


def test_remove_subject(model1, group1, user_char1, admin_char2):
    """Tests removing user from group"""
    group1.remove_subject(user_char1)
    assert not model1.has_permission(user_char1, GROUP_PERMISSION)
    assert model1.has_permission(admin_char2, GROUP_PERMISSION)


def test_contains_subject(group1, user_char1, admin_char2, admin_char1):
    """Tests checking if group includes user"""
    assert group1.contains_subject(user_char1)
    assert group1.contains_subject(admin_char2)
    assert not group1.contains_subject(admin_char1)


def test_has_permission(model1, group1, user_char1, admin_char2, user_char2):
    """Tests checking if user in group has permission"""
    assert model1.has_permission(user_char1, GROUP_PERMISSION)
    assert model1.has_permission(admin_char2, GROUP_PERMISSION)
    assert not model1.has_permission(user_char2, GROUP_PERMISSION)


def test_same_group_name_two_objects(model1, model2, admin_char1):
    """Tests permission checking on multiple models"""
    group = model2.create_group(GROUP_ONE)
    group.add_subject(admin_char1)
    group.add_permission(GROUP_PERMISSION)
    assert not model1.has_permission(admin_char1, GROUP_PERMISSION)
    assert model2.has_permission(admin_char1, GROUP_PERMISSION)
