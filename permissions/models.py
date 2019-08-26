from django.db import models

# Create your models here.
from base.models.character import Character
from permissions.utils import AbstractPermissionSystem


class PermissionManager(models.Model):
    def list_groups(self):
        return self.groups.all()

    def get_group_by_name(self, group_name):
        return self.groups.filter(name=group_name)

    def has_group(self, group_name):
        return self.groups.filter(name=group_name).exists()

    def create_group(self, group_name) -> 'Group':
        if self.has_group(group_name):
            return self.get_group_by_name(group_name)

        group = Group(name=group_name, manager=self)
        group.save()
        return group

    def get_permission(self, subject, permission):
        return self.permissions.filter(permission=permission, subject=subject)[0]

    def has_permission(self, subject, permission):
        return self.permissions.filter(permission=permission, subject=subject).exists()

    def list_permissions(self, subject):
        return [perm.permission for perm in self.permissions.filter(subject=subject)]

    def add_permission(self, subject, permission):
        if self.has_permission(subject, permission):
            pass

        perm = Permission(permission=permission, subject=subject, manager=self)
        perm.save()

    def remove_permission(self, subject, permission):
        if not self.has_permission(subject, permission):
            pass

        self.get_permission(subject, permission).delete()


class Group(models.Model):
    name = models.TextField()
    manager = models.ForeignKey(PermissionManager, related_name="groups", on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Character)

    def get_permission(self, permission) -> 'GroupPermission':
        return self.permissions.filter(permission=permission)[0]

    def has_permission(self, permission):
        return self.permissions.filter(permission=permission).exists()

    def list_permissions(self):
        return [perm.permission for perm in self.permissions.all()]

    def add_permission(self, permission):
        if self.has_permission(permission):
            pass

        perm = GroupPermission(permission=permission, group=self)
        perm.save()

    def remove_permission(self, permission):
        if not self.has_permission(permission):
            pass

        self.get_permission(permission).delete()

    def contains_subject(self, subject) -> bool:
        return subject in self.subjects

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

    def list_groups(self):
        return self.manager.list_groups()

    def has_group(self, group_name):
        return self.has_group(group_name)

    def get_group_by_name(self, group_name):
        return self.get_group_by_name(group_name)

    def create_group(self, group_name):
        return self.create_group(group_name)

    def has_permission(self, subject, permission):
        return self.has_permission(subject, permission)

    def list_permissions(self, subject):
        return self.list_permissions(subject)

    def add_permission(self, subject, permission):
        return self.add_permission(subject, permission)

    def remove_permission(self, subject, permission):
        return self.remove_permission(subject, permission)

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
