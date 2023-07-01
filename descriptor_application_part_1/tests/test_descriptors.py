"""
Tests for Resource class
Command line: python -m pytest descriptor_application_part_1/tests/test_descriptors_part_1.py

To run a specific test:
Command line: python -m pytest descriptor_application_part_1/tests/test_descriptors_part_1.py::test_name

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
from descriptor_application_part_1.apps.descriptors import IntegerField, CharField
from pytest_check import check

pytestmark = pytest.mark.desc

# --------------test that come from the course for IntegerField----------------------


def test_set_age_ok(create_test_class):
    """Tests that valid values can be assigned/retrieved"""
    min_ = 5
    max_ = 10
    obj, _ = create_test_class(min_, max_)
    valid_values = range(min_, max_)

    for value in valid_values:
        obj.age = value
        assert value == obj.age


def test_set_age_invalid(create_test_class):
    """Tests that invalid values raise ValueErrors"""
    min_ = -10
    max_ = 10
    obj, _ = create_test_class(min_, max_)
    bad_values = list(range(min_ - 5, min_))
    bad_values += list(range(max_ + 1, max_ + 5))
    bad_values += [10.5, 1 + 0j, "abc", (1, 2)]

    for value in bad_values:
        with pytest.raises(ValueError) as e:
            obj.age = value


def test_class_get(create_test_class):
    """Tests that class attribute retrieval returns the descriptor instance"""
    obj, _ = create_test_class(0, 0)
    obj_class = type(obj)
    assert isinstance(obj_class.age, IntegerField)


def test_set_age_min_only(create_test_class):
    """Tests that we can specify a min value only"""
    min_ = 0
    max_ = None
    obj, _ = create_test_class(min_, max_)
    values = range(min_, min_ + 100, 10)
    for value in values:
        obj.age = value
        assert value == obj.age


def test_set_age_max_only(create_test_class):
    """Tests that we can specify a max value only"""
    min_ = None
    max_ = 10
    obj, _ = create_test_class(min_, max_)
    values = range(max_ - 100, max_, 10)
    for value in values:
        obj.age = value
        assert value == obj.age


def test_set_age_no_limits(create_test_class):
    """Tests that we can use IntegerField without any limits at all"""
    min_ = None
    max_ = None
    obj, _ = create_test_class(min_, max_)
    values = range(-100, 100, 10)
    for value in values:
        obj.age = value
        assert value == obj.age


# --------------test that come from the course for CharField----------------------
def test_set_name_ok(create_test_class):
    """Tests that valid values can be assigned/retrieved"""
    min_ = 1
    max_ = 10
    _, obj = create_test_class(min_, max_)
    valid_lengths = range(min_, max_)

    for length in valid_lengths:
        value = "a" * length
        obj.name = value
        assert value == obj.name


def test_set_name_invalid(create_test_class):
    """Tests that invalid values raise ValueErrors"""
    min_ = 5
    max_ = 10
    _, obj = create_test_class(min_, max_)
    bad_lengths = list(range(min_ - 5, min_))
    bad_lengths += list(range(max_ + 1, max_ + 5))
    for length in bad_lengths:
        value = "a" * length
        with pytest.raises(ValueError) as e:
            obj.name = value


def test_class_get(create_test_class):
    """Tests that class attribute retrieval returns the descriptor instance"""
    _, obj = create_test_class(0, 0)
    obj_class = type(obj)
    assert isinstance(obj_class.name, CharField)


def test_set_name_min_only(create_test_class):
    """Tests that we can specify a min length only"""
    min_ = 0
    max_ = None
    _, obj = create_test_class(min_, max_)
    valid_lengths = range(min_, min_ + 100, 10)
    for length in valid_lengths:
        value = "a" * length
        obj.name = value
        assert value == obj.name


def test_set_name_min_negative(create_test_class):
    """Tests that setting a negative or None length results in a zero length"""
    _, obj = create_test_class(-10, 100)
    assert type(obj).name.min_length == -10
    assert type(obj).name.max_length == 100
    _, obj = create_test_class(None, None)
    assert type(obj).name.min_length == None
    assert type(obj).name.max_length == None


def test_set_name_max_only(create_test_class):
    """Tests that we can specify a max length only"""
    min_ = None
    max_ = 10
    _, obj = create_test_class(min_, max_)
    valid_lengths = range(max_ - 100, max_, 10)
    for length in valid_lengths:
        value = "a" * length
        obj.name = value
        assert value == obj.name


def test_set_name_no_limits(create_test_class):
    """Tests that we can use CharField without any limits at all"""
    min_ = None
    max_ = None
    _, obj = create_test_class(min_, max_)
    valid_lengths = range(0, 100, 10)
    for length in valid_lengths:
        value = "a" * length
        obj.name = value
        assert value == obj.name


# ------------------- my own test ------------------------


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
    assert f"name cannot be less than {type(p).name.min_length} characters." == str(
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
    assert f"name cannot be more than {type(p).name.max_length} characters." == str(
        e.value
    )
