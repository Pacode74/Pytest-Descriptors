# Descriptors


class BaseValidator:
    def __init__(self, min_value=None, max_value=None):
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(self, cls, name):
        self.name = name

    def __get__(self, instance, cls):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, None)


class IntegerField(BaseValidator):
    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise ValueError(f"{self.name} must be an Integer.")
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"{self.name} cannot be less than {self.min_value}.")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"{self.name} cannot be more than {self.max_value}.")
        instance.__dict__[self.name] = value


class CharField(BaseValidator):
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError(f"{self.name} must be an String.")
        if self.min_value is not None and len(value) < self.min_value:
            raise ValueError(
                f"{self.name} cannot be less than {self.min_value} characters."
            )
        if self.max_value is not None and len(value) > self.max_value:
            raise ValueError(
                f"{self.name} cannot be more than {self.max_value} characters."
            )
        instance.__dict__[self.name] = value
