"""
Conftest for permission tests
"""

# pylint: disable=unused-argument
import pytest
from permissions.models import TestModel

PERMISSION_ONE = "can_do_things"
PERMISSION_TWO = "can_cook_dinner"
PERMISSION_UNUSED = "is_useless"


@pytest.fixture
def model1(user_char1):
    """Test model with one user with one permission added"""
    test_model = TestModel()
    test_model.save()
    test_model.add_permission(user_char1, PERMISSION_TWO)
    return test_model


@pytest.fixture
def model2(transactional_db):
    """Blank test model"""
    test_model = TestModel()
    test_model.save()
    return test_model
