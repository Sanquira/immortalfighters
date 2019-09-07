from typing import List

from django.db import models

# Create your models here.
from base.models.character import Character
from permissions.utils import AbstractPermissionSystem


class PermissionManager(models.Model):
    def list_groups(self):
        return self.groups.all()

    def get_group_by_name(self, group_name: str) -> 'Group':
        return self.groups.get(name=group_name)

    def has_group(self, group_name: str) -> bool:
        return self.groups.filter(name=group_name).exists()

    def create_group(self, group_name: str) -> 'Group':
        if self.has_group(group_name):
            return self.get_group_by_name(group_name)

        group = Group(name=group_name, manager=self)
        group.save()
        return group

    def get_permission(self, subject: Character, permission: str) -> 'Permission':
        return self.permissions.get(permission=permission, subject=subject)

    def has_permission(self, subject: Character, permission: str) -> bool:
        if self.permissions.filter(permission=permission, subject=subject).exists():
            return True

        for group in self.groups.all():
            if group.contains_subject(subject) and group.has_permission(permission):
                return True
        return False

    def list_permissions(self, subject: Character) -> List['Permission']:
        return [perm.permission for perm in self.permissions.filter(subject=subject)]

    def add_permission(self, subject: Character, permission: str):
        if self.has_permission(subject, permission):
            return

        perm = Permission(permission=permission, subject=subject, manager=self)
        perm.save()

    def remove_permission(self, subject: Character, permission: str):
        if not self.has_permission(subject, permission):
            return

        self.get_permission(subject, permission).delete()


class Group(models.Model):
    name = models.TextField()
    manager = models.ForeignKey(PermissionManager, related_name="groups", on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Character)

    def get_permission(self, permission: str) -> 'GroupPermission':
        return self.permissions.get(permission=permission)

    def has_permission(self, permission: str) -> bool:
        return self.permissions.filter(permission=permission).exists()

    def list_permissions(self) -> List['GroupPermission']:
        return [perm.permission for perm in self.permissions.all()]

    def add_permission(self, permission: str):
        if self.has_permission(permission):
            return

        perm = GroupPermission(permission=permission, group=self)
        perm.save()

    def remove_permission(self, permission: str):
        if not self.has_permission(permission):
            return

        self.get_permission(permission).delete()

    def contains_subject(self, subject: Character) -> bool:
        return subject in self.subjects.all()

    def add_subject(self, subject: Character):
        return self.subjects.add(subject)

    def remove_subject(self, subject: Character):
        return self.subjects.remove(subject)

    class Meta:
        unique_together = [['name', 'manager']]


class Permission(models.Model):
    permission = models.TextField(max_length=30)
    subject = models.ForeignKey(Character, on_delete=models.CASCADE)
    manager = models.ForeignKey(PermissionManager, related_name="permissions", on_delete=models.CASCADE)

    class Meta:
        unique_together = [['subject', 'permission', 'manager']]


class GroupPermission(models.Model):
    permission = models.TextField(max_length=30)
    group = models.ForeignKey(Group, related_name="permissions", on_delete=models.CASCADE)

    class Meta:
        unique_together = [['group', 'permission']]


class CharacterPermissions(models.Model):
    manager = models.ForeignKey(PermissionManager, on_delete=models.CASCADE)

    def list_groups(self) -> List[Group]:
        return self.manager.list_groups()

    def has_group(self, group_name: str) -> bool:
        return self.manager.has_group(group_name)

    def get_group_by_name(self, group_name: str) -> Group:
        return self.manager.get_group_by_name(group_name)

    def create_group(self, group_name: str) -> Group:
        return self.manager.create_group(group_name)

    def has_permission(self, subject: Character, permission: str) -> bool:
        return self.manager.has_permission(subject, permission)

    def list_permissions(self, subject: Character) -> List[Permission]:
        return self.manager.list_permissions(subject)

    def add_permission(self, subject: Character, permission: str):
        return self.manager.add_permission(subject, permission)

    def remove_permission(self, subject: Character, permission: str):
        return self.manager.remove_permission(subject, permission)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        try:
            self.manager
        except PermissionManager.DoesNotExist:
            manager = PermissionManager()
            manager.save()
            self.manager = manager

        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = "Permissions"


class TestModel(CharacterPermissions):
    pass


# Problems with Django models and metaclasses
AbstractPermissionSystem.register(PermissionManager)
AbstractPermissionSystem.register(CharacterPermissions)
