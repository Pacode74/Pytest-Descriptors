import numbers


class BaseValidator:
    def __init__(self, min_=None, max_=None):
        self._min = min_
        self._max = max_

    def __set_name__(self, owner_class, prop_name):
        self.prop_name = prop_name

    def __get__(self, instance, owner_class):
        if instance is None:
            return self
        else:
            return instance.__dict__.get(self.prop_name, None)

    def validate(self, value):
        # this will need to be implemented specifically by each subclass
        # here we just default to not raising any exceptions
        pass

    def __set__(self, instance, value):
        self.validate(value)
        instance.__dict__[self.prop_name] = value


class IntegerField(BaseValidator):
    def validate(self, value):
        if not isinstance(value, numbers.Integral):
            raise ValueError(f"{self.prop_name} must be an integer.")
        if self._min is not None and value < self._min:
            raise ValueError(f"{self.prop_name} must be >= {self._min}.")
        if self._max is not None and value > self._max:
            raise ValueError(f"{self.prop_name} must be <= {self._max}")


class CharField(BaseValidator):
    def __init__(self, min_, max_):
        min_ = max(min_ or 0, 0)
        super().__init__(min_, max_)

    def validate(self, value):
        if not isinstance(value, str):
            raise ValueError(f"{self.prop_name} must be a string.")
        if self._min is not None and len(value) < self._min:
            raise ValueError(f"{self.prop_name} must be >= {self._min} chars.")
        if self._max is not None and len(value) > self._max:
            raise ValueError(f"{self.prop_name} must be <= {self._max} chars")
