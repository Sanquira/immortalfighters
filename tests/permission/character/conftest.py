"""
Conftest for character permission tests
"""
import pytest

GROUP_ONE = "group1"
GROUP_TWO = "group2"
GROUP_PERMISSION = "can_do_group_things"
GROUP_PERMISSION_TWO = "can_do_group_dishes"


@pytest.fixture
def group1(model1, admin_char2, user_char1):
    """Test group with two subjects and one permission"""
    group = model1.create_group(GROUP_ONE)
    group.add_subject(admin_char2)
    group.add_subject(user_char1)
    group.add_permission(GROUP_PERMISSION)
    return group
