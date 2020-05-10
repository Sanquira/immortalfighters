"""Module containing serializable helper class"""


# pylint: disable=too-few-public-methods
class Serializable:
    """Simple serializable class that exports all field name into a dict ignoring protected fields"""
    def to_dict(self):
        """
        Returns all object fields in a dict form to be used for serialization purposes.
        It ignores all protected attributes and methods.
        """
        return {key: value for key, value in vars(self).items() if not key.startswith("_")}
