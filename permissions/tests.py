from django.test import TestCase

from permissions.models import TestModel, CharacterPermissions
from permissions.utils import AbstractPermissionSystem


class CharacterPermissionTest(TestCase):
    def setUp(self) -> None:
        super().setUp()

    def testDefaultPermissionManager(self):
        test_model = TestModel()
        test_model.save()
        assert test_model.manager is not None

    def testSubclasses(self):
        assert issubclass(TestModel, AbstractPermissionSystem)
        assert issubclass(CharacterPermissions, AbstractPermissionSystem)