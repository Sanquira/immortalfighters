from django.test import TestCase

from base.models import IFUser
from base.models.character import Character
from permissions.models import TestModel, CharacterPermissions
from permissions.utils import AbstractPermissionSystem


class CharacterPermissionTest(TestCase):
    def setUp(self) -> None:
        super().setUp()
        
        self.admin1 = IFUser.objects.create_superuser(username="Admin", email="kiss.my.ass@lol.net", password="admin")
        self.user1 = IFUser.objects.create_user(username="User", email="fluffy.pedo.bear@lol.net", password="user")
        self.admin1.save()
        self.user1.save()
        
        self.charA1 = Character(owner=self.admin1, character_name="Kitten")
        self.charA1.save()
        self.charA2 = Character(owner=self.admin1, character_name="Shitten")
        self.charA2.save()
        
        self.charU1 = Character(owner=self.user1, character_name="Dog")
        self.charU1.save()
        self.charU2 = Character(owner=self.user1, character_name="Shog")
        self.charU2.save()
    
    def testDefaultPermissionManager(self):
        test_model = TestModel()
        test_model.save()
        assert test_model.manager is not None
    
    def testSubclasses(self):
        assert issubclass(TestModel, AbstractPermissionSystem)
        assert issubclass(CharacterPermissions, AbstractPermissionSystem)
