from permissions.models import Group
from permissions.tests.permission_test_case import PermissionTestCase


class CharacterPermissionGroupsTest(PermissionTestCase):
    GROUP_ONE = "group1"
    GROUP_TWO = "group2"
    GROUP_PERMISSION = "can_do_group_things"
    GROUP_PERMISSION_TWO = "can_do_group_dishes"

    def setUp(self) -> None:
        super().setUp()

        self.group1 = self.test_model.create_group(self.GROUP_ONE)
        self.group1.add_subject(self.charA2)
        self.group1.add_subject(self.charU1)
        self.group1.add_permission(self.GROUP_PERMISSION)

    def test_create_group(self):
        group2 = self.test_model.create_group(self.GROUP_TWO)
        group2.add_subject(self.charA1)
        group2.add_permission(self.GROUP_PERMISSION)
        assert len(self.test_model.list_groups()) == 2
        assert self.test_model.has_permission(self.charA1, self.GROUP_PERMISSION)

    def test_has_group(self):
        assert self.test_model.has_group(self.GROUP_ONE)
        assert not self.test_model.has_group(self.GROUP_TWO)

    def test_get_group_by_name(self):
        group = self.test_model.get_group_by_name(self.GROUP_ONE)
        assert group is not None
        assert isinstance(group, Group)

    def test_remove_permission(self):
        self.group1.remove_permission(self.GROUP_PERMISSION)
        assert not self.test_model.has_permission(self.charU1, self.GROUP_PERMISSION)

    def test_remove_non_existing_permission(self):
        self.group1.remove_permission(self.PERMISSION_UNUSED)
        assert not self.test_model.has_permission(self.charU1, self.PERMISSION_UNUSED)

    def test_list_groups(self):
        assert len(self.test_model.list_groups()) == 1

    def test_list_permissions(self):
        assert len(self.group1.list_permissions()) == 1

    def test_add_permission(self):
        self.group1.add_permission(self.GROUP_PERMISSION_TWO)
        assert len(self.group1.list_permissions()) == 2
        assert self.test_model.has_permission(self.charU1, self.GROUP_PERMISSION_TWO)

    def test_remove_group(self):
        self.group1.delete()
        assert len(self.test_model.list_groups()) == 0

    def test_remove_subject(self):
        self.group1.remove_subject(self.charU1)
        assert not self.test_model.has_permission(self.charU1, self.GROUP_PERMISSION)
        assert self.test_model.has_permission(self.charA2, self.GROUP_PERMISSION)

    def test_contains_subject(self):
        assert self.group1.contains_subject(self.charU1)
        assert self.group1.contains_subject(self.charA2)
        assert not self.group1.contains_subject(self.charA1)

    def test_has_permission(self):
        assert self.test_model.has_permission(self.charU1, self.GROUP_PERMISSION)
        assert self.test_model.has_permission(self.charA2, self.GROUP_PERMISSION)
        assert not self.test_model.has_permission(self.charU2, self.GROUP_PERMISSION)

    def test_same_group_name_two_objects(self):
        group = self.test_model_two.create_group(self.GROUP_ONE)
        group.add_subject(self.charA1)
        group.add_permission(self.GROUP_PERMISSION)
        assert not self.test_model.has_permission(self.charA1, self.GROUP_PERMISSION)
        assert self.test_model_two.has_permission(self.charA1, self.GROUP_PERMISSION)
