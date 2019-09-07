from django.test import TestCase

from base.models import IFUser
from base.models.character import Character
from permissions.models import TestModel, CharacterPermissions


class PermissionTestCase(TestCase):
    PERMISSION_ONE = "can_do_things"
    PERMISSION_TWO = "can_cook_dinner"
    PERMISSION_UNUSED = "is_useless"

    def setUp(self) -> None:
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

        self.test_model = TestModel()
        self.test_model.save()
        self.test_model.add_permission(self.charU1, self.PERMISSION_TWO)

        self.test_model_two = TestModel()
        self.test_model_two.save()
