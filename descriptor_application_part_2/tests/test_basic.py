# test_basic.py
from descriptor_application_part_1.apps.basic import addition


def test_basic(demo_fixt) -> None:
    """Basic test to test Continuous Integration works correctly."""
    a, b, expected = demo_fixt
    result = addition(a, b)
    assert result == expected
