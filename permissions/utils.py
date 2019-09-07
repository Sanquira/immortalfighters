import abc
from abc import ABC


class AbstractPermissionSystem(ABC):

    @abc.abstractmethod
    def list_groups(self):
        pass

    @abc.abstractmethod
    def has_group(self, group_name: str) -> bool:
        pass

    @abc.abstractmethod
    def get_group_by_name(self, group_name: str):
        pass

    @abc.abstractmethod
    def create_group(self, group_name: str):
        pass

    @abc.abstractmethod
    def has_permission(self, subject, permission: str) -> bool:
        pass

    @abc.abstractmethod
    def list_permissions(self, subject):
        pass

    @abc.abstractmethod
    def add_permission(self, subject, permission: str):
        pass

    @abc.abstractmethod
    def remove_permission(self, subject, permission: str):
        pass
