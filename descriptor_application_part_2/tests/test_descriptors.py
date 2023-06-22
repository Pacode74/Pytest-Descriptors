"""
Tests for Resource class
Command line: python -m pytest descriptor_application_part_1/tests/test_descriptors.py

To run a specific test:
Command line: python -m pytest descriptor_application_part_1/tests/test_descriptors.py::test_name

To run test under specific pattern:
Command line: pytest -k "test_validate or test_some_other_test"

I want to apply the same marker for all below pytest:
pytestmark = pytest.mark.xyz or pytestmark = [pytest.mark.xyz, pytest.mark.abc]
pytestmark = pytest.mark.resources
Also need to register the marker in pytest.ini
Command line: pytest -m resources

To check coverage: $ coverage run -m pytest .
To generate coverage report: $ coverage html
"""


import pytest
from descriptor_application_part_2.apps.descriptors import IntegerField, CharField
from pytest_check import check
import inspect
import types

pytestmark = pytest.mark.desc


def test_name(person, generate_short_name):
    p = person
    for short_name in generate_short_name:
        p.name = short_name
        # print(f'{p.name=}')
        assert p.name == short_name


def test_age(person):
    p = person
    for n in range(0, 101):
        with check:
            p.age = n
            assert p.age == n


def test_descriptors_instance():
    class Person:
        name = CharField(0, 10)
        age = IntegerField(0, 100)

    p = Person()
    with check:
        assert Person.name == type(p).name.__get__(None, type(p))
    with check:
        assert Person.age == type(p).age.__get__(None, type(p))


@pytest.mark.parametrize(
    "name,age",
    [
        (r, 100)
        for r in [
            [1, 2, 3],
            1,
            2j + 1,
            0.1,
            -0.5,
            int,
            str,
            float,
            complex,
            list,
            tuple,
            range,
            dict,
            set,
            frozenset,
        ]
    ],
)
def test_raise_type_exception_should_pass_parameterize_name(
    person, name: str, age: int
) -> None:
    with pytest.raises(ValueError) as e:
        p = person
        p.age = age
        p.name = name
    assert "name must be an String." == str(e.value)


@pytest.mark.parametrize(
    "name,age",
    [
        ("Alex", r)
        for r in [
            [1, 2, 3],
            "John",
            2j + 1,
            0.1,
            -0.5,
            int,
            str,
            float,
            complex,
            list,
            tuple,
            range,
            dict,
            set,
            frozenset,
        ]
    ],
)
def test_raise_type_exception_should_pass_parameterize_age(
    person, name: str, age: int
) -> None:
    with pytest.raises(ValueError) as e:
        p = person
        p.age = age
        p.name = name
    assert "age must be an Integer." == str(e.value)


@pytest.mark.parametrize(
    "number, exception", [(-1, ValueError), (-2, ValueError), (-3, ValueError)]
)
def test_create_invalid_min_age(number, exception, person):
    with pytest.raises(exception) as e:
        p = person
        p.age = number
    assert f"age cannot be less than {type(p).age.min_value}." == str(e.value)


@pytest.mark.parametrize(
    "number, exception", [(102, ValueError), (103, ValueError), (104, ValueError)]
)
def test_create_invalid_max_age(number, exception, person):
    with pytest.raises(exception) as e:
        p = person
        p.age = number
    assert f"age cannot be more than {type(p).age.max_value}." == str(e.value)


@pytest.mark.parametrize(
    "name, exception", [("", ValueError), ("V", ValueError), ("D", ValueError)]
)
def test_create_invalid_min_name(name, exception, person):
    with pytest.raises(exception) as e:
        p = person
        p.name = name
    assert f"name cannot be less than {type(p).name.min_value} characters." == str(
        e.value
    )


@pytest.mark.parametrize(
    "name, exception",
    [("Alexander", ValueError), ("Victor", ValueError), ("Silvester", ValueError)],
)
def test_create_invalid_max_name(name, exception, person):
    with pytest.raises(exception) as e:
        p = person
        p.name = name
    assert f"name cannot be more than {type(p).name.max_value} characters." == str(
        e.value
    )
