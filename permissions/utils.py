"""
Utility classes for the Permission submodule
"""
import abc
from abc import ABC


class AbstractPermissionSystem(ABC):
    """Interface for every PermissionSystem"""

    @abc.abstractmethod
    def list_groups(self):
        """Lists all the groups that exist in this manager"""

    @abc.abstractmethod
    def has_group(self, group_name: str) -> bool:
        """Checks if group exists"""

    @abc.abstractmethod
    def get_group_by_name(self, group_name: str):
        """Finds group by name"""

    @abc.abstractmethod
    def create_group(self, group_name: str):
        """Creates new group, if the group exists, returns the existing one"""

    @abc.abstractmethod
    def has_permission(self, subject, permission: str) -> bool:
        """Finds permission object for subject by the permission name"""

    @abc.abstractmethod
    def list_permissions(self, subject):
        """Lists all the permissions"""

    @abc.abstractmethod
    def add_permission(self, subject, permission: str):
        """Adds new permission for the subject"""

    @abc.abstractmethod
    def remove_permission(self, subject, permission: str):
        """Removes the permission from the subject"""
