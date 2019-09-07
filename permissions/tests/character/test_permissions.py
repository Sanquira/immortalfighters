from permissions.models import TestModel, CharacterPermissions
from permissions.tests.permission_test_case import PermissionTestCase
from permissions.utils import AbstractPermissionSystem


class CharacterPermissionTest(PermissionTestCase):
    def test_default_permission_manager(self):
        assert self.test_model.manager is not None

    def test_subclasses(self):
        assert issubclass(TestModel, AbstractPermissionSystem)
        assert issubclass(CharacterPermissions, AbstractPermissionSystem)

    def test_add_permission(self):
        self.test_model.add_permission(self.charA1, self.PERMISSION_ONE)
        assert self.test_model.has_permission(self.charA1, self.PERMISSION_ONE)
        assert not self.test_model.has_permission(self.charU1, self.PERMISSION_ONE)
        assert not self.test_model.has_permission(self.charA2, self.PERMISSION_ONE)

    def test_remove_permission(self):
        self.test_model.remove_permission(self.charU1, self.PERMISSION_TWO)
        assert not self.test_model.has_permission(self.charU1, self.PERMISSION_TWO)

    def test_remove_non_existing_permission(self):
        self.test_model.remove_permission(self.charU1, self.PERMISSION_UNUSED)
        assert not self.test_model.has_permission(self.charU1, self.PERMISSION_UNUSED)
        self.test_model.remove_permission(self.charA1, self.PERMISSION_UNUSED)
        assert not self.test_model.has_permission(self.charA1, self.PERMISSION_UNUSED)

    def test_list_permissions(self):
        assert len(self.test_model.list_permissions(self.charU1)) == 1
        assert len(self.test_model.list_permissions(self.charA2)) == 0

    def test_has_permission(self):
        assert self.test_model.has_permission(self.charU1, self.PERMISSION_TWO)
