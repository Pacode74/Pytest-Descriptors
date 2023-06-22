# Descriptors


class IntegerField:
    def __init__(self, min_value=None, max_value=None):
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(self, cls, name):
        self.name = name

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise ValueError(f"{self.name} must be an Integer.")
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"{self.name} cannot be less than {self.min_value}.")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"{self.name} cannot be more than {self.max_value}.")
        instance.__dict__[self.name] = value

    def __get__(self, instance, cls):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, None)


class CharField:
    def __init__(self, min_length=None, max_length=None):
        self.min_length = min_length
        self.max_length = max_length

    def __set_name__(self, cls, name):
        self.name = name

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError(f"{self.name} must be an String.")
        if self.min_length is not None and len(value) < self.min_length:
            raise ValueError(
                f"{self.name} cannot be less than {self.min_length} characters."
            )
        if self.max_length is not None and len(value) > self.max_length:
            raise ValueError(
                f"{self.name} cannot be more than {self.max_length} characters."
            )
        instance.__dict__[self.name] = value

    def __get__(self, instance, cls):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, None)
