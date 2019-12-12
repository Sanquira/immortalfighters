"""
Models for the Permission submodule
"""
from typing import List

from django.db import models

from base.models.character import Character
from permissions.utils import AbstractPermissionSystem


class PermissionManager(models.Model):
    """
    Manages the permissions. All permissions are bound to specific manager.
    You can either attach specific permission to the subject itself,
    or use groups of subjects and attach permissions to them.
    To use this class, simply create model than inherits from this model.
    """
    def list_groups(self):
        """Lists all the groups that exist in this manager"""
        return self.groups.all()

    def get_group_by_name(self, group_name: str) -> 'Group':
        """Finds group by name"""
        return self.groups.get(name=group_name)

    def has_group(self, group_name: str) -> bool:
        """Checks if said group exists"""
        return self.groups.filter(name=group_name).exists()

    def create_group(self, group_name: str) -> 'Group':
        """Creates new group, if the group exists, returns the existing one"""
        if self.has_group(group_name):
            return self.get_group_by_name(group_name)

        group = Group(name=group_name, manager=self)
        group.save()
        return group

    def get_permission(self, subject: Character, permission: str) -> 'Permission':
        """Finds permission object for subject by the permission name"""
        return self.permissions.get(permission=permission, subject=subject)

    def has_permission(self, subject: Character, permission: str) -> bool:
        """Checks if subject has permission"""
        if self.permissions.filter(permission=permission, subject=subject).exists():
            return True

        for group in self.groups.all():
            if group.contains_subject(subject) and group.has_permission(permission):
                return True
        return False

    def list_permissions(self, subject: Character) -> List['Permission']:
        """Lists all the permissions"""
        return [perm.permission for perm in self.permissions.filter(subject=subject)]

    def add_permission(self, subject: Character, permission: str):
        """Adds new permission for the subject"""
        if self.has_permission(subject, permission):
            return

        perm = Permission(permission=permission, subject=subject, manager=self)
        perm.save()

    def remove_permission(self, subject: Character, permission: str):
        """Removes the permission from the subject"""
        if not self.has_permission(subject, permission):
            return

        self.get_permission(subject, permission).delete()


class Group(models.Model):
    """
    Collection on subjects that has permissions.
    Interface is extension of the PermissionManager's one.
    """
    name = models.TextField()
    manager = models.ForeignKey(PermissionManager, related_name="groups", on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Character)

    def get_permission(self, permission: str) -> 'GroupPermission':
        """Finds GroupPermission objects by the permission name"""
        return self.permissions.get(permission=permission)

    def has_permission(self, permission: str) -> bool:
        """Checks if group has permission"""
        return self.permissions.filter(permission=permission).exists()

    def list_permissions(self) -> List['GroupPermission']:
        """Lists all the permissions for this group"""
        return [perm.permission for perm in self.permissions.all()]

    def add_permission(self, permission: str):
        """Adds new permission for the group"""
        if self.has_permission(permission):
            return

        perm = GroupPermission(permission=permission, group=self)
        perm.save()

    def remove_permission(self, permission: str):
        """Removes the permission from the group"""
        if not self.has_permission(permission):
            return

        self.get_permission(permission).delete()

    def contains_subject(self, subject: Character) -> bool:
        """Checks if group contains the subject"""
        return subject in self.subjects.all()

    def add_subject(self, subject: Character):
        """Add subject to this group"""
        return self.subjects.add(subject)

    def remove_subject(self, subject: Character):
        """Remove subject from this group"""
        return self.subjects.remove(subject)

    class Meta:
        unique_together = [['name', 'manager']]


class Permission(models.Model):
    """Simple subject permission binding"""
    permission = models.TextField(max_length=30)
    subject = models.ForeignKey(Character, on_delete=models.CASCADE)
    manager = models.ForeignKey(PermissionManager, related_name="permissions", on_delete=models.CASCADE)

    class Meta:
        unique_together = [['subject', 'permission', 'manager']]


class GroupPermission(models.Model):
    """Simple group permission binding"""
    permission = models.TextField(max_length=30)
    group = models.ForeignKey(Group, related_name="permissions", on_delete=models.CASCADE)

    class Meta:
        unique_together = [['group', 'permission']]


class CharacterPermissions(models.Model):
    """
    Parent of all objects that should use Permission submodule.
    To use simply create new model with this as its parent
    """
    manager = models.ForeignKey(PermissionManager, on_delete=models.CASCADE)

    def list_groups(self) -> List[Group]:
        """Lists all the groups that exist in this manager"""
        return self.manager.list_groups()

    def has_group(self, group_name: str) -> bool:
        """Checks if group exists"""
        return self.manager.has_group(group_name)

    def get_group_by_name(self, group_name: str) -> Group:
        """Finds group by name"""
        return self.manager.get_group_by_name(group_name)

    def create_group(self, group_name: str) -> Group:
        """Creates new group, if the group exists, returns the existing one"""
        return self.manager.create_group(group_name)

    def has_permission(self, subject: Character, permission: str) -> bool:
        """Finds permission object for subject by the permission name"""
        return self.manager.has_permission(subject, permission)

    def list_permissions(self, subject: Character) -> List[Permission]:
        """Lists all the permissions"""
        return self.manager.list_permissions(subject)

    def add_permission(self, subject: Character, permission: str):
        """Adds new permission for the subject"""
        return self.manager.add_permission(subject, permission)

    def remove_permission(self, subject: Character, permission: str):
        """Removes the permission from the subject"""
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
    """Simple descedant of CharacterPermission used for testing purposes"""


# Problems with Django models and metaclasses
AbstractPermissionSystem.register(PermissionManager)
AbstractPermissionSystem.register(CharacterPermissions)
