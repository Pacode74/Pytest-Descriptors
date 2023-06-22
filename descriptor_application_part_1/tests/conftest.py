# conftest.py
import pytest
from faker import Faker
from descriptor_application_part_1.apps.descriptors import IntegerField, CharField
from datetime import datetime, timedelta
from typing import Callable


# --------------------- used for basic test to check that CI works correctly------------------
@pytest.fixture(
    params=[
        (1, 1, 2),
        (2, 2, 4),
        (3, 4, 7),
        (7, 5, 12),
        (12, 6, 18),
    ]
)
def demo_fixt(request):
    """fixture for basic test to test basic app"""
    # print(f'{request.param=}')
    return request.param


# ------------------for faker, used in test_simple_with_faker ------
@pytest.fixture
def fake():
    fake = Faker()
    fake.seed_instance(1234)
    return fake


# ----------use in any test to truck timing-------------
@pytest.fixture
def time_tracker():
    """In order to use the time tracker in our test we need to mark it as a fixture."""
    start = datetime.now()
    yield  # yield and pass the cpu to run the test
    end = datetime.now()
    diff = end - start
    print(f"\n runtime: {diff.total_seconds()}")


@pytest.fixture
def person():
    class Person:
        name = CharField(2, 5)
        age = IntegerField(0, 100)

    return Person()


def faker(n):
    fake = Faker()
    return [fake.name()[:5] for _ in range(n)]


@pytest.fixture(params=[faker(10)])
def generate_short_name(request):
    return request.param
